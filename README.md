# Selfmade-CKKS

## Introduction

Selfmade-CKKS is a Python implementation of the CKKS Homomorphic Encryption scheme, built to make encrypted real-number computation understandable, modular, and extensible.

This project focuses on implementing the core ideas behind CKKS from the ground up, including polynomial ring arithmetic, RLWE-based encryption, noise-based security, approximate decoding, homomorphic computation, ciphertext multiplication, scale growth, and relinearization.

Rather than simply calling an existing HE library, the goal is to gradually build a readable and educational open-source CKKS framework while preserving the real mathematical structure behind the scheme.

The project combines:

* Homomorphic Encryption
* CKKS Approximate Arithmetic
* Polynomial Ring Arithmetic
* RLWE-based Cryptography
* Gaussian Noise Sampling
* Encrypted Vector Computation
* Ciphertext Multiplication
* Relinearization
* Educational Noise / Operation Tracking
* Python Open Source Engineering

---

## Background

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

This project also tracks educational operation metadata such as multiplication depth and operation history. This is useful for understanding how ciphertexts evolve during homomorphic operations.

Current tracking includes:

* Ciphertext size
* Scale metadata
* Multiplication depth
* Operation history

However, this is not yet a formal CKKS noise bound estimator.

---

### Plaintext-Ciphertext Operations

In CKKS, plaintext values can also interact directly with ciphertexts.

This means operations such as:

$$
Enc(m) + Encode(p)
$$

and:

$$
Enc(m) \cdot Encode(p)
$$

are also supported.

After decryption:

$$
Dec(Enc(m) + Encode(p)) \approx m + p
$$

and:

$$
Dec(Enc(m) \cdot Encode(p)) \approx m \cdot p
$$

Plaintext values must still be encoded into polynomial form before interacting with ciphertexts.

Ciphertext-plaintext addition is currently supported in this project.

Ciphertext-plaintext multiplication is also currently supported. Since both the ciphertext and plaintext carry scale, multiplication causes scale growth:

$$
\Delta \cdot \Delta = \Delta^2
$$

This means rescaling will be needed in later phases to reduce the scale back to a manageable level.

---

### Ciphertext Multiplication

Fresh CKKS ciphertexts usually contain two polynomial components:

$$
ct = (c_0, c_1)
$$

Decryption uses:

$$
m' = c_0 + c_1 \cdot s
$$

When two ciphertexts are multiplied:

$$
(c_0, c_1) \cdot (d_0, d_1)
$$

the result becomes:

$$
(c_0d_0,\ c_0d_1 + c_1d_0,\ c_1d_1)
$$

This creates a three-component ciphertext:

$$
ct_{mul} = (r_0, r_1, r_2)
$$

Decryption then becomes:

$$
m' = r_0 + r_1 \cdot s + r_2 \cdot s^2
$$

This is why multiplication increases ciphertext size:

$$
2 \rightarrow 3
$$

In this project, ciphertext-ciphertext multiplication has been implemented, and the multiplication demo shows ciphertext size growth, scale growth, and multiplication depth tracking.

---

### Relinearization

After ciphertext multiplication, the ciphertext has three components:

$$
(r_0, r_1, r_2)
$$

The extra $r_2$ component introduces an $s^2$ term during decryption:

$$
r_0 + r_1s + r_2s^2
$$

Relinearization converts this back into a two-component ciphertext:

$$
(c_0', c_1')
$$

so that decryption returns to the standard form:

$$
c_0' + c_1's
$$

The goal is:

$$
c_0' + c_1's \approx r_0 + r_1s + r_2s^2
$$

This project currently implements an educational relinearization mechanism using gadget/base decomposition and relinearization keys.

After relinearization:

$$
3 \rightarrow 2
$$

The decrypted result should remain approximately the same, while the ciphertext structure becomes compact again.

Relinearization does not reduce the scale. Scale reduction is handled by rescaling, which is planned for a later phase.

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

After multiplication, the scale grows:

$$
\Delta \cdot \Delta = \Delta^2
$$

For example:

$$
2^{20} \cdot 2^{20} = 2^{40}
$$

This project currently tracks scale metadata correctly after ciphertext-plaintext and ciphertext-ciphertext multiplication.

Rescaling is not implemented yet.

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
→ multiplication  
→ relinearization  
→ decrypt  
→ decode

Future versions will replace this simplified encoder with a more complete CKKS encoding implementation.

---

## Tech Stack

### Core Implementation

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Future Development

