# ============================================================
# selfmade-ckks
#
# File: ciphertext.py
#
# Description:
# This module implements the Ciphertext abstraction used in
# CKKS-style homomorphic encryption.
#
# In RLWE-based homomorphic encryption schemes such as CKKS,
# ciphertexts are NOT single values.
#
# Instead, they are typically tuples of polynomials:
#
#     (c0, c1)
#
# During decryption:
#
#     message ≈ c0 + c1 * s
#
# where:
#
#     s = secret key
#
# Reference:
# OpenMined CKKS Explained Part 3
# https://openmined.org/blog/ckks-explained-part-3-encryption-and-decryption/
#
# ============================================================


class Ciphertext:
    """
    Ciphertext Class

    Represents encrypted polynomial data.

    Current simplified structure:
        (c0, c1)

    Additional metadata:
        scale:
            CKKS scaling factor.

        length:
            Original vector length before encryption.

    Why length matters:
        The polynomial ring has fixed degree N.
        If the original input vector length is smaller than N,
        we should only decode the original number of slots.
    """

    def __init__(self, c0, c1, scale=1.0, length=None):
        """
        Initialize ciphertext.

        Parameters
        ----------
        c0 : Polynomial
            First ciphertext polynomial.

        c1 : Polynomial
            Second ciphertext polynomial.

        scale : float
            CKKS scaling factor.

        length : int, optional
            Original vector length before encoding/encryption.
        """

        self.c0 = c0
        self.c1 = c1
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
            f"Ciphertext("
            f"c0={self.c0}, "
            f"c1={self.c1}, "
            f"scale={self.scale}, "
            f"length={self.length}"
            f")"
        )

    def __str__(self):
        """
        Human-readable representation.
        """

        return (
            f"Ciphertext("
            f"c0={self.c0}, "
            f"c1={self.c1}"
            f")"
        )