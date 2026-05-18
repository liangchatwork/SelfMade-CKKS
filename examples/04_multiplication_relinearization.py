# ============================================================
# selfmade-ckks
#
# Example: Multiplication, Scale Growth, and Relinearization
#
# This demo shows:
#
#   1. Ciphertext-Plaintext Multiplication
#   2. Ciphertext-Ciphertext Multiplication
#   3. Ciphertext Size Growth
#   4. Scale Growth
#   5. Relinearization
#   6. Educational operation / noise tracking
#
# Current status:
#
#   - Ciphertext-plaintext multiplication is implemented
#   - Ciphertext-ciphertext multiplication is implemented
#   - Relinearization is implemented
#   - Rescaling is NOT implemented yet
#
# Therefore, multiplication results keep scale Δ².
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

    # ========================================================
    # Ciphertext-Plaintext Multiplication
    # ========================================================

    a = [2]
    p = [3]

    enc_a = ctx.encrypt(a)

    enc_plain_product = ctx.multiply_plain(
        enc_a,
        p,
    )

    plain_product_result = ctx.decrypt(enc_plain_product)

    print("Ciphertext * Plaintext")
    print("Encrypted Input:      ", a)
    print("Plaintext Input:      ", p)
    print("Expected:             ", [6])
    print("Ciphertext Size:      ", enc_plain_product.size())
    print("Scale:                ", enc_plain_product.scale)
    print("Depth:                ", enc_plain_product.depth)
    print("History:              ", enc_plain_product.history)
    print("Decrypted:            ", plain_product_result)
    print()

    # ========================================================
    # Ciphertext-Ciphertext Multiplication
    # ========================================================

    b = [3]

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
    print("Depth:                ", enc_product.depth)
    print("History:              ", enc_product.history)
    print("Decrypted:            ", result_before_relin)
    print()

    print("After Relinearization")
    print("Ciphertext Size:      ", relin_product.size())
    print("Scale:                ", relin_product.scale)
    print("Depth:                ", relin_product.depth)
    print("History:              ", relin_product.history)
    print("Decrypted:            ", result_after_relin)
    print()

    print("Explanation:")
    print("Fresh ciphertext size is 2:        (c0, c1)")
    print("After multiplication, size is 3:   (c0, c1, c2)")
    print("After relinearization, size is 2:  (c0, c1)")
    print("Current scale was Δ = 2^20")
    print("After multiplication: Δ² = 2^40")
    print("Depth tracks multiplication depth.")
    print("History tracks educational operation flow.")
    print("Rescaling is not implemented yet.")


if __name__ == "__main__":
    main()