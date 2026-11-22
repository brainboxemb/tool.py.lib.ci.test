# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Accepted baseline

- currently accepted: `tool.py.lib.ci 0.1.5`;
- candidate under issue #17: `tool.py.lib.ci 0.2.0` @
  `8d18b3514180641e1756cc14efc4d8696c23e71b`.

## Current work

### #17 — accept reusable release workflow 0.2.0

1. pin package CI and local released-tool checks to 0.2.0;
2. verify released reusable release workflow and versioned templates;
3. merge only after the normal package-CI acceptance is green;
4. create one acceptance issue on `main`;
5. issue owner command `/release v0.2.0 <main-sha>`;
6. verify validator notes, exact tag/target, GitHub Release and issue comment;
7. close #17 only after that live publication succeeds;
8. only then allow Forge to replace its local generic release workflow.

## Open issue assessment — 2026-11-22

| Issue | Status | Assessment |
| --- | --- | --- |
| #17 Accept tool.py.lib.ci 0.2.0 reusable release workflow | **now** | PR contract acceptance followed by real issue-comment release. |
| #16 Align historical changelog with shared meta template and guidance | **later / docs-only** | No behavior impact. |

## Boundary

This repository observes the released behavior. It owns only the synthetic
package and repository-specific acceptance validator. Generic CI/release
implementation stays in `tool.py.lib.ci`.
