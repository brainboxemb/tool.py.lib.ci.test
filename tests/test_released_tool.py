"""Tests run through the released tool.py.lib.ci workflow."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

import packaging
import tool_py_lib_ci_test_library


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL_SHA = "58ead6897a4ac8cafef22a3c1f834491bf61568d"
TOOL_ROOT = ROOT / ".tool-py-lib-ci"
TOOL_SCRIPT = TOOL_ROOT / "scripts" / "library_ci.py"
CHANGE_SCOPE_SCRIPT = TOOL_ROOT / "scripts" / "change_scope.py"
RELEASE_WORKFLOW = TOOL_ROOT / ".github" / "workflows" / "reusable-release.yml"
TEMPLATE_MANIFEST = TOOL_ROOT / "templates" / "manifest.json"


def load_change_scope():
    """Load the classifier from the exact released tool checkout."""

    spec = spec_from_file_location("released_change_scope", CHANGE_SCOPE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHANGE_SCOPE_SCRIPT}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_library(
    root: pathlib.Path,
    *,
    name: str,
    dependency: str | None = None,
    failing_test: bool = False,
) -> pathlib.Path:
    """Create one disposable Python library for a failure-path test."""

    package = name.replace("-", "_")
    repo = root / name
    (repo / "src" / package).mkdir(parents=True)
    (repo / "tests").mkdir()
    dependencies = [] if dependency is None else [dependency]
    (repo / "pyproject.toml").write_text(
        textwrap.dedent(
            f"""
            [build-system]
            requires = ["setuptools>=68", "wheel"]
            build-backend = "setuptools.build_meta"

            [project]
            name = "{name}"
            version = "0.1.0"
            dependencies = {dependencies!r}

            [tool.setuptools.packages.find]
            where = ["src"]
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (repo / "src" / package / "__init__.py").write_text(
        'VALUE = "ok"\n',
        encoding="utf-8",
    )
    assertion = "self.fail('expected test failure')" if failing_test else (
        f"self.assertEqual({package}.VALUE, 'ok')"
    )
    (repo / "tests" / "test_package.py").write_text(
        textwrap.dedent(
            f"""
            import unittest
            import {package}


            class PackageTests(unittest.TestCase):
                def test_package(self):
                    {assertion}


            if __name__ == "__main__":
                unittest.main()
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    return repo


class ReleasedToolTests(unittest.TestCase):
    def run_tool(self, repo: pathlib.Path, work: pathlib.Path) -> subprocess.CompletedProcess:
        """Run the exact released package-CI script."""

        return subprocess.run(
            [
                sys.executable,
                str(TOOL_SCRIPT),
                "--repo",
                str(repo),
                "--work",
                str(work),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_installed_wheel_and_declared_dependency(self):
        source = pathlib.Path(tool_py_lib_ci_test_library.__file__).resolve()
        self.assertFalse(source.is_relative_to(ROOT))
        self.assertEqual(tool_py_lib_ci_test_library.VALUE, "installed-wheel")
        self.assertTrue(packaging.__version__)
        self.assertIsNotNone(
            shutil.which("tool-py-lib-ci-test-command")
        )

    def test_exact_released_tool_commit(self):
        self.assertTrue(TOOL_ROOT.is_dir())
        actual = subprocess.check_output(
            ["git", "-C", str(TOOL_ROOT), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        self.assertEqual(actual, TOOL_SHA)

        manifest = (ROOT / "dependencies.repos").read_text(encoding="utf-8")
        self.assertIn(f"tool.py.lib.ci.commit={TOOL_SHA}", manifest)

        workflow = (
            ROOT / ".github" / "workflows" / "ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            f"tool.py.lib.ci/.github/workflows/reusable-ci.yml@{TOOL_SHA}",
            workflow,
        )

    def test_released_workflow_cancels_same_caller_scope(self):
        workflow = (
            TOOL_ROOT / ".github" / "workflows" / "reusable-ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("concurrency:", workflow)
        self.assertIn("cancel-in-progress: true", workflow)
        self.assertIn("github.repository", workflow)
        self.assertIn("github.workflow", workflow)
        self.assertIn(
            "github.event.pull_request.number || github.ref",
            workflow,
        )

    def test_released_docs_only_classifier_fails_safe(self):
        classifier = load_change_scope()
        self.assertEqual(
            classifier.classify_paths(["docs/plan.md", "docs/design.md"]),
            "docs-only",
        )
        for paths in (
            [],
            ["README.md"],
            ["docs/plan.md", "src/package.py"],
            [".github/workflows/ci.yml"],
        ):
            with self.subTest(paths=paths):
                self.assertEqual(classifier.classify_paths(paths), "full")

    def test_released_push_comparison_fails_safe(self):
        classifier = load_change_scope()
        sha_a = "a" * 40
        sha_b = "b" * 40
        zero = "0" * 40

        self.assertEqual(
            classifier.comparison_base(
                event_name="pull_request",
                source_sha_input="",
                pull_base_sha=sha_a,
                push_before_sha="",
                push_forced=False,
            ),
            sha_a,
        )
        self.assertEqual(
            classifier.comparison_base(
                event_name="push",
                source_sha_input="",
                pull_base_sha="",
                push_before_sha=sha_b,
                push_forced=False,
            ),
            sha_b,
        )

        for values in (
            dict(event_name="push", source_sha_input="", pull_base_sha="", push_before_sha=sha_b, push_forced=True),
            dict(event_name="push", source_sha_input="", pull_base_sha="", push_before_sha=zero, push_forced=False),
            dict(event_name="push", source_sha_input="override", pull_base_sha="", push_before_sha=sha_b, push_forced=False),
            dict(event_name="push", source_sha_input="", pull_base_sha="", push_before_sha="invalid", push_forced=False),
        ):
            with self.subTest(values=values):
                self.assertIsNone(classifier.comparison_base(**values))

    def test_released_workflow_has_conservative_docs_only_path(self):
        workflow = (
            TOOL_ROOT / ".github" / "workflows" / "reusable-ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("EVENT_NAME", workflow)
        self.assertIn("SOURCE_SHA_INPUT", workflow)
        self.assertIn("git diff --name-only -z --no-renames", workflow)
        self.assertIn("scripts/change_scope.py base", workflow)
        self.assertIn("scripts/change_scope.py classify", workflow)
        self.assertIn("PUSH_BEFORE_SHA", workflow)
        self.assertIn("PUSH_FORCED", workflow)
        self.assertIn(
            "Skip package validation for documentation-only change",
            workflow,
        )
        self.assertIn(
            "if: steps.scope.outputs.scope != 'docs-only'",
            workflow,
        )
        self.assertIn(
            "Python library CI skipped build/install/test:",
            workflow,
        )
        self.assertIn("change_scope:", workflow)
        self.assertIn("jobs.test.outputs.change_scope", workflow)
        self.assertIn("steps.scope.outputs.scope", workflow)

    def test_released_workflow_has_no_cad_scons_or_github_cache(self):
        workflow = (
            TOOL_ROOT / ".github" / "workflows" / "reusable-ci.yml"
        ).read_text(encoding="utf-8").lower()
        for value in (
            "actions/cache",
            "scons",
            ".cad-ci",
            ".cache/cad-ci",
            "tool.cad.ci",
            "lib.py.cad.ci",
        ):
            with self.subTest(value=value):
                self.assertNotIn(value, workflow)

    def test_released_release_workflow_and_templates(self):
        release = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        for value in (
            "workflow_call:",
            "Validate caller release context",
            "Checkout exact requested library source",
            "Run repository release validator",
            "Publish or verify exact GitHub release",
            "Record release on triggering issue",
            "scripts/release_command.py",
            "persist-credentials: false",
        ):
            with self.subTest(value=value):
                self.assertIn(value, release)

        import json
        manifest = json.loads(TEMPLATE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("schema"), 1)
        self.assertEqual(
            manifest.get("templates"),
            {
                "github/workflows/ci.yml": {
                    "id": "tool.py.lib.ci/ci",
                    "version": 1,
                    "surface": "reusable-ci.yml",
                },
                "github/workflows/release.yml": {
                    "id": "tool.py.lib.ci/release",
                    "version": 1,
                    "surface": "reusable-release.yml",
                },
            },
        )

        for relative, entry in manifest["templates"].items():
            template = (TOOL_ROOT / "templates" / relative).read_text(
                encoding="utf-8"
            )
            self.assertIn(f"# template: {entry['id']}", template)
            self.assertIn(
                f"# template-version: {entry['version']}",
                template,
            )
            self.assertEqual(
                template.count("TOOL_PY_LIB_CI_RELEASE_SHA"),
                2,
            )

    def test_acceptance_release_wrapper_is_thin_and_exactly_pinned(self):
        wrapper = (
            ROOT / ".github" / "workflows" / "release.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "brainboxemb/tool.py.lib.ci/.github/workflows/"
            f"reusable-release.yml@{TOOL_SHA}",
            wrapper,
        )
        self.assertIn(
            "validator_path: release_case/validate_release.py",
            wrapper,
        )
        for forbidden in (
            "actions/checkout@",
            "gh api",
            "git tag",
            "git push",
            "publish_release.py",
            "release_command.py",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, wrapper)

    def test_build_failure_is_returned_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            broken = root / "broken"
            broken.mkdir()
            result = self.run_tool(broken, root / "work")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR: build:", result.stdout)

    def test_library_test_failure_is_returned_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            failing = write_library(
                root,
                name="failing-library",
                failing_test=True,
            )
            result = self.run_tool(failing, root / "work")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR: test:", result.stdout)

    def test_dependency_install_failure_is_returned_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            failing = write_library(
                root,
                name="missing-dependency-library",
                dependency="brainboxemb-package-that-does-not-exist-20261119==1.0",
            )
            result = self.run_tool(failing, root / "work")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR: install:", result.stdout)


if __name__ == "__main__":
    unittest.main()
