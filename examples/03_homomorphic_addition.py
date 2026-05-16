# ============================================================
# selfmade-ckks
#
# Example: Homomorphic Addition
#
# This demo shows the first complete HE-style pipeline:
#
#     vector
#       -> encode
#       -> encrypt
#       -> homomorphic add
#       -> decrypt
#       -> decode
#
# Expected result:
#
#     [1, 2, 3] + [4, 5, 6]
#       =
#     [5, 7, 9]
#
# Note:
# This is currently an educational CKKS-style prototype.
# The encoder and encryption are not production-secure yet.
# ============================================================

import sys
from pathlib import Path

# Allow example file to import from src/
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

    a = [1, 2, 3]
    b = [4, 5, 6]

    enc_a = ctx.encrypt(a)
    enc_b = ctx.encrypt(b)

    enc_sum = ctx.add(enc_a, enc_b)

    result = ctx.decrypt(enc_sum)

    print("Input A:   ", a)
    print("Input B:   ", b)
    print("Decrypted: ", result)


if __name__ == "__main__":
    main()