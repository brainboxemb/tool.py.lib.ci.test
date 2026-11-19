# Repository plan

This file contains only current unfinished work for `tool.py.lib.ci.test`.

## 1. Build the sample library

Add one minimal Python package with:

- package metadata;
- one declared runtime dependency;
- one module;
- passing unit tests;
- installed-package location proof.

## 2. Add the released-tool pin

After `tool.py.lib.ci` 0.1.0 is released:

- record its exact release commit in one dependency manifest;
- bootstrap/use only that exact revision.

Do not point test at moving `main`.

## 3. Prove the external reusable workflow

Call the pinned released reusable workflow from this repository.

Verify:

- wheel build;
- dependency installation;
- installed-wheel tests;
- exact repository behavior.

## 4. Add negative external cases

Prove:

- repository test failure;
- package build failure;
- dependency/install failure.

Run these through disposable synthetic inputs without making normal repository
CI intentionally fail.

## 5. Guard the architectural boundary

Prove the accepted public path uses:

- no SCons;
- no CAD-CI state;
- no `actions/cache`;
- no source-tree import leakage.

## 6. Mark 0.1.0 accepted

When all checks pass:

- document the accepted tool version/commit in README;
- remove completed plan sections;
- notify the first repository repository that the exact release is ready to pin.
