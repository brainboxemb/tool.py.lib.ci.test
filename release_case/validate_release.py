"""Acceptance validator for the released generic release workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-sha", required=True)
    parser.add_argument("--notes-out", type=Path, required=True)
    args = parser.parse_args()

    if args.version != "0.2.1":
        raise SystemExit(f"unexpected acceptance release version: {args.version}")

    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if args.target_sha != head:
        raise SystemExit(
            f"validator target mismatch: requested {args.target_sha}, checkout {head}"
        )

    args.notes_out.write_text(
        "tool.py.lib.ci 0.2.1 external reusable-release acceptance\n",
        encoding="utf-8",
    )
    print(f"validated external release {args.version} at {args.target_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
