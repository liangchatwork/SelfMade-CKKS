# ============================================================
# selfmade-ckks
#
# File: keys.py
#
# Description:
# This module implements educational RLWE-style key generation
# for the Selfmade-CKKS project.
#
# ============================================================
#
# WHY DOES CKKS NEED NOISE?
#
# In RLWE / CKKS-based homomorphic encryption,
# security fundamentally relies on adding small random errors.
#
# Without noise:
#
#     attackers may solve equations directly
#     and recover the secret key.
#
# Therefore:
#
#     noise IS NOT OPTIONAL.
#
# It is one of the core foundations of lattice cryptography.
#
# ============================================================
#
# RLWE STRUCTURE
#
# We work inside the polynomial ring:
#
#     R_q = Z_q[X] / (X^N + 1)
#
# Public key structure:
#
#     pk = (b, a)
#
# where:
#
#     b = -a*s + e
#
# and:
#
#     s = secret key polynomial
#     e = small random error (noise)
#
# ============================================================
#
# IMPORTANT CONCEPT
#
# The error/noise polynomial should be:
#
#     - random
#     - small
#     - difficult to reverse
#
# In real CKKS / RLWE systems:
#
#     e is usually sampled from
#     a Discrete Gaussian Distribution.
#
# Reference:
# OpenMined CKKS Explained Part 3:
# https://openmined.org/blog/ckks-explained-part-3-encryption-and-decryption/
#
# ============================================================

import random

from he_math.polynomial import Polynomial


class SecretKey:
    """
    Secret Key Object

    In RLWE-based cryptography,
    the secret key is usually a "small polynomial".

    Many HE systems use:
        {-1, 0, 1}

    or sparse ternary distributions.
    """

    def __init__(self, polynomial):

        self.polynomial = polynomial

    def __repr__(self):

        return f"SecretKey({self.polynomial})"


class PublicKey:
    """
    Public Key Object

    Represents:

        pk = (b, a)

    where:

        b = -a*s + e
    """

    def __init__(self, b, a):

        self.b = b
        self.a = a

    def __repr__(self):

        return (
            f"PublicKey("
            f"b={self.b}, "
            f"a={self.a}"
            f")"
        )
    
class RelinearizationKey:
    """
    Relinearization Key

    After ciphertext multiplication, ciphertext size grows:

        (c0, c1) -> (c0, c1, c2)

    Decryption becomes:

        c0 + c1*s + c2*s²

    Relinearization converts the c2*s² term back into a form
    that only depends on:

        1 and s

    This educational version uses gadget/base decomposition.

    Instead of encrypting only s² once, we generate keys for:

        B^0 * s²
        B^1 * s²
        B^2 * s²
        ...

    where B is the decomposition base.
    """

    def __init__(self, entries, base, levels):
        self.entries = entries
        self.base = base
        self.levels = levels

    def __repr__(self):
        return (
            f"RelinearizationKey("
            f"base={self.base}, "
            f"levels={self.levels}, "
            f"entries={len(self.entries)}"
            f")"
        )


