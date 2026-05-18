# ============================================================
# selfmade-ckks
#
# Example: Basic Homomorphic Operations
#
# This demo shows the currently supported basic operations:
#
#   1. Ciphertext + Ciphertext
#   2. Ciphertext + Plaintext
#   3. Ciphertext + Scalar
#   4. Ciphertext * Scalar
#
# In CKKS, plaintext vectors must be encoded before interacting
# with ciphertexts.
#
# Scalar operations are slightly different:
#
#   - scalar addition requires scaling the scalar by Δ
#   - scalar multiplication can directly multiply ciphertext
#     polynomial components and keep the same scale
#
# Current supported operations:
#
#   Enc(a) + Enc(b)      ≈ a + b
#   Enc(a) + Encode(p)  ≈ a + p
#   Enc(a) + k          ≈ a + k
#   Enc(a) * k          ≈ a * k
#
# Note:
# This is currently an educational CKKS implementation.
# Full CKKS encoding, ciphertext multiplication, plaintext
# multiplication, rescaling, and relinearization are still
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
    # Base encrypted vector
    # ========================================================

    a = [1, 2, 3]
    enc_a = ctx.encrypt(a)

    # ========================================================
    # 1. Ciphertext + Ciphertext
    # ========================================================

    b = [4, 5, 6]
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

    # ========================================================
    # 3. Ciphertext + Scalar
    # ========================================================

    scalar_add = 10

    enc_add_scalar = ctx.add_scalar(
        enc_a,
        scalar_add,
    )

    add_scalar_result = ctx.decrypt(enc_add_scalar)

    print("Ciphertext + Scalar")
    print("Encrypted: ", a)
    print("Scalar:    ", scalar_add)
    print("Expected:  ", [11, 12, 13])
    print("Decrypted: ", add_scalar_result)
    print()

    # ========================================================
    # 4. Ciphertext * Scalar
    # ========================================================

    scalar_mul = 2

    enc_mul_scalar = ctx.multiply_scalar(
        enc_a,
        scalar_mul,
    )

    mul_scalar_result = ctx.decrypt(enc_mul_scalar)

    print("Ciphertext * Scalar")
    print("Encrypted: ", a)
    print("Scalar:    ", scalar_mul)
    print("Expected:  ", [2, 4, 6])
    print("Decrypted: ", mul_scalar_result)


if __name__ == "__main__":
    main()