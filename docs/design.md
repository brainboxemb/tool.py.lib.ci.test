# Python library CI external test design

## 1. Structure

Keep one permanent synthetic Python package in this repository.

Suggested layout:

```text
repository/
  pyproject.toml
  src/
  tests/
test/
  ...
dependencies.repos
```

Exact names may be adjusted during implementation.

## 2. Exact tool pin

Store the released `tool.py.lib.ci` commit in one small dependency manifest.

The GitHub workflow and local test harness must use that same exact
revision.

## 3. Real external workflow call

The main GitHub Actions path calls the released
`.github/workflows/reusable-ci.yml` from `tool.py.lib.ci`.

That proves workflow-call permissions, checkout semantics and package execution
from a real external repository.

## 4. Synthetic repository

The synthetic package has one declared runtime dependency and one simple test
suite.

A test records or asserts the imported package location so source-tree leakage
is detectable.

## 5. Negative cases

Failure semantics are tested with disposable copies/configurations of the
synthetic package.

Do not deliberately make the repository's ordinary required workflow fail.

The test harness should invoke the released tool's local/package-CI
entrypoint or equivalent public test surface for negative cases.

## 6. Forbidden-state checks

Test explicitly inspects the repository/workspace for forbidden generic
state:

- SCons state;
- `.cad-ci`;
- `.cache/cad-ci`.

The accepted workflow definition is also checked to ensure no
`actions/cache` action is present.

## 7. No generic implementation

Helpers in this repository may copy files, invoke the pinned released tool and
inspect outputs.

They must not implement build, install or test semantics themselves.


## 8. Documentation-only release acceptance

For a release that changes change-scope behavior, the external test repository:

1. pins the exact released tool commit;
2. imports the released classifier from the checked-out tool and tests its
   public observable classifications;
3. inspects the exact released reusable workflow for caller-event guards and
   conditional expensive steps;
4. continues to call the reusable workflow normally so the standard full
   package path remains externally proven.

The actual documentation-only event path is then proven separately by a real
pull request in a normal consumer repository.


## 9. 0.1.5 maintenance acceptance

The external repository imports `change_scope.py` from the exact pinned
release and directly tests comparison-base decisions. It also inspects the
released reusable workflow for the `change_scope` output wiring.

This complements, rather than replaces, the normal full package acceptance run.


## 10. Reusable release acceptance

The PR path first proves the exact released source contract without mutating
repository releases:

```text
released tool checkout
  -> inspect reusable-release.yml
  -> inspect template manifest/wrappers
  -> run normal package CI
```

After that PR is merged to `main`, an issue comment on this test repository
invokes the released reusable release workflow.

The repository-owned validator lives at
`release_case/validate_release.py`. It checks only the acceptance version and
exact checked-out target SHA and writes deterministic release notes. It does
not call GitHub APIs.

The resulting tag/release is a deliberate durable acceptance artifact for the
tool release version under test.
