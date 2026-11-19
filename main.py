# Entry point for the make.fun bounty "news-image-20261119".
#
# The artwork itself (entry.png, stored next to this file) is a newspaper
# front page that sums up Thursday 19 November 2026; generate_image.py in
# this repository is the program that drew it. All this entry point has to
# do is deliver that PNG to the grader's output directory, unchanged, on
# every run — so it is a plain file copy: no network, no third-party
# packages, byte-for-byte deterministic.

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_PNG = os.path.join(HERE, "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET_PNG = os.path.join(TARGET_DIR, "entry.png")


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    shutil.copyfile(SOURCE_PNG, TARGET_PNG)


if __name__ == "__main__":
    main()
