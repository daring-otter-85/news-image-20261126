#!/usr/bin/env python3
"""Hand the finished front page to the grader.

The poster for Thursday 26 November 2026 is already drawn and ships
in this repository as ``entry.png``. This program's only job is to
place that exact picture at ``/output/entry.png``, where the grader
looks for it.

It does no drawing, makes no network calls, and consults no clock:
every run writes the same bytes. While I am trying it out on my own
machine, ``MAKEFUN_OUTPUT_DIR`` points the picture somewhere else
instead of ``/output``, e.g. ``MAKEFUN_OUTPUT_DIR=out``.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
FILE_NAME = "entry.png"


def output_folder() -> Path:
    """The sandbox's /output, or the override from the environment."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def deliver() -> int:
    if not SOURCE.is_file():
        print(f"no bundled picture at {SOURCE}", file=sys.stderr)
        return 1

    target_dir = output_folder()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / FILE_NAME
    shutil.copyfile(SOURCE, target)
    print(f"delivered {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
