#!/usr/bin/env python3
"""Entry point for the news-image-20261119 submission.

The picture the competition judges is stored in this repository as
news.png. It was drawn by generate.py, a deterministic Pillow program
that lays out the front page from Thursday's headlines. This module
does the one thing the runner needs: it places an exact copy of that
picture at /output/entry.png.

There is no network access and no randomness anywhere in this path, so
running the program twice writes the same bytes twice.
"""
import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent
PICTURE = REPO / "news.png"


def target_folder() -> Path:
    """Where the runner expects the finished image."""
    preferred = Path("/output")
    if preferred.is_dir() or os.access("/", os.W_OK):
        return preferred
    return REPO / "output"


def run() -> Path:
    folder = target_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.png"
    shutil.copyfile(PICTURE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return target


if __name__ == "__main__":
    run()