class KeyGenerator:
    """
    Educational RLWE-style Key Generator

    This class generates:

    - secret key
    - public key
    - error/noise polynomials

    ========================================================

    Current Educational Design

    Secret Key:
        ternary distribution {-1, 0, 1}

    Error Polynomial:
        approximate discrete Gaussian

    ========================================================

    Future Improvements

    - true discrete Gaussian samplers
    - cryptographic RNG
    - RNS decomposition
    - modulus switching
    - parameter validation
    """

    def __init__(
        self,
        ring,
        degree,
        modulus,
        noise_std=3.2,
        decomposition_base=2**10,
        decomposition_levels=12,
    ):
        self.ring = ring
        self.degree = degree
        self.modulus = modulus
        self.noise_std = noise_std
        self.decomposition_base = decomposition_base
        self.decomposition_levels = decomposition_levels

    # ========================================================
    # Secret Key Sampling
    # ========================================================

    def _sample_secret_polynomial(self):
        """
        Sample secret key polynomial.

        ====================================================

        Educational Design:
            coefficients from {-1, 0, 1}

        Why small coefficients?

        Small secret keys help:
            - efficient computation
            - stable decryption
            - RLWE hardness assumptions

        ====================================================

        Example:
            [1, 0, -1, 1, 0, 0, ...]
        """

        coeffs = [
            random.choice([-1, 0, 1])
            for _ in range(self.degree)
        ]

        return Polynomial(coeffs)

    # ========================================================
    # Uniform Polynomial Sampling
    # ========================================================

    def _sample_uniform_polynomial(self):
        """
        Sample uniformly random polynomial modulo q.

        ====================================================

        In RLWE:

            a <- uniform random polynomial

        This polynomial is PUBLIC.

        ====================================================

        Example:
            coefficients sampled from:

                [0, q-1]
        """

        coeffs = [
            random.randint(0, self.modulus - 1)
            for _ in range(self.degree)
        ]

        return Polynomial(coeffs)

    # ========================================================
    # Error / Noise Sampling
    # ========================================================

    def _sample_error_polynomial(self):
        """
        Sample small Gaussian-like error polynomial.

        ====================================================

        THIS IS ONE OF THE MOST IMPORTANT PARTS OF CKKS.

        The security of RLWE-based cryptography depends on
        adding small random errors.

        ====================================================

        Real CKKS:

            e <- Discrete Gaussian Distribution

        Educational Approximation:

            round( Normal(0, sigma) )

        ====================================================

        Why Gaussian?

        Gaussian noise is deeply connected to:
            - LWE hardness
            - RLWE hardness
            - lattice cryptography security proofs

        ====================================================

        Why should noise be small?

        If noise becomes too large:
            decrypt() will fail.

        If noise is too small:
            security weakens.

        Managing noise growth is one of the central problems
        of homomorphic encryption.
        """

        coeffs = [
            int(round(
                random.gauss(0, self.noise_std)
            ))
            for _ in range(self.degree)
        ]

        return Polynomial(coeffs)

    # ========================================================
    # Secret Key Generation
    # ========================================================

    def generate_secret_key(self):
        """
        Generate secret key.

        ====================================================

        Result:
            s <- small polynomial
        """

        s = self._sample_secret_polynomial()

        return SecretKey(s)

    # ========================================================
    # Public Key Generation
    # ========================================================

    def generate_public_key(self, secret_key):
        """
        Generate public key.

        ====================================================

        RLWE Public Key Formula:

            pk = (b, a)

        where:

            b = -a*s + e

        ====================================================

        Why this structure?

        During decryption:

            c0 + c1*s

        causes:

            -a*s and +a*s

        to cancel each other out.

        The remaining term is:

            message + noise

        which approximately recovers the original message.

        ====================================================

        Reference:
        OpenMined CKKS Explained Part 3
        """

        # ----------------------------------------------------
        # Sample uniformly random polynomial
        # ----------------------------------------------------

        a = self._sample_uniform_polynomial()

        # ----------------------------------------------------
        # Sample small Gaussian error polynomial
        # ----------------------------------------------------

        e = self._sample_error_polynomial()

        # ----------------------------------------------------
        # Retrieve secret key polynomial
        # ----------------------------------------------------

        s = secret_key.polynomial

        # ----------------------------------------------------
        # Compute:
        #
        #     a * s
        #
        # inside the polynomial ring.
        # ----------------------------------------------------

        a_times_s = self.ring.multiply(a, s)

        # ----------------------------------------------------
        # Compute:
        #
        #     b = -a*s + e
        #
        # This becomes part of the public key.
        # ----------------------------------------------------

        b = self.ring.add(
            (-1) * a_times_s,
            e,
        )

        return PublicKey(
            b=b,
            a=a,
        )
    
    # ========================================================
    # Relinearization Key Generation
    # ========================================================

    def generate_relinearization_key(self, secret_key):
        """
        Generate educational relinearization key.

        Goal:
            Help convert c2*s² into a standard ciphertext form.

        Fresh ciphertext decryption:

            c0 + c1*s

        After multiplication:

            c0 + c1*s + c2*s²

        Relinearization key provides encrypted forms of:

            B^i * s²

        where B is the decomposition base.

        For each level i:

            rlk_i = (b_i, a_i)

        where:

            b_i = -a_i*s + e_i + B^i*s²

        Then:

            b_i + a_i*s ≈ B^i*s²

        This lets us replace c2*s² with ciphertext components
        involving only 1 and s.
        """

        s = secret_key.polynomial
        s_squared = self.ring.multiply(s, s)

        entries = []

        for i in range(self.decomposition_levels):
            factor = self.decomposition_base ** i

            a_i = self._sample_uniform_polynomial()
            e_i = self._sample_error_polynomial()

            a_times_s = self.ring.multiply(a_i, s)

            # message = B^i * s²
            message = factor * s_squared

            # b_i = -a_i*s + e_i + B^i*s²
            b_i = self.ring.add(
                self.ring.add(
                    (-1) * a_times_s,
                    e_i,
                ),
                message,
            )

            entries.append(
                PublicKey(
                    b=b_i,
                    a=a_i,
                )
            )

        return RelinearizationKey(
            entries=entries,
            base=self.decomposition_base,
            levels=self.decomposition_levels,
        )