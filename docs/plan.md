# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Current goal

Complete #14: externally accept released `tool.py.lib.ci 0.1.5` at exact
commit `d189d0718659ca3927f1dddbe373c1c788b11b6c`.

This is one maintenance-release acceptance batch covering the complete released
change-scope contract: pull requests, safe pushes, fail-safe push fallbacks and
the reusable `change_scope` output.

## Execution order

1. Pin exact 0.1.5 in the dependency manifest and reusable workflow.
2. Preserve all existing package/build/install/failure-path acceptance.
3. Import the released classifier and prove:
   - docs-only path classification;
   - safe pull-request base selection;
   - safe non-forced push `before` selection;
   - forced, zero/invalid and overridden contexts fail safe to full.
4. Inspect the exact released workflow and prove:
   - rename-disabled NUL-delimited Git diff;
   - docs-only package-validation skip;
   - exported `change_scope` output.
5. Merge only after green PR acceptance.
6. Verify main acceptance once.
7. Then consumers may adopt 0.1.5.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #14 Accept tool.py.lib.ci 0.1.5 maintenance release | now | Current external acceptance batch for the complete 0.1.5 maintenance release. |

No other open issues remain at this snapshot.

## Boundary

This repository only observes the released behavior. It does not implement
changed-path classification, package-CI skipping, concurrency or consumer
release policy.
