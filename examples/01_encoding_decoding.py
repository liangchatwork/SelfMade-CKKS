# ============================================================
# selfmade-ckks
#
# Example: Encoding and Decoding
#
# This demo shows the first CKKS pipeline component:
#
#     vector
#       -> encode
#       -> plaintext polynomial
#       -> decode
#       -> approximate vector
#
# ============================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))

from context import CKKSContext


def main():
    ctx = CKKSContext(
        degree=8,
        modulus=2**40,
        scale=2**20,
        noise_std=3.2,
    )

    vector = [1.1, 2.2, 3.3]

    plaintext = ctx.encode(vector)
    decoded = ctx.decode(plaintext)

    print("Original:  ", vector)
    print("Plaintext: ", plaintext)
    print("Decoded:   ", decoded)


if __name__ == "__main__":
    main()