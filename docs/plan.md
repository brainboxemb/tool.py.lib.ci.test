# Repository plan

This file is the current source of truth for unfinished work in
`tool.py.lib.ci.test`.

## Accepted baseline

- live reusable-release 0.2.0 acceptance is complete;
- candidate under issue #19: `tool.py.lib.ci 0.2.1` @
  `58ead6897a4ac8cafef22a3c1f834491bf61568d`.

## Current work

### #19 — accept annotated release tags in 0.2.1

1. pin package CI, release wrapper and released-tool checks to 0.2.1;
2. keep normal package-CI acceptance green;
3. merge the exact acceptance tree to main;
4. issue owner command `/release v0.2.1 <main-sha>`;
5. verify `refs/tags/v0.2.1` has object type `tag`;
6. resolve the annotated tag object to the exact acceptance main commit;
7. verify validator notes and issue reporting;
8. close #19 only after live publication succeeds;
9. then allow Forge to adopt the released generic publisher.

## Open issue assessment — 2026-11-22

| Issue | Status | Assessment |
| --- | --- | --- |
| #19 Accept tool.py.lib.ci 0.2.1 annotated release tags | **now** | PR acceptance followed by live annotated-tag release. |
| #16 Align historical changelog with shared meta template and guidance | **later / docs-only** | No behavior impact. |

## Boundary

This repository observes released behavior only. Generic tag/release code stays
in `tool.py.lib.ci`.
