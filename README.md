# tool.py.lib.ci.test

Permanent black-box acceptance repository for released `tool.py.lib.ci`
revisions.

This repository proves the public Python-library CI contract from outside the
tool repository.

## Purpose

A `tool.py.lib.ci` release is not consumer-ready merely because its own tests
pass.

This repository pins one exact released tool revision and uses it as a real
external consumer would.

## Boundary

Do not develop generic CI behavior here.

If acceptance exposes a generic problem:

1. return to `tool.py.lib.ci`;
2. fix and release a new exact revision;
3. update the pin here;
4. rerun acceptance.

## Acceptance target

The synthetic consumer must prove:

- external reusable-workflow invocation;
- exact consumer source checkout;
- exactly one wheel built;
- clean wheel installation;
- declared dependency installation;
- tests run against the installed wheel;
- pass/fail propagation;
- no SCons;
- no CAD-CI;
- no GitHub Actions cache.

## Documentation

- `docs/requirements.md` — black-box acceptance contract.
- `docs/design.md` — acceptance-repository structure.
- `docs/plan.md` — current unfinished work only.
