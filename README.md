# Selfmade-CKKS

## 1. Introduction

Selfmade-CKKS is a Python implementation of the CKKS Homomorphic Encryption scheme, built to make encrypted real-number computation understandable, modular, and extensible.

This project focuses on implementing the core ideas behind CKKS from the ground up, including polynomial ring arithmetic, RLWE-based encryption, noise-based security, approximate decoding, and homomorphic computation.

Rather than simply calling an existing HE library, the goal is to gradually build a readable and educational open-source CKKS framework while preserving the real mathematical structure behind the scheme.

The project combines:

* Homomorphic Encryption
* CKKS Approximate Arithmetic
* Polynomial Ring Arithmetic
* RLWE-based Cryptography
* Gaussian Noise Sampling
* Encrypted Vector Computation
* Python Open Source Engineering

---

## 2. Background

### What is Homomorphic Encryption?

Homomorphic Encryption, or HE, is a type of encryption that allows computation to be performed directly on encrypted data.

In traditional encryption, data must be decrypted before computation:

plaintext
→ encrypt
→ ciphertext
→ decrypt
→ plaintext
→ compute

In Homomorphic Encryption, computation happens while the data remains encrypted:

plaintext
→ encrypt
→ ciphertext
→ compute on ciphertext
→ decrypt
→ computed plaintext

The key idea is that operations on ciphertexts correspond to operations on plaintexts.

For addition:

$$
Dec(Enc(a) + Enc(b)) = a + b
$$

For multiplication:

$$
Dec(Enc(a) \cdot Enc(b)) = a \cdot b
$$

A fully homomorphic encryption scheme supports both encrypted addition and encrypted multiplication, which allows general arithmetic circuits to be evaluated over encrypted data.

This is useful for:

* Privacy-preserving machine learning
* Secure cloud computation
* Federated learning
* Encrypted statistics
* Private AI inference
* Confidential data processing

---

### What is CKKS?

CKKS, proposed by Cheon, Kim, Kim, and Song, is a Homomorphic Encryption scheme designed for approximate arithmetic over real or complex numbers.

Unlike BFV or BGV, which are usually used for exact integer or modular arithmetic, CKKS is designed for numerical computation where small approximation errors are acceptable.

For example, after decryption, CKKS may return:

$$
4.999997
$$

instead of:

$$
5.0
$$

This is expected behavior.

CKKS is especially suitable for:

* Machine learning
* Neural networks
* Federated learning
* Statistical computation
* Vector operations
* Approximate numerical workloads

---

### Polynomial Ring

CKKS operates over a polynomial ring:

$$
R_q = \mathbb{Z}_q[X] / (X^N + 1)
$$

where:

* $N$ is the polynomial degree
* $q$ is the coefficient modulus
* $\mathbb{Z}_q$ means coefficients are reduced modulo $q$
* $X^N + 1$ defines the ring relation

Since:

$$
X^N + 1 = 0
$$

we have:

$$
X^N = -1
$$

Therefore:

$$
X^{N+1} = -X
$$

and:

$$
X^{N+2} = -X^2
$$

This is called negacyclic reduction.

In this project, polynomial ring arithmetic is one of the first implemented components because plaintexts, ciphertexts, keys, and noise are all represented as polynomials.

---

### RLWE-based Encryption

CKKS security is based on the Ring Learning With Errors, or RLWE, problem.

A simplified public key structure is:

$$
pk = (b, a)
$$

where:

$$
b = -a \cdot s + e
$$

and:

* $s$ is the secret key polynomial
* $a$ is a uniformly sampled public polynomial
* $e$ is a small random error polynomial

The error term $e$ is essential.

Without noise, the relationship between $a$, $b$, and $s$ would be too clean:

$$
b = -a \cdot s
$$

which would make the secret key much easier to recover.

With noise:

$$
b = -a \cdot s + e
$$

recovering $s$ becomes computationally hard under the RLWE assumption.

---

### Noise and Approximate Decryption

Noise is not a bug in CKKS. It is part of the security design.

In this project, the error polynomial is currently sampled using a Gaussian-style approximation:

$$
e_i \leftarrow round(Normal(0, \sigma))
$$

The current educational default is:

$$
\sigma = 3.2
$$

During encryption, the current simplified structure is:

$$
c_0 = m + b
$$

$$
c_1 = a
$$

So the ciphertext is:

$$
ct = (c_0, c_1)
$$

During decryption:

$$
m' = c_0 + c_1 \cdot s
$$

Substitute the encryption structure:

$$
m' = m + (-a \cdot s + e) + a \cdot s
$$

The secret-key terms cancel:

$$
m' = m + e
$$

Therefore, the decrypted value is approximately equal to the original message:

$$
m' \approx m
$$

This is why CKKS decrypts to approximate values.

---

### Scaling

CKKS uses a scale factor to preserve decimal precision.

A real number $x$ is encoded as:

$$
x \cdot \Delta
$$

where $\Delta$ is the scale.

For example:

$$
1.234 \cdot 2^{20}
$$

If the noise is small compared to the scale, then after decoding, the error becomes:

$$
\frac{e}{\Delta}
$$

For example, if:

$$
e \approx 3
$$

and:

$$
\Delta = 2^{20}
$$

then:

$$
\frac{3}{2^{20}} \approx 0.000003
$$

This is why the decrypted result may look like:

$$
4.999992
$$

instead of exactly:

$$
5.0
$$

---

### Current Implementation Note

The current encoder does not yet implement full CKKS canonical embedding.

Real CKKS encoding involves:

* Complex vector slots
* Roots of unity
* Canonical embedding
* Inverse embedding
* Coordinate projection
* Scaling
* Random rounding

The current version uses a simplified educational encoder:

$$
vector[i] \cdot \Delta \rightarrow polynomial\ coefficient[i]
$$

This allows the project to first build a complete working pipeline:

vector
→ encode
→ plaintext
→ encrypt
→ ciphertext
→ homomorphic addition
→ decrypt
→ decode

Future versions will replace this simplified encoder with a more complete CKKS encoding implementation.

---

## 3. Tech Stack

### Core Implementation

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)

### Future Development

![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge\&logo=jupyter\&logoColor=white)

### Cryptographic Focus

* Polynomial Ring Arithmetic
* RLWE-based Encryption
* CKKS Approximate Arithmetic
* Gaussian-style Noise Sampling


---

## 4. Roadmap

### Phase 1 — Polynomial Arithmetic ✅

* [x] Polynomial class
* [x] Polynomial addition
* [x] Polynomial subtraction
* [x] Polynomial multiplication
* [x] Scalar multiplication
* [x] Pretty printing

---

### Phase 2 — Polynomial Ring Arithmetic ✅

* [x] Polynomial ring abstraction
* [x] Negacyclic reduction
* [x] Ring addition
* [x] Ring subtraction
* [x] Ring multiplication

---

### Phase 3 — Encoding / Decoding 🚧

* [x] Simplified encoder
* [x] Scaling support
* [x] Decode pipeline
* [x] Vector length metadata
* [ ] Canonical embedding
* [ ] Inverse embedding
* [ ] Coordinate projection
* [ ] Random rounding
* [ ] Full CKKS encoding

---

### Phase 4 — RLWE Key Generation ✅

* [x] Secret key generation
* [x] Public key generation
* [x] Uniform polynomial sampling
* [x] Gaussian-style error sampling

---

### Phase 5 — Encryption / Decryption ✅

* [x] Plaintext abstraction
* [x] Ciphertext abstraction
* [x] Encryption
* [x] Decryption
* [x] Approximate recovery

---

### Phase 6 — Homomorphic Addition ✅

* [x] Ciphertext addition
* [x] Encrypted vector addition demo
* [x] Approximate decrypted result

---

### Phase 7 — Ciphertext Multiplication

* [ ] Ciphertext multiplication
* [ ] Ciphertext size growth
* [ ] Noise growth tracking

---

### Phase 8 — Relinearization

* [ ] Relinearization key
* [ ] Key switching
* [ ] Ciphertext size reduction

---

### Phase 9 — Rescaling

* [ ] Scale growth handling
* [ ] Modulus switching
* [ ] Level management

---

### Phase 10 — Vector and API Improvements

* [ ] NumPy support
* [ ] Cleaner high-level API
* [ ] SIMD-style packing
* [ ] More examples
* [ ] Unit tests

---

## 5. Usage

### Installation

Clone the repository:

```bash
git clone https://github.com/liangchatwork/SelfMade-CKKS.git
```

Enter the project directory:

```bash
cd selfmade-ckks
```

---

### Encoding and Decoding

```bash
python examples/01_encoding_decoding.py
```

Example output:

```bash
Original:   [1.1, 2.2, 3.3]
Plaintext:  Plaintext(1153433.6 + 2306867.2x + 3460300.8x^2)
Decoded:    [1.1, 2.2, 3.3]
```

---

### Encryption and Decryption

```bash
python examples/02_encrypt_decrypt.py
```

Example output:

```bash
Original:   [1.1, 2.2, 3.3]
Decrypted:  [1.1000009, 2.2000038, 3.2999990]
```

---

### Homomorphic Addition

```bash
python examples/03_homomorphic_addition.py
```

Example output:

```bash
Input A:    [1, 2, 3]
Input B:    [4, 5, 6]
Decrypted:  [4.999992, 7.000005, 8.999994]
```

This demonstrates:

$$
Dec(Enc(A) + Enc(B)) \approx A + B
$$

---

## 6. Reference

### Papers

* Cheon, J. H., Kim, A., Kim, M., & Song, Y. (2017). *Homomorphic Encryption for Arithmetic of Approximate Numbers*. In **Advances in Cryptology — ASIACRYPT 2017**, Lecture Notes in Computer Science, vol. 10624, pp. 409–437. Springer. [https://doi.org/10.1007/978-3-319-70694-8_15](https://doi.org/10.1007/978-3-319-70694-8_15)

* Regev, O. (2005). *On Lattices, Learning with Errors, Random Linear Codes, and Cryptography*. In **Proceedings of the 37th Annual ACM Symposium on Theory of Computing (STOC 2005)**, pp. 84–93. ACM. [https://doi.org/10.1145/1060590.1060603](https://doi.org/10.1145/1060590.1060603)

* Lyubashevsky, V., Peikert, C., & Regev, O. (2010). *On Ideal Lattices and Learning with Errors over Rings*. In **Advances in Cryptology — EUROCRYPT 2010**, Lecture Notes in Computer Science, vol. 6110, pp. 1–23. Springer. [https://doi.org/10.1007/978-3-642-13190-5_1](https://doi.org/10.1007/978-3-642-13190-5_1)

### Learning Resources

* OpenMined. *CKKS Explained Series*.
  [https://openmined.org/blog/tag/ckks/](https://openmined.org/blog/tag/ckks/)

### Related Libraries

* Microsoft SEAL.
  [https://github.com/microsoft/SEAL](https://github.com/microsoft/SEAL)

* OpenFHE.
  [https://github.com/openfheorg/openfhe-development](https://github.com/openfheorg/openfhe-development)

* TenSEAL.
  [https://github.com/OpenMined/TenSEAL](https://github.com/OpenMined/TenSEAL)

* Pyfhel.
  [https://github.com/ibarrond/Pyfhel](https://github.com/ibarrond/Pyfhel)
