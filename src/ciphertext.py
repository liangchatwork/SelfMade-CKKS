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
# ciphertexts are not single values.
#
# A fresh ciphertext usually has two polynomial components:
#
#     ct = (c0, c1)
#
# During decryption:
#
#     message ≈ c0 + c1 * s
#
# After ciphertext-ciphertext multiplication, the ciphertext
# size grows:
#
#     (c0, c1) * (d0, d1)
#       =
#     (c0*d0, c0*d1 + c1*d0, c1*d1)
#
# Therefore, the ciphertext becomes:
#
#     ct = (c0, c1, c2)
#
# During decryption:
#
#     message ≈ c0 + c1*s + c2*s^2
#
# This growth is why CKKS needs relinearization later.
#
# Reference:
# OpenMined CKKS Explained Part 4
# https://openmined.org/blog/ckks-explained-part-4-multiplication-and-relinearization/
#
# ============================================================


class Ciphertext:
    """
    Ciphertext Class

    Represents encrypted polynomial data.

    Current supported structures:
        Fresh ciphertext:
            (c0, c1)

        After multiplication:
            (c0, c1, c2)

    Additional metadata:
        scale:
            CKKS scaling factor.

        length:
            Original vector length before encryption.
    """

    def __init__(self, c0=None, c1=None, scale=1.0, length=None, components=None):
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

        components : list, optional
            General ciphertext component list.

        Why components?

        Fresh ciphertexts have 2 components:

            [c0, c1]

        But multiplication creates 3 components:

            [c0, c1, c2]

        Later, relinearization will reduce this back to 2.
        """

        if components is not None:
            self.components = components
        else:
            self.components = [c0, c1]

        self.scale = scale
        self.length = length

        # Keep backward-compatible access.
        self.c0 = self.components[0]
        self.c1 = self.components[1] if len(self.components) > 1 else None

    # ========================================================
    # Ciphertext Size
    # ========================================================

    def size(self):
        """
        Return number of ciphertext components.

        Fresh ciphertext:
            size = 2

        After multiplication:
            size = 3
        """

        return len(self.components)

    # ========================================================
    # String Representation
    # ========================================================

    def __repr__(self):
        """
        Developer-friendly representation.
        """

        return (
            f"Ciphertext("
            f"components={self.components}, "
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
            f"size={self.size()}, "
            f"scale={self.scale}"
            f")"
        )