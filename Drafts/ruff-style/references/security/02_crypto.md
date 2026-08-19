---
---

# Security: Crypto

Choose strong primitives and secure randomness; avoid broken hashes, weak ciphers, small keys, deprecated crypto.

## Rule of thumb

1. Use SHA-256 or stronger for cryptographic hashing through `hashlib` or `cryptography`.
2. Choose modern, authenticated encryption; avoid ARC4 and ECB mode.
3. Use `secrets` for security-sensitive randomness, never `random`.
4. Use maintained libraries like `cryptography`; avoid `pycrypto`.
5. Enforce minimum key sizes: RSA/DSA ≥ 2048 bits, EC ≥ 224 bits.

## Example: In-house crypto helpers

A junior's first in-house cryptography class, mixing broken hashes, weak ciphers, predictable randomness, and undersized keys.

### Bad

```python
"""In-house crypto helpers."""

import hashlib
import random

import Crypto.Random  # S413

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, ec, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Vault:
    def __init__(self):
        self.key = b"sixteen byte key"

    def checksum(self, data: bytes) -> str:
        return hashlib.md5(data).hexdigest()  # S324

    def legacy_checksum(self, data: bytes) -> str:
        digest = hashes.Hash(hashes.MD5())  # S303
        digest.update(data)
        return digest.finalize().hex()

    def stream_encrypt(self, plaintext: bytes) -> bytes:
        cipher = Cipher(algorithms.ARC4(self.key), mode=None)  # S304
        return cipher.encryptor().update(plaintext)

    def block_encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(iv))  # S305
        return cipher.encryptor().update(plaintext)

    def nonce(self) -> int:
        return random.randrange(1_000_000)  # S311

    def keypair(self):
        dsa.generate_private_key(key_size=512)  # S505
        rsa.generate_private_key(public_exponent=65537, key_size=1024)  # S505
        ec.generate_private_key(curve=ec.SECT163K1())
```

### Good

```python
"""In-house crypto helpers."""

import hashlib
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, ec, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Vault:
    def __init__(self):
        self.key = AESGCM.generate_key(bit_length=256)
        self.fernet = Fernet(Fernet.generate_key())

    def checksum(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def legacy_checksum(self, data: bytes) -> str:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        return digest.finalize().hex()

    def stream_encrypt(self, plaintext: bytes) -> bytes:
        return self.fernet.encrypt(plaintext)

    def block_encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        aesgcm = AESGCM(self.key)
        return aesgcm.encrypt(iv, plaintext, None)

    def nonce(self) -> int:
        return secrets.randbelow(1_000_000)

    def keypair(self):
        dsa.generate_private_key(key_size=2048)
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        ec.generate_private_key(curve=ec.SECP256R1())
```

### Violations

1. **S303** — `hashes.Hash(hashes.MD5())`; MD5 is broken and vulnerable to collisions.
2. **S304** — `algorithms.ARC4(self.key)`; ARC4 is a weak, deprecated stream cipher.
3. **S305** — `modes.ECB(iv)`; ECB leaks structure and is not semantically secure.
4. **S311** — `random.randrange(1_000_000)`; `random` is predictable and unsuitable for secrets.
5. **S324** — `hashlib.md5(data).hexdigest()`; MD5 is insecure for cryptographic use.
6. **S413** — `import Crypto.Random`; pycrypto has a public buffer-overflow vulnerability.
7. **S505** — `dsa.generate_private_key(key_size=512)` and `rsa.generate_private_key(..., key_size=1024)`; keys below 2048 bits are breakable.
