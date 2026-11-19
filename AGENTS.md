# Repository instructions

## Purpose

`tool.py.lib.ci.test` is the external test repository for one
exact released `tool.py.lib.ci` revision.

## Released-tool rule

Always pin an exact released tool commit.

Never follow moving `main`.

## Hard boundary

Do not implement or patch generic Python-library CI behavior here.

If test reveals missing generic behavior, fix it in
`tool.py.lib.ci`, release it, then update the exact pin here.

## Synthetic repository

Keep the repository deliberately small and domain-neutral.

Do not add Forge, SolidCraft, CAD or real application logic.

The synthetic package exists only to prove the public CI contract.

## Forbidden behavior

Test must fail if the released tool introduces:

- SCons;
- CAD-CI state;
- `actions/cache`;
- source-tree import leakage.

## Repository plan

Current unfinished work lives in `docs/plan.md`.

Remove completed sections after the accepted release is proven.

## Change quality

Use literal engineering language.

Each test check should identify the public contract it proves.

Keep one logical change per branch/PR and prefer squash merges.

## Repository plan source of truth

`docs/plan.md` is the current source of truth for unfinished repository work.

Keep it as a current snapshot:

- state the current goal and execution order;
- include every open issue in an issue assessment snapshot;
- give each open issue an explicit status such as `now`, `later`, `blocked`, `probably obsolete`, or `effectively complete but still open`;
- explain briefly why that status applies;
- identify dependencies or blockers between issues;
- keep the issue assessment current when issues are opened, closed, merged or superseded.

Issues contain detail and history. README and design/requirements documents describe stable purpose and behavior. The plan tells an agent what work is actually current and what should happen next.

