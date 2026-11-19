#!/usr/bin/env python3
"""make.fun entry for 'Sum up 19 November's world news in one image' (news-image-20261119).

Simplest valid program, as the brief allows: it copies the image the
repository holds (news.png, generated deterministically by generate.py)
to /output/entry.png. No network, no randomness — repeated runs write
exactly the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")
OUT_DIR = "/output" if os.path.isdir("/output") or os.access("/", os.W_OK) else os.path.join(HERE, "output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
