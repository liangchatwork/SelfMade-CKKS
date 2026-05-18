# ============================================================
# selfmade-ckks
#
# Ciphertext Representation
#
# In CKKS, a fresh ciphertext usually contains two polynomial
# components:
#
#     ct = (c0, c1)
#
# Decryption uses:
#
#     c0 + c1 * s
#
# After ciphertext-ciphertext multiplication, ciphertext size
# grows:
#
#     (c0, c1) * (d0, d1)
#       = (c0*d0, c0*d1 + c1*d0, c1*d1)
#
# The multiplied ciphertext has three components:
#
#     ct = (c0, c1, c2)
#
# Decryption then uses:
#
#     c0 + c1*s + c2*s^2
#
# Relinearization later reduces size 3 back to size 2.
#
# This class also stores educational metadata:
#
#     scale   - CKKS scale metadata
#     length  - original vector length
#     depth   - multiplication depth
#     history - operation history for educational tracking
#
# Note:
# This is not a formal cryptographic noise estimator yet.
# ============================================================


class Ciphertext:
    """
    Ciphertext object used by Selfmade-CKKS.

    Supports both:

        Fresh ciphertext:
            components = [c0, c1]

        Multiplied ciphertext:
            components = [c0, c1, c2]

    The metadata fields help track CKKS behavior during
    homomorphic operations.
    """

    def __init__(
        self,
        c0=None,
        c1=None,
        components=None,
        scale=1.0,
        length=None,
        depth=0,
        history=None,
    ):
        if components is not None:
            self.components = components
        else:
            if c0 is None or c1 is None:
                raise ValueError(
                    "Ciphertext requires either components or both c0 and c1."
                )
            self.components = [c0, c1]

        if len(self.components) < 2:
            raise ValueError("Ciphertext must contain at least two components.")

        # Backward-compatible access.
        self.c0 = self.components[0]
        self.c1 = self.components[1]

        self.scale = scale
        self.length = length

        # Educational noise / operation tracking metadata.
        self.depth = depth
        self.history = history if history is not None else []

    def size(self):
        """
        Return the number of ciphertext components.
        """
        return len(self.components)

    def add_history(self, operation):
        """
        Return a copied history list with a new operation appended.
        """
        return self.history + [operation]

    def __repr__(self):
        return (
            f"Ciphertext("
            f"size={self.size()}, "
            f"scale={self.scale}, "
            f"length={self.length}, "
            f"depth={self.depth}, "
            f"history={self.history}"
            f")"
        )

    def __str__(self):
        return self.__repr__()