# ============================================================
# selfmade-ckks
#
# File: scheme.py
#
# Description:
# This module implements the main educational CKKS-style
# encryption scheme.
#
# Mathematical reference:
#
# Public key:
#
#     pk = (b, a)
#     b  = -a * s + e
#
# Encryption:
#
#     c0 = m + b
#     c1 = a
#
# Decryption:
#
#     c0 + c1 * s
#       = m + (-a*s + e) + a*s
#       = m + e
#       ≈ m
#
# Reference:
# OpenMined CKKS Explained Part 3:
# https://openmined.org/blog/ckks-explained-part-3-encryption-and-decryption/
#
# IMPORTANT:
# Noise is NOT removed.
# Noise is required for RLWE security.
#
# Correctness comes from:
#
#     large scale Δ
#
# so that:
#
#     noise / Δ
#
# becomes small after decoding.
# ============================================================

from plaintext import Plaintext
from ciphertext import Ciphertext


class CKKSScheme:
    """
    Educational CKKS-style encryption scheme.

    This class owns the core cryptographic operations:

    - encrypt_plaintext()
    - decrypt_ciphertext()
    - add_ciphertexts()
    """

    def __init__(self, ring, public_key, secret_key):
        """
        Initialize scheme.

        Parameters
        ----------
        ring : PolynomialRing
            Ring used for polynomial arithmetic.

        public_key : PublicKey
            RLWE-style public key.

        secret_key : SecretKey
            RLWE-style secret key.
        """

        self.ring = ring
        self.public_key = public_key
        self.secret_key = secret_key

    # ========================================================
    # Encryption
    # ========================================================

    def encrypt_plaintext(self, plaintext):
        """
        Encrypt a Plaintext object into a Ciphertext object.

        Current educational encryption:

            c0 = m + b
            c1 = a

        where:

            public_key = (b, a)

        Since:

            b = -a*s + e

        the noise e is already inside b.

        We do NOT remove noise.
        """

        if not isinstance(plaintext, Plaintext):
            raise TypeError("encrypt_plaintext expects a Plaintext object.")

        m = plaintext.polynomial
        b = self.public_key.b
        a = self.public_key.a

        c0 = self.ring.add(m, b)
        c1 = a

        return Ciphertext(
            c0=c0,
            c1=c1,
            scale=plaintext.scale,
            length=plaintext.length,
        )

    # ========================================================
    # Decryption
    # ========================================================

    def decrypt_ciphertext(self, ciphertext):
        """
        Decrypt a Ciphertext object into a Plaintext object.

        Decryption formula:

            recovered = c0 + c1 * s

        Substitute encryption:

            c0 = m + (-a*s + e)
            c1 = a

        Then:

            recovered = m + (-a*s + e) + a*s
                      = m + e

        In CKKS, approximate recovery is expected.
        """

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("decrypt_ciphertext expects a Ciphertext object.")

        c0 = ciphertext.c0
        c1 = ciphertext.c1
        s = self.secret_key.polynomial

        c1_times_s = self.ring.multiply(c1, s)
        recovered = self.ring.add(c0, c1_times_s)

        return Plaintext(
            polynomial=recovered,
            scale=ciphertext.scale,
            length=ciphertext.length,
        )

    # ========================================================
    # Homomorphic Addition
    # ========================================================

    def add_ciphertexts(self, left, right):
        """
        Add two ciphertexts homomorphically.

        If:

            left  encrypts m1
            right encrypts m2

        then:

            left + right

        decrypts approximately to:

            m1 + m2

        Ciphertext addition:

            (c0, c1) + (d0, d1)
                =
            (c0 + d0, c1 + d1)
        """

        if not isinstance(left, Ciphertext):
            raise TypeError("left must be a Ciphertext object.")

        if not isinstance(right, Ciphertext):
            raise TypeError("right must be a Ciphertext object.")

        if left.scale != right.scale:
            raise ValueError(
                "Ciphertexts must have the same scale before addition."
            )

        if left.length != right.length:
            raise ValueError(
                "Ciphertexts must have the same vector length before addition."
            )

        new_c0 = self.ring.add(left.c0, right.c0)
        new_c1 = self.ring.add(left.c1, right.c1)

        return Ciphertext(
            c0=new_c0,
            c1=new_c1,
            scale=left.scale,
            length=left.length,
        )