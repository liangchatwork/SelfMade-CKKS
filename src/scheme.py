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

    def __init__(
        self,
        ring,
        public_key,
        secret_key,
        relinearization_key=None,
    ):
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
        self.relinearization_key = relinearization_key

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
            depth=0,
            history=["encrypt"],
        )

    # ========================================================
    # Decryption
    # ========================================================

    def decrypt_ciphertext(self, ciphertext):
        """
        Decrypt a Ciphertext object into a Plaintext object.

        Fresh ciphertext decryption:

            m' = c0 + c1*s

        After multiplication, ciphertext may have 3 components:

            m' = c0 + c1*s + c2*s^2

        General form:

            m' = sum(ci * s^i)

        This is mathematically important because ciphertext
        multiplication increases ciphertext size.

        Relinearization will later reduce:

            (c0, c1, c2)

        back into:

            (c0, c1)
        """

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("decrypt_ciphertext expects a Ciphertext object.")

        s = self.secret_key.polynomial

        # Start with c0.
        recovered = ciphertext.components[0]

        # Current power of secret key.
        #
        # For i = 1:
        #     s_power = s
        #
        # For i = 2:
        #     s_power = s^2
        #
        s_power = s

        for i in range(1, len(ciphertext.components)):
            term = self.ring.multiply(
                ciphertext.components[i],
                s_power,
            )

            recovered = self.ring.add(
                recovered,
                term,
            )

            # Prepare next power:
            #
            #     s_power = s_power * s
            #
            if i < len(ciphertext.components) - 1:
                s_power = self.ring.multiply(
                    s_power,
                    s,
                )

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
            depth=max(left.depth, right.depth),
            history=left.history + right.history + ["add_ciphertexts"],
        )
    
    # ========================================================
    # Ciphertext-Ciphertext Multiplication
    # ========================================================

    def multiply_ciphertexts(self, left, right):
        """
        Multiply two ciphertexts homomorphically.

        Mathematical idea:

            left  = (c0, c1)
            right = (d0, d1)

        Then:

            left * right
                =
            (c0*d0,
             c0*d1 + c1*d0,
             c1*d1)

        This creates a 3-component ciphertext:

            (r0, r1, r2)

        Decryption becomes:

            r0 + r1*s + r2*s^2

        Important CKKS consequence:

        1. Ciphertext size grows:
               2 -> 3

        2. Scale grows:
               Δ -> Δ²

        3. Noise grows.

        Later phases will implement:

        - relinearization:
              reduce size 3 back to size 2

        - rescaling:
              reduce scale Δ² back to manageable scale
        """

        if not isinstance(left, Ciphertext):
            raise TypeError("left must be a Ciphertext object.")

        if not isinstance(right, Ciphertext):
            raise TypeError("right must be a Ciphertext object.")

        if left.scale != right.scale:
            raise ValueError(
                "Ciphertexts must have the same scale before multiplication."
            )

        if left.length != right.length:
            raise ValueError(
                "Ciphertexts must have the same vector length before multiplication."
            )

        if left.size() != 2 or right.size() != 2:
            raise ValueError(
                "Current multiplication only supports fresh 2-component ciphertexts."
            )

        c0, c1 = left.components
        d0, d1 = right.components

        # r0 = c0 * d0
        r0 = self.ring.multiply(c0, d0)

        # r1 = c0*d1 + c1*d0
        c0_d1 = self.ring.multiply(c0, d1)
        c1_d0 = self.ring.multiply(c1, d0)
        r1 = self.ring.add(c0_d1, c1_d0)

        # r2 = c1 * d1
        r2 = self.ring.multiply(c1, d1)

        return Ciphertext(
            components=[r0, r1, r2],
            scale=left.scale * right.scale,
            length=left.length,
            depth=max(left.depth, right.depth) + 1,
            history=left.history + right.history + ["multiply_ciphertexts"],
        )
    
    # ========================================================
    # Polynomial Decomposition
    # ========================================================

    def _decompose_polynomial(self, poly, base, levels):
        """
        Decompose a polynomial into base-B digit polynomials.

        Example:

            coeff = 1234
            base = 10

        becomes digits:

            4, 3, 2, 1

        For relinearization, we decompose c2:

            c2 = d0 + d1*B + d2*B² + ...

        Then each digit polynomial is used with the matching
        relinearization key entry.
        """

        digit_coeffs = [
            [0 for _ in range(len(poly.coefficients))]
            for _ in range(levels)
        ]

        for coeff_index, coeff in enumerate(poly.coefficients):
            sign = -1 if coeff < 0 else 1
            value = abs(int(round(coeff)))

            for level in range(levels):
                digit = value % base
                digit_coeffs[level][coeff_index] = sign * digit
                value //= base

            if value != 0:
                raise ValueError(
                    "Polynomial coefficient is too large for current "
                    "decomposition levels. Increase decomposition_levels."
                )

        return [
            type(poly)(coeffs)
            for coeffs in digit_coeffs
        ]
    
    # ========================================================
    # Relinearization
    # ========================================================

    def relinearize_ciphertext(self, ciphertext):
        """
        Relinearize a 3-component ciphertext back to 2 components.

        Input after multiplication:

            ct = (r0, r1, r2)

        Decryption would be:

            r0 + r1*s + r2*s²

        Relinearization replaces:

            r2*s²

        with:

            u0 + u1*s

        using the relinearization key.

        Output:

            ct' = (r0 + u0, r1 + u1)

        Then decryption becomes:

            (r0 + u0) + (r1 + u1)*s

        which is approximately equivalent to:

            r0 + r1*s + r2*s²
        """

        if self.relinearization_key is None:
            raise ValueError("Relinearization key is not available.")

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("ciphertext must be a Ciphertext object.")

        if ciphertext.size() != 3:
            raise ValueError(
                "Relinearization currently expects a 3-component ciphertext."
            )

        r0, r1, r2 = ciphertext.components

        base = self.relinearization_key.base
        levels = self.relinearization_key.levels

        digit_polys = self._decompose_polynomial(
            r2,
            base=base,
            levels=levels,
        )

        # These accumulate the replacement for r2*s²:
        #
        #     r2*s² ≈ u0 + u1*s
        #
        u0 = self.ring.create_constant(0)
        u1 = self.ring.create_constant(0)

        for level, digit_poly in enumerate(digit_polys):
            relin_entry = self.relinearization_key.entries[level]

            # digit * b_i
            part0 = self.ring.multiply(
                digit_poly,
                relin_entry.b,
            )

            # digit * a_i
            part1 = self.ring.multiply(
                digit_poly,
                relin_entry.a,
            )

            u0 = self.ring.add(u0, part0)
            u1 = self.ring.add(u1, part1)

        new_c0 = self.ring.add(r0, u0)
        new_c1 = self.ring.add(r1, u1)

        return Ciphertext(
            components=[new_c0, new_c1],
            scale=ciphertext.scale,
            length=ciphertext.length,
            depth=ciphertext.depth,
            history=ciphertext.add_history("relinearize"),
        )
    
    # ========================================================
    # Ciphertext-Plaintext Addition
    # ========================================================

    def add_plaintext_to_ciphertext(self, ciphertext, plaintext):
        """
        Add a plaintext to a ciphertext.

        Mathematical idea:

            ct = (c0, c1)

        If plaintext is encoded as polynomial p, then:

            ct + p = (c0 + p, c1)

        Why only c0 changes?

        During decryption:

            (c0 + p) + c1 * s
                =
            (c0 + c1 * s) + p

        Since:

            c0 + c1 * s ≈ m

        the result becomes:

            m + p

        Therefore:

            Dec(Enc(m) + Encode(p)) ≈ m + p

        This operation is cheaper than ciphertext-ciphertext
        addition because plaintext does not contain a second
        ciphertext component.
        """

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("ciphertext must be a Ciphertext object.")

        if not isinstance(plaintext, Plaintext):
            raise TypeError("plaintext must be a Plaintext object.")

        if ciphertext.scale != plaintext.scale:
            raise ValueError(
                "Ciphertext and plaintext must have the same scale."
            )

        if ciphertext.length != plaintext.length:
            raise ValueError(
                "Ciphertext and plaintext must have the same vector length."
            )

        new_c0 = self.ring.add(
            ciphertext.c0,
            plaintext.polynomial,
        )

        return Ciphertext(
            c0=new_c0,
            c1=ciphertext.c1,
            scale=ciphertext.scale,
            length=ciphertext.length,
            depth=ciphertext.depth,
            history=ciphertext.add_history("add_plaintext"),
        )


    # ========================================================
    # Ciphertext-Scalar Multiplication
    # ========================================================

    def multiply_ciphertext_by_scalar(self, ciphertext, scalar):
        """
        Multiply a ciphertext by a scalar constant.

        Mathematical idea:

            ct = (c0, c1)

        To multiply by scalar k:

            k * ct = (k*c0, k*c1)

        During decryption:

            k*c0 + k*c1*s
                =
            k * (c0 + c1*s)

        Since:

            c0 + c1*s ≈ m

        the result becomes:

            k*m

        Important:

        This operation keeps the same scale.

        It is different from multiplying by an encoded plaintext
        with scale Δ, which would cause:

            Δ * Δ = Δ²

        and require rescaling later.
        """

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("ciphertext must be a Ciphertext object.")

        new_c0 = scalar * ciphertext.c0
        new_c1 = scalar * ciphertext.c1

        return Ciphertext(
            c0=new_c0,
            c1=new_c1,
            scale=ciphertext.scale,
            length=ciphertext.length,
            depth=ciphertext.depth,
            history=ciphertext.add_history("multiply_scalar"),
        )
    
    # ========================================================
    # Ciphertext-Plaintext Multiplication
    # ========================================================

    def multiply_plaintext_with_ciphertext(self, ciphertext, plaintext):
        """
        Multiply a ciphertext by an encoded plaintext.

        Mathematical idea:

            ct = (c0, c1)
            pt = p

        Then:

            ct * pt = (c0 * p, c1 * p)

        Decryption:

            (c0 * p) + (c1 * p) * s
              = p * (c0 + c1*s)
              ≈ p * m

        Scale behavior:

            ciphertext.scale = Δ
            plaintext.scale  = Δ

            result.scale = Δ²

        This is different from scalar multiplication.

        Scalar multiplication:

            Enc(m) * k

        keeps the same scale.

        Plaintext multiplication:

            Enc(m) * Encode(p)

        grows the scale.
        """

        if not isinstance(ciphertext, Ciphertext):
            raise TypeError("ciphertext must be a Ciphertext object.")

        if not isinstance(plaintext, Plaintext):
            raise TypeError("plaintext must be a Plaintext object.")

        if ciphertext.length != plaintext.length:
            raise ValueError("Ciphertext and plaintext must have the same length.")

        new_components = [
            self.ring.multiply(component, plaintext.polynomial)
            for component in ciphertext.components
        ]

        if ciphertext.scale != plaintext.scale:
            raise ValueError(
                "Ciphertext and plaintext must have the same scale before multiplication."
            )

        return Ciphertext(
            components=new_components,
            scale=ciphertext.scale * plaintext.scale,
            length=ciphertext.length,
            depth=ciphertext.depth + 1,
            history=ciphertext.add_history("multiply_plaintext"),
        )