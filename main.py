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

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
FILE_NAME = "entry.png"


def output_folder() -> Path:
    """The sandbox's /output, or the override from the environment."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def png_size(path: Path) -> tuple[int, int] | None:
    """Width and height from the PNG IHDR header, or None if not a PNG."""
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def deliver() -> int:
    if not SOURCE.is_file():
        print(f"no bundled picture at {SOURCE}", file=sys.stderr)
        return 1

    target_dir = output_folder()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / FILE_NAME
    shutil.copyfile(SOURCE, target)

    # Prove the delivery landed intact: same digest, readable PNG header.
    src_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    out_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if src_hash != out_hash:
        print(f"delivery mismatch: {target} differs from {SOURCE}", file=sys.stderr)
        return 1
    size = png_size(target)
    dims = f"{size[0]}x{size[1]}" if size else "unknown size"
    print(f"delivered {target} ({target.stat().st_size} bytes, {dims}, sha256 {out_hash[:12]}…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
