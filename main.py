#!/usr/bin/env python3
"""news-image-20261126 entrypoint.

Copies the front-page image for Thursday 26 November 2026 into the
grading directory, byte for byte, and refuses to finish if the copy
does not match the reviewed file. Nothing is drawn or changed here;
the image itself is the entry.
"""

from __future__ import annotations

import hashlib
import pathlib
import shutil
import sys

IMAGE_NAME = "entry.png"
OUTPUT_DIR = pathlib.Path("/output")
EXPECTED_SHA256 = "bdf8dd56169d49b307432d661a3e352bae0e7e149c07ca7476be999bba85c027"


def find_image() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve().parent
    candidate = here / IMAGE_NAME
    if not candidate.is_file():
        raise SystemExit(f"missing {IMAGE_NAME} beside main.py")
    return candidate


def fingerprint(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_size(path: pathlib.Path) -> None:
    expected_bytes = 663730
    actual = path.stat().st_size
    if actual != expected_bytes:
        raise SystemExit(f"unexpected size {actual} bytes (want {expected_bytes})")


def main() -> int:
    source = find_image()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / IMAGE_NAME
    shutil.copyfile(source, target)
    check_size(target)
    if fingerprint(target) != EXPECTED_SHA256:
        raise SystemExit("copied image does not match the reviewed file")
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
