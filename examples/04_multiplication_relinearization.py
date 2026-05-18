# ============================================================
# selfmade-ckks
#
# Example: Ciphertext Multiplication
#
# This demo shows the first CKKS multiplication-related step:
#
#   Ciphertext * Ciphertext
#
# In CKKS, multiplying two ciphertexts causes two important
# effects:
#
#   1. Ciphertext size grows
#        (c0, c1) -> (c0, c1, c2)
#
#   2. Scale grows
#        Δ -> Δ²
#
# This is why CKKS later needs:
#
#   - Relinearization
#   - Rescaling
#
# Current status:
#
#   - Ciphertext multiplication is implemented
#   - Relinearization is NOT implemented yet
#   - Rescaling is NOT implemented yet
#
# Therefore, this example focuses on observing ciphertext size
# growth and scale growth.
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
    # Ciphertext * Ciphertext
    # ========================================================
    #
    # We use single-value inputs here.
    #
    # Reason:
    # The current encoder is still a simplified coefficient
    # mapping encoder, not full CKKS SIMD slot encoding.
    #
    # Vector multiplication will require full CKKS encoding
    # or a clearer polynomial-slot interpretation.
    # ========================================================

    a = [2]
    b = [3]

    enc_a = ctx.encrypt(a)
    enc_b = ctx.encrypt(b)

    enc_product = ctx.multiply(
        enc_a,
        enc_b,
    )

    result_before_relin = ctx.decrypt(enc_product)

    relin_product = ctx.relinearize(enc_product)

    result_after_relin = ctx.decrypt(relin_product)

    print("Ciphertext * Ciphertext")
    print("Input A:              ", a)
    print("Input B:              ", b)
    print("Expected:             ", [6])
    print()

    print("Before Relinearization")
    print("Ciphertext Size:      ", enc_product.size())
    print("Scale:                ", enc_product.scale)
    print("Decrypted:            ", result_before_relin)
    print()

    print("After Relinearization")
    print("Ciphertext Size:      ", relin_product.size())
    print("Scale:                ", relin_product.scale)
    print("Decrypted:            ", result_after_relin)
    print()

    print("Explanation:")
    print("Fresh ciphertext size is 2:        (c0, c1)")
    print("After multiplication, size is 3:   (c0, c1, c2)")
    print("After relinearization, size is 2:  (c0, c1)")
    print("Current scale was Δ = 2^20")
    print("After multiplication: Δ² = 2^40")
    print("Rescaling is not implemented yet.")

if __name__ == "__main__":
    main()