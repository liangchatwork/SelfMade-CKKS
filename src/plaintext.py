# ============================================================
# selfmade-ckks
#
# File: plaintext.py
#
# Description:
# This module implements the Plaintext abstraction used in
# CKKS-style homomorphic encryption.
#
# In homomorphic encryption, a plaintext is typically:
#
#     User Data
#         ->
#     Encoded Polynomial
#
# but NOT encrypted yet.
#
# Therefore:
#
#     Plaintext != Ciphertext
#
# A Plaintext object usually stores:
#
# - Encoded polynomial
# - Scale information
# - Metadata
#
# Reference:
# OpenMined CKKS Explained Part 2
# https://openmined.org/blog/ckks-explained-part-2-ckks-encoding-and-decoding/
#
# ============================================================


class Plaintext:
    """
    Plaintext Class

    Represents an encoded polynomial before encryption.

    Additional metadata:
        length:
            Original vector length before encoding.

    Why length matters:
        CKKS works inside a fixed-size polynomial ring.
        If the ring degree is 8 but the input vector length is 3,
        decoding the whole polynomial may return extra coefficients.
    """

    def __init__(self, polynomial, scale=1.0, length=None):
        """
        Initialize plaintext.

        Parameters
        ----------
        polynomial : Polynomial
            Encoded polynomial.

        scale : float
            CKKS scaling factor.

        length : int, optional
            Original vector length before encoding.

        In real CKKS:
            scale is extremely important because CKKS uses
            approximate arithmetic.
        """

        self.polynomial = polynomial
        self.scale = scale
        self.length = length

    # ========================================================
    # String Representation
    # ========================================================

    def __repr__(self):
        """
        Developer-friendly representation.
        """

        return (
            f"Plaintext("
            f"polynomial={self.polynomial}, "
            f"scale={self.scale}, "
            f"length={self.length}"
            f")"
        )

    def __str__(self):
        """
        Human-readable representation.
        """

        return (
            f"Plaintext("
            f"{self.polynomial}"
            f")"
        )