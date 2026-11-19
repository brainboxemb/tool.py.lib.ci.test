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
