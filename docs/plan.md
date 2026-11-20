# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Current goal

Complete #10: externally test released `tool.py.lib.ci 0.1.3` at exact commit
`801480ad10b31d417ed7843f44608c795032c6d5`.

## Execution order

1. Pin the exact 0.1.3 release in the dependency manifest and reusable workflow.
2. Preserve the complete existing package/build/install/failure-path acceptance.
3. Add an external contract check for the released concurrency configuration.
4. Merge only after green PR acceptance.
5. Verify main acceptance before ordinary Python-library repositories adopt 0.1.3.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #10 Externally test tool.py.lib.ci 0.1.3 concurrency | now | Required release acceptance before consumer adoption. |
| #3 Test tool.py.lib.ci 0.1.1 from another repository | effectively complete but still open | Historical 0.1.1 acceptance was completed; the repository subsequently accepted 0.1.2. Close separately after historical review. |

## Boundary

This repository does not implement concurrency or package-CI behavior. It only
pins and observes the released tool contract.
