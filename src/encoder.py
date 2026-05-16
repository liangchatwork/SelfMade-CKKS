# ============================================================
# selfmade-ckks
#
# File: encoder.py
#
# Description:
# This module implements a simplified educational encoder
# for CKKS-style homomorphic encryption.
#
# In real CKKS:
#
#     Complex Vector
#         ->
#     Canonical Embedding
#         ->
#     Polynomial Ring Element
#
# However, true CKKS encoding involves:
#
# - Canonical embedding
# - Sigma inverse
# - Coordinate projection
# - Scaling
# - Random rounding
#
# Reference:
# OpenMined CKKS Explained Part 2
# https://openmined.org/blog/ckks-explained-part-2-ckks-encoding-and-decoding/
#
# IMPORTANT:
# This file currently implements a simplified educational
# encoder, NOT the full canonical embedding yet.
#
# Current strategy:
#
#     vector[i] * scale
#         ->
#     polynomial coefficient[i]
#
# This gives us the correct high-level CKKS pipeline:
#
#     encode -> encrypt -> decrypt -> decode
#
# Future versions will replace this with full CKKS encoding.
# ============================================================

from he_math.polynomial import Polynomial


class CKKSEncoder:
    """
    Simplified Educational CKKS Encoder

    This encoder converts vectors into polynomial objects.

    Current version:
        Direct coefficient mapping with scaling.

    Future version:
        Real CKKS canonical embedding.
    """

    def __init__(self, scale=1.0):
        """
        Initialize encoder.

        Parameters
        ----------
        scale : float
            Scaling factor used in approximate arithmetic.

        Why scale matters:
            CKKS is approximate homomorphic encryption.
            Decimal values are multiplied by a large scale before
            encryption, then divided by the same scale after decryption.

        Example:
            1.234 * 2^20

        This makes small encryption noise relatively tiny after decoding.
        """

        self.scale = scale

    # ========================================================
    # Encoding
    # ========================================================

    def encode(self, vector):
        """
        Encode a vector into a polynomial.

        Current encoding strategy:
            vector[i] * scale -> coefficient[i]

        Example
        -------
        Input:
            [1.1, 2.2, 3.3]

        With scale = 2^20:
            [1.1 * 2^20, 2.2 * 2^20, 3.3 * 2^20]

        Output:
            Polynomial([...])

        Note:
            This is not full CKKS canonical embedding yet.
        """

        scaled_vector = [
            value * self.scale
            for value in vector
        ]

        return Polynomial(scaled_vector)

    # ========================================================
    # Decoding
    # ========================================================

    def decode(self, poly, length=None):
        """
        Decode polynomial back into vector.

        Current decoding strategy:
            coefficient[i] / scale -> vector[i]

        Parameters
        ----------
        poly : Polynomial
            Polynomial to decode.

        length : int, optional
            Original vector length.

        Why length matters:
            The ring degree may be larger than the original vector.
            We only return the original number of encoded values.
        """

        decoded_vector = [
            coeff / self.scale
            for coeff in poly.coefficients
        ]

        if length is not None:
            decoded_vector = decoded_vector[:length]

        return decoded_vector