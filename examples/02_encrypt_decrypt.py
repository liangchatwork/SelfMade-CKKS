# ============================================================
# selfmade-ckks
#
# Example: Encryption and Decryption
#
# This demo shows:
#
#     vector
#       -> encode
#       -> encrypt
#       -> decrypt
#       -> decode
#
# Because CKKS is approximate HE, the decrypted result should
# be close to the original vector, not necessarily identical.
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

    message = [1.1, 2.2, 3.3]

    ciphertext = ctx.encrypt(message)
    result = ctx.decrypt(ciphertext)

    print("Original:  ", message)
    print("Ciphertext:", ciphertext)
    print("Decrypted: ", result)


if __name__ == "__main__":
    main()