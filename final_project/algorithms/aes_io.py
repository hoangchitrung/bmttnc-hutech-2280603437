"""Helpers to encrypt/decrypt files/bytes using the project's AES implementation.
Uses AES-128 ECB mode with PKCS#7 padding. Operates in binary ('rb'/'wb').
"""

from typing import List
from .aes import aes_encrypt, aes_decrypt


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid padding bytes")
    return data[:-pad_len]


def _chunkify(data: bytes, block_size: int = 16):
    for i in range(0, len(data), block_size):
        yield data[i : i + block_size]


def encrypt_bytes_ecb(plaintext: bytes, key: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("Only 16-byte AES-128 keys are supported")
    data = pkcs7_pad(plaintext, 16)
    out = bytearray()
    for block in _chunkify(data, 16):
        ct_block = bytes(aes_encrypt(list(block), list(key)))
        out.extend(ct_block)
    return bytes(out)


def decrypt_bytes_ecb(ciphertext: bytes, key: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("Only 16-byte AES-128 keys are supported")
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext length must be multiple of 16")
    out = bytearray()
    for block in _chunkify(ciphertext, 16):
        pt_block = bytes(aes_decrypt(list(block), list(key)))
        out.extend(pt_block)
    return pkcs7_unpad(bytes(out))


def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    with open(input_path, "rb") as f:
        data = f.read()
    ct = encrypt_bytes_ecb(data, key)
    with open(output_path, "wb") as f:
        f.write(ct)


def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    with open(input_path, "rb") as f:
        data = f.read()
    pt = decrypt_bytes_ecb(data, key)
    with open(output_path, "wb") as f:
        f.write(pt)
