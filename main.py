# Entry for make.fun's "Sum up 19 November's world news in one image" bounty.
# The image (entry.png, beside this file) is a newspaper front page summing up
# Thursday 19 November 2026; it was rendered by generate_image.py in this repo.
# This program copies it to the output directory, byte for byte, every run:
# no network, standard library only, deterministic.
import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUTPUT_DIR, "entry.png"))
