# ============================================================
# selfmade-ckks
#
# File: ring.py
#
# Description:
# This module implements polynomial ring arithmetic for CKKS.
#
# In CKKS, plaintexts and ciphertexts are not ordinary
# polynomials. They live inside a polynomial ring:
#
#     R = Z[X] / (X^N + 1)
#
# This means:
#
#     X^N = -1
#
# Therefore:
#
#     X^(N+1) = -X
#     X^(N+2) = -X²
#
# This type of reduction is called:
#
#     Negacyclic Reduction
#
# This module currently implements:
#
# - Ring initialization
# - Negacyclic polynomial reduction
# - Ring addition
# - Ring multiplication
#
# Future extensions:
#
# - Modular coefficient arithmetic
# - NTT acceleration
# - Ciphertext polynomial arithmetic
# - RNS decomposition
#
# ============================================================

from he_math.polynomial import Polynomial


class PolynomialRing:
    """
    Polynomial Ring Class

    Represents the ring:

        Z[X] / (X^N + 1)

    Parameters
    ----------
    degree : int
        Ring degree N.
    """

    def __init__(self, degree):
        """
        Initialize polynomial ring.

        Example:
            PolynomialRing(8)

        Represents:
            Z[X] / (X^8 + 1)
        """

        self.degree = degree

    # ========================================================
    # Negacyclic Reduction
    # ========================================================

    def reduce(self, poly):
        """
        Reduce a polynomial modulo (X^N + 1).

        Core CKKS relation:

            X^N = -1

        Example:
            X^9 -> -X

        This function folds higher-degree terms back into
        the ring.
        """

        coeffs = poly.coefficients[:]

        # Ensure enough space
        result = [0] * self.degree

        for power, coeff in enumerate(coeffs):

            # ------------------------------------------------
            # Terms already inside ring degree
            # ------------------------------------------------

            if power < self.degree:
                result[power] += coeff

            # ------------------------------------------------
            # Negacyclic reduction
            # ------------------------------------------------

            else:

                # Fold power back into ring
                reduced_power = power % self.degree

                # Number of wraps around X^N
                wrap_count = power // self.degree

                # Every wrap introduces a sign flip:
                #
                # X^N = -1
                #
                # Example:
                #   X^8  -> -1
                #   X^16 -> +1
                #
                sign = -1 if wrap_count % 2 == 1 else 1

                result[reduced_power] += sign * coeff

        return Polynomial(result)

    # ========================================================
    # Ring Addition
    # ========================================================

    def add(self, a, b):
        """
        Ring polynomial addition.

        Addition itself is ordinary polynomial addition,
        followed by ring reduction.
        """

        result = a + b

        return self.reduce(result)

    # ========================================================
    # Ring Subtraction
    # ========================================================

    def subtract(self, a, b):
        """
        Ring polynomial subtraction.
        """

        result = a - b

        return self.reduce(result)

    # ========================================================
    # Ring Multiplication
    # ========================================================

    def multiply(self, a, b):
        """
        Ring polynomial multiplication.

        Polynomial multiplication may increase degree,
        so reduction is required afterwards.
        """

        result = a * b

        return self.reduce(result)