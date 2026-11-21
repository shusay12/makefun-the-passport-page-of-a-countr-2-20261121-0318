#!/usr/bin/env python3
"""Entry program for make.fun bounty
the-passport-page-of-a-countr-2-20261121-0318.

Writes /output/entry.png: one uncaptioned open passport spread for the
invented Republic of Talveria. The image is built by build_image.py
(Pillow, plus a generated portrait in portrait.png) and shipped in this
repository as entry.png; this program copies it byte for byte to the
grader's output directory. No network, no randomness, no dependencies
beyond the standard library.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_BYTES = 1_048_576


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    if not src.is_file():
        raise FileNotFoundError(f"missing {src}")
    if src.stat().st_size > MAX_BYTES:
        raise ValueError(f"{src} is {src.stat().st_size} bytes, over the "
                         f"{MAX_BYTES} byte cap")
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"wrote {dst} ({dst.stat().st_size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
