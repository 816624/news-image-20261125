#!/usr/bin/env python3
"""Write the 25 November 2026 world-news summary image.

The finished image lives in this repository as entry.png.b64, a base64
encoding of the PNG. This program decodes it and writes the result to
``entry.png`` inside the output directory (``$MAKEFUN_OUTPUT_DIR`` when
set, otherwise ``/output``). It uses only the Python standard library,
touches no network, and writes byte-identical output on every run.
"""

import base64
import os
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
SOURCE_FILE = REPO_DIR / "entry.png.b64"


def build_image() -> bytes:
    """Decode the stored image. Raises if the payload is not valid base64."""
    text = SOURCE_FILE.read_text(encoding="ascii").strip()
    return base64.b64decode(text, validate=True)


def main() -> int:
    try:
        image_bytes = build_image()
    except Exception as exc:  # corrupt payload: fail loudly, write nothing
        print(f"error: cannot decode entry.png.b64: {exc}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(image_bytes)
    print(f"wrote {target} ({len(image_bytes)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
