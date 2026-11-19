# Python library CI black-box acceptance design

## 1. Structure

Keep one permanent synthetic Python package in this repository.

Suggested layout:

```text
consumer/
  pyproject.toml
  src/
  tests/
acceptance/
  ...
dependencies.repos
```

Exact names may be adjusted during implementation.

## 2. Exact tool pin

Store the released `tool.py.lib.ci` commit in one small dependency manifest.

The GitHub workflow and local acceptance harness must use that same exact
revision.

## 3. Real external workflow call

The main GitHub Actions path calls the released
`.github/workflows/reusable-ci.yml` from `tool.py.lib.ci`.

That proves workflow-call permissions, checkout semantics and package execution
from a real external repository.

## 4. Synthetic consumer

The synthetic package has one declared runtime dependency and one simple test
suite.

A test records or asserts the imported package location so source-tree leakage
is detectable.

## 5. Negative cases

Failure semantics are tested with disposable copies/configurations of the
synthetic package.

Do not deliberately make the repository's ordinary required workflow fail.

The acceptance harness should invoke the released tool's local/package-CI
entrypoint or equivalent public test surface for negative cases.

## 6. Forbidden-state checks

Acceptance explicitly inspects the repository/workspace for forbidden generic
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
