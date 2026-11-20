# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Current goal

Complete #12: externally test released `tool.py.lib.ci 0.1.4` at exact commit
`81461fa4b61c90b91b0427ce3e99a493c2dc2e78`.

The previous 0.1.3 concurrency release is externally accepted on main.

## Execution order

1. Pin the exact 0.1.4 release in the dependency manifest and reusable workflow.
2. Preserve the complete existing package/build/install/failure-path acceptance.
3. Test the released docs-only classifier directly from the pinned tool.
4. Inspect the released workflow contract for conservative PR-only skipping,
   rename-safe changed-path detection and conditional package validation.
5. Merge only after green PR acceptance.
6. Verify main acceptance.
7. Then prove the actual cheap path with a docs-only PR in a normal library
   consumer.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #12 Externally test tool.py.lib.ci 0.1.4 documentation-only CI | now | Required release acceptance before consumer adoption and real docs-only timing proof. |
| #3 Test tool.py.lib.ci 0.1.1 from another repository | effectively complete but still open | Historical acceptance is complete; later releases supersede its target. Close separately after historical review. |

## Boundary

This repository only observes the released behavior. It does not implement
changed-path classification, package-CI skipping or concurrency.
