# Repository plan

This file contains only current unfinished work for `tool.py.lib.ci.test`.

## 1. Test tool.py.lib.ci 0.1.2 — #6

Pin exact release commit:

`9045367540102ba2208c517e45a52ddad4bb60ea`

Run the released reusable workflow and prove:

- wheel build;
- clean install;
- declared dependency installation;
- installed-wheel imports;
- installed console script available through PATH;
- build/test/install failures remain visible;
- no SCons, CAD-CI state or `actions/cache`.

After the external test passes:

1. merge this change;
2. close #6;
3. update library repositories to the exact tested release;
4. remove this section.
