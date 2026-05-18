# ============================================================
# selfmade-ckks
#
# Example: Homomorphic Operations
#
# This demo shows three basic CKKS-style homomorphic operations:
#
#   1. Ciphertext + Ciphertext
#   2. Ciphertext + Plaintext
#
# In CKKS, plaintext values must also be encoded before they
# can interact with ciphertexts.
#
# Current supported operations:
#
#   Enc(a) + Enc(b)      ≈ a + b
#   Enc(a) + Encode(p)  ≈ a + p
#
# Note:
# This is currently an educational CKKS implementation.
# Full CKKS encoding, rescaling, and relinearization are still
# planned future work.
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

    # ========================================================
    # 1. Ciphertext + Ciphertext
    # ========================================================

    a = [1, 2, 3]
    b = [4, 5, 6]

    enc_a = ctx.encrypt(a)
    enc_b = ctx.encrypt(b)

    enc_sum = ctx.add(enc_a, enc_b)

    sum_result = ctx.decrypt(enc_sum)

    print("Ciphertext + Ciphertext")
    print("Input A:   ", a)
    print("Input B:   ", b)
    print("Expected:  ", [5, 7, 9])
    print("Decrypted: ", sum_result)
    print()

    # ========================================================
    # 2. Ciphertext + Plaintext
    # ========================================================

    plain_add = [10, 20, 30]

    enc_add_plain = ctx.add_plain(
        enc_a,
        plain_add,
    )

    add_plain_result = ctx.decrypt(enc_add_plain)

    print("Ciphertext + Plaintext")
    print("Encrypted: ", a)
    print("Plaintext: ", plain_add)
    print("Expected:  ", [11, 22, 33])
    print("Decrypted: ", add_plain_result)
    print()


if __name__ == "__main__":
    main()