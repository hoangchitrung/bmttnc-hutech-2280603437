"""
Triple DES (3DES) - EDE Mode (Encrypt-Decrypt-Encrypt)
Sử dụng ba khóa DES liên tiếp

C = E(K3, D(K2, E(K1, P)))
P = D(K1, E(K2, D(K3, C)))

Pure Python implementation, không dùng thư viện crypto bên ngoài.
"""

from des import des_encrypt, des_decrypt


def triple_des_encrypt(plaintext, key1, key2, key3):
    """
    Mã hóa plaintext sử dụng Triple DES (EDE mode)

    Quá trình:
    1. Mã hóa với K1: temp1 = E(K1, plaintext)
    2. Giải mã với K2: temp2 = D(K2, temp1)
    3. Mã hóa với K3: ciphertext = E(K3, temp2)

    Args:
        plaintext: Dữ liệu gốc (bytes hoặc int)
        key1: Khóa thứ nhất (8 bytes)
        key2: Khóa thứ hai (8 bytes)
        key3: Khóa thứ ba (8 bytes)

    Returns:
        Dữ liệu mã hóa (int)
    """
    # Convert bytes to int if needed
    if isinstance(plaintext, bytes):
        plaintext = int.from_bytes(plaintext, "big")
    if isinstance(key1, bytes):
        key1 = int.from_bytes(key1, "big")
    if isinstance(key2, bytes):
        key2 = int.from_bytes(key2, "big")
    if isinstance(key3, bytes):
        key3 = int.from_bytes(key3, "big")

    # Step 1: Encrypt with K1
    temp1 = des_encrypt(plaintext, key1)
    # Step 2: Decrypt with K2
    temp2 = des_decrypt(temp1, key2)
    # Step 3: Encrypt with K3
    ciphertext = des_encrypt(temp2, key3)

    return ciphertext


def triple_des_decrypt(ciphertext, key1, key2, key3):
    """
    Giải mã ciphertext sử dụng Triple DES (EDE mode)

    Quá trình (ngược lại):
    1. Giải mã với K3: temp1 = D(K3, ciphertext)
    2. Mã hóa với K2: temp2 = E(K2, temp1)
    3. Giải mã với K1: plaintext = D(K1, temp2)

    Args:
        ciphertext: Dữ liệu mã hóa (bytes hoặc int)
        key1: Khóa thứ nhất (8 bytes)
        key2: Khóa thứ hai (8 bytes)
        key3: Khóa thứ ba (8 bytes)

    Returns:
        Dữ liệu gốc (int)
    """
    # Convert bytes to int if needed
    if isinstance(ciphertext, bytes):
        ciphertext = int.from_bytes(ciphertext, "big")
    if isinstance(key1, bytes):
        key1 = int.from_bytes(key1, "big")
    if isinstance(key2, bytes):
        key2 = int.from_bytes(key2, "big")
    if isinstance(key3, bytes):
        key3 = int.from_bytes(key3, "big")

    # Step 1: Decrypt with K3
    temp1 = des_decrypt(ciphertext, key3)
    # Step 2: Encrypt with K2
    temp2 = des_encrypt(temp1, key2)
    # Step 3: Decrypt with K1
    plaintext = des_decrypt(temp2, key1)

    return plaintext


if __name__ == "__main__":
    # Test Triple DES
    plaintext = 0x0123456789ABCDEF
    key1 = 0x133457799BBCDFF1
    key2 = 0x07A1D0CE4E2546B8
    key3 = 0xF1E5D3C1B7A5938D

    print("=== Triple DES Test ===")
    print(f"Plaintext:  0x{plaintext:016X}")
    print(f"Key1:       0x{key1:016X}")
    print(f"Key2:       0x{key2:016X}")
    print(f"Key3:       0x{key3:016X}")

    ciphertext = triple_des_encrypt(plaintext, key1, key2, key3)
    print(f"Ciphertext: 0x{ciphertext:016X}")

    # Test round-trip
    plaintext_recovered = triple_des_decrypt(ciphertext, key1, key2, key3)
    print(f"Recovered:  0x{plaintext_recovered:016X}")
    print(f"Round-trip match: {plaintext_recovered == plaintext}")
