# Python library CI external test requirements

This repository validates one exact released `tool.py.lib.ci` revision from
outside the tool repository.

## 1. Exact released pin

Test uses one exact released tool commit.

Moving branches are not valid test dependencies.

## 2. External reusable workflow

The repository must call the released public reusable workflow exactly as a
normal repository repository would.

Test fails if the public workflow cannot be called externally.

## 3. Synthetic Python library

Provide one small Python package with:

- normal package metadata;
- one runtime dependency;
- one importable module;
- unit tests;
- one value/version check proving which installed package is imported.

The package contains no CAD/domain behavior.

## 4. Wheel proof

The released tool must build exactly one wheel for the synthetic package.

Test verifies the reported/generated wheel belongs to the synthetic
repository.

## 5. Clean installation proof

The workflow must install the wheel and its declared dependency in a clean
environment.

Test must not rely on the dependency being preinstalled globally.

## 6. Installed-package import proof

Tests must prove imports resolve from the installed wheel environment, not from
the repository source tree.

## 7. Passing tests

The normal synthetic package test suite passes through the released public
workflow.

## 8. Failure propagation

Test must also prove, without making normal main CI intentionally red,
that the released tool reports:

- repository test failure as failure;
- package build failure as failure;
- package/dependency install failure as failure.

These failure cases may be exercised by an test harness against
disposable synthetic copies.

## 9. No SCons

Test fails if the released public path invokes SCons or creates SCons
state.

## 10. No CAD-CI

Test fails if it creates or consumes:

- `.cad-ci`;
- `.cache/cad-ci`;
- CAD-CI item/build semantics.

## 11. No GitHub Actions cache

The released public workflow must contain no `actions/cache` restore/save
steps in the initial accepted version.

## 12. Repository-ready rule

A released `tool.py.lib.ci` revision is ready to use only when all external
test checks pass here.


## 13. Superseded-run concurrency proof

When the released tool adds central superseded-run cancellation, the external
test must inspect the exact released workflow and prove that:

- concurrency is enabled;
- `cancel-in-progress` is true;
- the group includes caller repository;
- the group includes caller workflow;
- the group distinguishes PR/branch context.

The test repository does not implement its own replacement concurrency policy.


## 14. Documentation-only CI external proof

When the released tool adds a documentation-only cheap path, external acceptance
must prove both the classifier and public workflow contract from the exact
released revision.

The classifier must accept only a non-empty path set entirely below `docs/`.
Empty, mixed and non-doc path sets must select full package CI.

The released workflow must keep the docs-only optimization restricted to normal
pull requests without an explicit source override, use rename-safe changed-path
detection, skip only the expensive Python setup/package-validation steps, and
leave unsafe or unknown cases on the full path.

A separate real consumer PR must later prove the actual GitHub Actions cheap
path; this repository does not fabricate caller event state.


## 15. Push and workflow-output acceptance

For the released 0.1.5 maintenance contract, external acceptance must prove:

- safe normal push comparison uses the event `before` commit;
- forced, zero/invalid-before and explicit source override contexts fail safe;
- the reusable workflow exports `change_scope` as the exact classifier result.

The test repository does not implement consumer release policy with that output.
