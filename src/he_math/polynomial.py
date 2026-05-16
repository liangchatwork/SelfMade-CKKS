# ============================================================
# selfmade-ckks
#
# File: polynomial.py
#
# Description:
# This module implements a basic Polynomial class that will
# serve as one of the mathematical foundations of CKKS.
#
# In homomorphic encryption schemes such as CKKS, plaintexts
# and ciphertexts are represented as polynomials inside
# special polynomial rings.
#
# Example polynomial:
#
#     [1, 2, 3]
#
# Represents:
#
#     1 + 2x + 3x²
#
# This file currently implements:
#
# - Polynomial initialization
# - Pretty printing
# - Addition
# - Subtraction
# - Multiplication
# - Scalar multiplication
#
# Future extensions:
#
# - Polynomial modular reduction
# - Negacyclic reduction
# - Ring arithmetic
# - NTT acceleration
# - Modular arithmetic
#
# ============================================================


class Polynomial:
    """
    Basic Polynomial Class

    A polynomial is represented by a list of coefficients.

    Example:
        [1, 2, 3]

    Represents:
        1 + 2x + 3x²
    """

    def __init__(self, coefficients):
        """
        Initialize a polynomial.

        Parameters
        ----------
        coefficients : list
            List of polynomial coefficients.

        Example
        -------
        Polynomial([1, 2, 3])

        Represents:
            1 + 2x + 3x²
        """

        # Remove trailing zeros for cleaner representation
        self.coefficients = self._trim(coefficients)

    # ========================================================
    # Internal Utilities
    # ========================================================

    def _trim(self, coeffs):
        """
        Remove unnecessary trailing zeros.

        Example:
            [1, 2, 0, 0] -> [1, 2]
        """

        coeffs = coeffs[:]

        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()

        return coeffs

    # ========================================================
    # String Representation
    # ========================================================

    def __repr__(self):
        """
        Developer-friendly representation.
        """

        return f"Polynomial({self.coefficients})"

    def __str__(self):
        """
        Human-readable polynomial format.

        Example:
            1 + 2x + 3x²
        """

        terms = []

        for power, coeff in enumerate(self.coefficients):

            # Skip zero coefficients
            if coeff == 0:
                continue

            # Constant term
            if power == 0:
                terms.append(f"{coeff}")

            # x term
            elif power == 1:
                terms.append(f"{coeff}x")

            # Higher-order terms
            else:
                terms.append(f"{coeff}x^{power}")

        # Handle zero polynomial
        if not terms:
            return "0"

        return " + ".join(terms)

    # ========================================================
    # Polynomial Addition
    # ========================================================

    def __add__(self, other):
        """
        Polynomial addition.

        Example:
            (1 + 2x) + (3 + 4x)

        Result:
            4 + 6x
        """

        max_len = max(
            len(self.coefficients),
            len(other.coefficients)
        )

        result = [0] * max_len

        for i in range(max_len):

            a = (
                self.coefficients[i]
                if i < len(self.coefficients)
                else 0
            )

            b = (
                other.coefficients[i]
                if i < len(other.coefficients)
                else 0
            )

            result[i] = a + b

        return Polynomial(result)

    # ========================================================
    # Polynomial Subtraction
    # ========================================================

    def __sub__(self, other):
        """
        Polynomial subtraction.

        Example:
            (5 + 3x) - (2 + x)

        Result:
            3 + 2x
        """

        max_len = max(
            len(self.coefficients),
            len(other.coefficients)
        )

        result = [0] * max_len

        for i in range(max_len):

            a = (
                self.coefficients[i]
                if i < len(self.coefficients)
                else 0
            )

            b = (
                other.coefficients[i]
                if i < len(other.coefficients)
                else 0
            )

            result[i] = a - b

        return Polynomial(result)

    # ========================================================
    # Polynomial Multiplication
    # ========================================================

    def __mul__(self, other):
        """
        Polynomial multiplication.

        This currently uses naive convolution.

        Example:
            (1 + 2x) * (3 + 4x)

        Result:
            3 + 10x + 8x²
        """

        # ----------------------------------------------------
        # Scalar multiplication
        # ----------------------------------------------------

        if isinstance(other, (int, float)):

            result = [
                coeff * other
                for coeff in self.coefficients
            ]

            return Polynomial(result)

        # ----------------------------------------------------
        # Polynomial multiplication
        # ----------------------------------------------------

        result_degree = (
            len(self.coefficients)
            + len(other.coefficients)
            - 1
        )

        result = [0] * result_degree

        for i, a in enumerate(self.coefficients):

            for j, b in enumerate(other.coefficients):

                result[i + j] += a * b

        return Polynomial(result)

    # ========================================================
    # Right Scalar Multiplication
    # ========================================================

    def __rmul__(self, other):
        """
        Enables:
            3 * polynomial
        """

        return self.__mul__(other)

    # ========================================================
    # Polynomial Equality
    # ========================================================

    def __eq__(self, other):
        """
        Check polynomial equality.
        """

        return (
            self.coefficients
            == other.coefficients
        )