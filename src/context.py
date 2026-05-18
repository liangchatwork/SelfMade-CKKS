# ============================================================
# selfmade-ckks
#
# File: context.py
#
# Description:
# High-level user-facing CKKS context.
#
# This is the main API layer of the project.
#
# Users should be able to write:
#
#     ctx = CKKSContext()
#     ct = ctx.encrypt([1.0, 2.0, 3.0])
#     result = ctx.decrypt(ct)
#
# without directly managing:
#
# - polynomial rings
# - encoders
# - secret keys
# - public keys
# - ciphertext internals
#
# ============================================================

from he_math.ring import PolynomialRing
from encoder import CKKSEncoder
from plaintext import Plaintext
from keys import KeyGenerator
from scheme import CKKSScheme


class CKKSContext:
    """
    High-level CKKS Context

    This object manages:

    - ring parameters
    - encoder
    - key generation
    - encryption scheme

    Current status:
        Educational RLWE-style CKKS prototype.

    Future goal:
        Full CKKS-style framework with multiplication,
        relinearization, rescaling, and real encoding.
    """

    def __init__(
        self,
        degree=8,
        modulus=2**40,
        scale=2**20,
        noise_std=3.2,
    ):
        """
        Initialize CKKS context.

        Parameters
        ----------
        degree : int
            Ring degree N.

        modulus : int
            Coefficient modulus q.

        scale : float
            CKKS scale Δ.

        noise_std : float
            Standard deviation for Gaussian-like error noise.

        Important:
            We do NOT remove noise.

            Noise is required for RLWE security.

            Correctness comes from using a large scale Δ,
            so that noise / Δ becomes small after decoding.
        """

        self.degree = degree
        self.modulus = modulus
        self.scale = scale
        self.noise_std = noise_std

        # ----------------------------------------------------
        # Polynomial ring:
        #
        #     Z[X] / (X^N + 1)
        # ----------------------------------------------------

        self.ring = PolynomialRing(degree=degree)

        # ----------------------------------------------------
        # Encoder:
        #
        # Current version:
        #     simplified coefficient mapping with scale.
        #
        # Future version:
        #     real CKKS canonical embedding.
        # ----------------------------------------------------

        self.encoder = CKKSEncoder(scale=scale)

        # ----------------------------------------------------
        # Key generation:
        #
        # secret key:
        #     small ternary polynomial
        #
        # error noise:
        #     Gaussian-like polynomial
        # ----------------------------------------------------

        keygen = KeyGenerator(
            ring=self.ring,
            degree=degree,
            modulus=modulus,
            noise_std=noise_std,
        )

        self.secret_key = keygen.generate_secret_key()
        self.public_key = keygen.generate_public_key(self.secret_key)

        # ----------------------------------------------------
        # Main encryption scheme.
        # ----------------------------------------------------

        self.scheme = CKKSScheme(
            ring=self.ring,
            public_key=self.public_key,
            secret_key=self.secret_key,
        )

    # ========================================================
    # Encode / Decode
    # ========================================================

    def encode(self, vector):
        """
        Encode a raw vector into a Plaintext object.

        Pipeline:

            raw vector
                -> encoder.encode()
                -> Plaintext
        """

        poly = self.encoder.encode(vector)

        return Plaintext(
            polynomial=poly,
            scale=self.scale,
            length=len(vector),
        )

    def decode(self, plaintext):
        """
        Decode a Plaintext object back into a vector.

        Pipeline:

            Plaintext
                -> encoder.decode()
                -> approximate vector
        """

        return self.encoder.decode(
            plaintext.polynomial,
            length=plaintext.length,
        )

    # ========================================================
    # Encrypt / Decrypt
    # ========================================================

    def encrypt(self, vector):
        """
        Encode and encrypt a vector.

        User-facing API:

            ct = ctx.encrypt([1.0, 2.0, 3.0])
        """

        plaintext = self.encode(vector)

        return self.scheme.encrypt_plaintext(plaintext)

    def decrypt(self, ciphertext):
        """
        Decrypt and decode a ciphertext.

        User-facing API:

            result = ctx.decrypt(ct)

        Because this is CKKS-style approximate arithmetic,
        result may be close to the original value, not exactly equal.
        """

        plaintext = self.scheme.decrypt_ciphertext(ciphertext)

        return self.decode(plaintext)

    # ========================================================
    # Homomorphic Addition
    # ========================================================

    def add(self, left, right):
        """
        Add two ciphertexts homomorphically.

        Example:

            enc_sum = ctx.add(enc_a, enc_b)
        """

        return self.scheme.add_ciphertexts(left, right)
    
    # ========================================================
    # Ciphertext-Plaintext Addition
    # ========================================================

    def add_plain(self, ciphertext, plain_vector):
        """
        Add a plaintext vector to a ciphertext.

        User-facing API:

            enc = ctx.encrypt([1, 2, 3])
            out = ctx.add_plain(enc, [10, 20, 30])

        Internally:

            plain_vector
                -> encode
                -> Plaintext
                -> scheme.add_plaintext_to_ciphertext()
        """

        plaintext = self.encode(plain_vector)

        return self.scheme.add_plaintext_to_ciphertext(
            ciphertext,
            plaintext,
        )
    