![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

### Cryptographic Focus

* Polynomial Ring Arithmetic
* RLWE-based Encryption
* CKKS Approximate Arithmetic
* Gaussian-style Noise Sampling
* Ciphertext Multiplication
* Relinearization
* Scale Tracking
* Educational Noise / Operation Tracking

---

## Roadmap

### Phase 1 — Polynomial Arithmetic ✅

* [x] Polynomial class
* [x] Polynomial addition
* [x] Polynomial subtraction
* [x] Polynomial multiplication
* [x] Scalar multiplication
* [x] Pretty printing

---

### Phase 2 — Polynomial Ring Arithmetic 🚧

* [x] Polynomial ring abstraction
* [x] Negacyclic reduction
* [x] Ring addition
* [x] Ring subtraction
* [x] Ring multiplication
* [ ] Coefficient modulus q reduction
* [ ] Centered coefficient representation

---

### Phase 3 — Encoding / Decoding 🚧

* [x] Simplified coefficient-based encoder
* [x] Scaling support
* [x] Decode pipeline
* [x] Vector length metadata
* [x] Integer rounding after scaling
* [ ] Canonical embedding
* [ ] Inverse canonical embedding
* [ ] Random rounding
* [ ] Full CKKS encoding

---

### Phase 4 — RLWE Key Generation 🚧

* [x] Secret key generation
* [x] Public key generation
* [x] Uniform polynomial sampling
* [x] Gaussian-style error sampling
* [x] Relinearization key generation
* [ ] Randomized encryption support using u, e0, e1

---

### Phase 5 — Encryption / Decryption 🚧

* [x] Plaintext abstraction
* [x] Ciphertext abstraction
* [x] Encryption
* [x] Decryption
* [x] Approximate recovery
* [x] Scale metadata support
* [x] Ciphertext depth tracking
* [x] Operation history tracking
* [ ] Decryption correctness under modulus q

---

### Phase 6 — Basic Homomorphic Operations ✅

* [x] Ciphertext addition
* [x] Ciphertext-plaintext addition
* [x] Ciphertext-scalar addition
* [x] Ciphertext-scalar multiplication
* [x] Scalar broadcasting through plaintext encoding
* [x] Encrypted vector addition demo

---

### Phase 7 — Multiplication and Scale Growth ✅

* [x] Ciphertext-plaintext multiplication
* [x] Ciphertext multiplication
* [x] Ciphertext size growth
* [x] Scale growth tracking
* [x] Decryption for 3-component ciphertexts
* [x] Multiplication demo
* [x] Educational noise / operation tracking

---

### Phase 8 — Relinearization 🚧

* [x] Relinearization key
* [x] Gadget/base decomposition
* [x] Convert ciphertext size from 3 back to 2
* [x] Relinearization demo
* [ ] Relinearization correctness tests

---

### Phase 9 — Rescaling and Modulus Switching 🚧

* [ ] Rescaling operation
* [ ] Modulus switching
* [ ] Level management
* [ ] Multiplication chain support

---

### Phase 10 — Testing and API Improvements 🚧

* [ ] Unit tests with Pytest
* [ ] Numerical tolerance tests
* [ ] Random vector tests
* [ ] NumPy support
* [ ] Optional Pandas-based result reporting
* [ ] Cleaner high-level API
* [ ] More examples
* [ ] Formal noise estimation

---

## Usage

### Installation

Clone the repository:

```bash
git clone https://github.com/liangchatwork/SelfMade-CKKS.git
````

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
Plaintext:  Plaintext(1153434 + 2306867x + 3460301x^2)
Decoded:    [1.1000003814697266, 2.1999998092651367, 3.3000001907348633]
```

This demonstrates:

$$
Encode(x) = round(x \cdot \Delta)
$$

and:

$$
Decode(Encode(x)) \approx x
$$

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

This demonstrates approximate CKKS-style decryption:

$$
Dec(Enc(x)) \approx x
$$

---

### Basic Homomorphic Operations

```bash
python examples/03_homomorphic_addition.py
```

Example output:

```bash
Ciphertext + Ciphertext
Input A:    [1, 2, 3]
Input B:    [4, 5, 6]
Expected:   [5, 7, 9]
Decrypted:  [4.999992, 7.000005, 8.999994]
```

Current supported basic operations:

$$
Enc(a) + Enc(b)
$$

$$
Enc(a) + Encode(p)
$$

$$
Enc(a) + k
$$

$$
Enc(a) \cdot k
$$

Scalar addition is implemented by encoding:

$$
[k, k, k, ...]
$$

with the same ciphertext vector length.

Scalar multiplication directly multiplies ciphertext polynomial components and keeps the same scale.

---

### Multiplication and Relinearization

```bash
python examples/04_multiplication_relinearization.py
```

Example output:

```bash
Ciphertext * Plaintext
Encrypted Input:       [2]
Plaintext Input:       [3]
Expected:              [6]
Ciphertext Size:       2
Scale:                 1099511627776
Depth:                 1
History:               ['encrypt', 'multiply_plaintext']
Decrypted:             [5.99994277954102]

Ciphertext * Ciphertext
Input A:               [2]
Input B:               [3]
Expected:              [6]

Before Relinearization
Ciphertext Size:       3
Scale:                 1099511627776
Depth:                 1
History:               ['encrypt', 'encrypt', 'multiply_ciphertexts']
Decrypted:             [5.999904632486505]

After Relinearization
Ciphertext Size:       2
Scale:                 1099511627776
Depth:                 1
History:               ['encrypt', 'encrypt', 'multiply_ciphertexts', 'relinearize']
Decrypted:             [5.999990478757354]
```

This demonstrates ciphertext-plaintext multiplication:

$$
Dec(Enc(a) \cdot Encode(p)) \approx a \cdot p
$$

ciphertext-ciphertext multiplication:

$$
Dec(Enc(a) \cdot Enc(b)) \approx a \cdot b
$$

ciphertext size growth:

$$
2 \rightarrow 3
$$

and relinearization:

$$
3 \rightarrow 2
$$

The scale remains:

$$
\Delta^2
$$

because rescaling has not been implemented yet.

Depth and history are currently educational metadata for understanding operation flow. They are not formal CKKS noise bounds.

---

## Reference

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

