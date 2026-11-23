#!/usr/bin/env python3
"""news-image-20261123 entry: write the day's news image to the output dir.

Copies the pre-built entry.png (a 6-panel summary of Monday 23 November
2026's world news) to $MAKEFUN_OUTPUT_DIR (default /output).
Standard library only; no network, no randomness: every run writes the
same bytes.
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # 1 MiB, the competition's image size cap


def verify_png(source: Path) -> str | None:
    """Return an error string if source is not a PNG within the size cap."""
    size = source.stat().st_size
    if size > MAX_BYTES:
        return f"{IMAGE_NAME} is {size} bytes, over the 1 MiB cap"
    with source.open("rb") as f:
        if f.read(len(PNG_MAGIC)) != PNG_MAGIC:
            return f"{IMAGE_NAME} is not a PNG (bad magic bytes)"
    return None


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        print(f"error: {IMAGE_NAME} not found next to main.py", file=sys.stderr)
        return 1
    problem = verify_png(source)
    if problem is not None:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / IMAGE_NAME)
    print(f"wrote {out_dir / IMAGE_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
