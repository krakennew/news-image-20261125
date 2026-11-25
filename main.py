"""Entry program (Python 3.13, standard library only): copy the bundled
front-page image to /output/entry.png. The image is drawn by
draw_poster.py; this program only copies it, so both grader runs write
identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
print(f"copied entry.png to {OUT / 'entry.png'}")
