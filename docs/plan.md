# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Current status

The repository has externally tested:

- `tool.py.lib.ci` 0.1.2
- commit `9045367540102ba2208c517e45a52ddad4bb60ea`

The test covers wheel build, clean installation, declared dependencies,
installed-wheel imports, installed console scripts on PATH, failure
propagation, and the absence of SCons/CAD-CI/`actions/cache`.

There is no active functional test change at this snapshot. The repository
should remain stable until a new `tool.py.lib.ci` release needs testing.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #7 Make docs/plan.md the repository work source of truth | now | Repository-process housekeeping. Close after this plan/AGENTS update is merged. |
| #3 Test tool.py.lib.ci 0.1.1 from another repository | effectively complete but still open | PR #4 merged and main external test passed. The repository has since also tested 0.1.2. Close this old 0.1.1 tracking issue after confirming no separate historical requirement remains. |

## Next action

Wait for a new released `tool.py.lib.ci` revision. For each future release:

1. pin the exact release commit;
2. add only the external check required by the changed public contract;
3. run the complete existing test suite;
4. merge only after green external test;
5. then allow library repositories to adopt that exact revision.
