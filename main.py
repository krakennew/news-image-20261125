"""Ship the rendered poster into the harness output directory.

The poster itself is baked into entry.png at build time; this program
just moves those bytes to $MAKEFUN_OUTPUT_DIR/entry.png, chunk by chunk,
and reports what it did on stderr.
"""

import os
import sys

CHUNK = 65536


class PosterShipper:
    def __init__(self):
        self.here = os.path.dirname(os.path.abspath(__file__))
        self.source = os.path.join(self.here, "entry.png")
        self.dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        self.dest = os.path.join(self.dest_dir, "entry.png")
        self.moved = 0

    def load_and_drop(self):
        os.makedirs(self.dest_dir, exist_ok=True)
        with open(self.source, "rb") as incoming:
            with open(self.dest, "wb") as outgoing:
                while True:
                    piece = incoming.read(CHUNK)
                    if not piece:
                        break
                    outgoing.write(piece)
                    self.moved += len(piece)
        return self.moved

    def announce(self):
        sys.stderr.write(
            "shipped %d bytes: entry.png -> %s\n" % (self.moved, self.dest)
        )


def main():
    shipper = PosterShipper()
    shipper.load_and_drop()
    shipper.announce()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
