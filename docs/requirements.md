# Python library CI black-box acceptance requirements

This repository validates one exact released `tool.py.lib.ci` revision from
outside the tool repository.

## 1. Exact released pin

Acceptance uses one exact released tool commit.

Moving branches are not valid acceptance dependencies.

## 2. External reusable workflow

The repository must call the released public reusable workflow exactly as a
normal consumer repository would.

Acceptance fails if the public workflow cannot be called externally.

## 3. Synthetic Python library

Provide one small Python package with:

- normal package metadata;
- one runtime dependency;
- one importable module;
- unit tests;
- one value/version check proving which installed package is imported.

The package contains no CAD/domain behavior.

## 4. Wheel proof

The released tool must build exactly one wheel for the synthetic package.

Acceptance verifies the reported/generated wheel belongs to the synthetic
consumer.

## 5. Clean installation proof

The workflow must install the wheel and its declared dependency in a clean
environment.

Acceptance must not rely on the dependency being preinstalled globally.

## 6. Installed-package import proof

Tests must prove imports resolve from the installed wheel environment, not from
the repository source tree.

## 7. Passing tests

The normal synthetic package test suite passes through the released public
workflow.

## 8. Failure propagation

Acceptance must also prove, without making normal main CI intentionally red,
that the released tool reports:

- consumer test failure as failure;
- package build failure as failure;
- package/dependency install failure as failure.

These failure cases may be exercised by an acceptance harness against
disposable synthetic copies.

## 9. No SCons

Acceptance fails if the released public path invokes SCons or creates SCons
state.

## 10. No CAD-CI

Acceptance fails if it creates or consumes:

- `.cad-ci`;
- `.cache/cad-ci`;
- CAD-CI item/build semantics.

## 11. No GitHub Actions cache

The released public workflow must contain no `actions/cache` restore/save
steps in the initial accepted version.

## 12. Consumer-ready rule

A released `tool.py.lib.ci` revision is consumer-ready only when all black-box
acceptance checks pass here.
