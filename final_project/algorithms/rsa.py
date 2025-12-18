"""
RSA (Rivest-Shamir-Adleman) Encryption Implementation
From scratch - NO external crypto libraries

RSA Concept (Dễ hiểu):
  1. Chọn 2 số nguyên tố lớn p, q
  2. Tính n = p * q
  3. Tính φ(n) = (p-1) * (q-1)
  4. Chọn e (public exponent) sao cho: 1 < e < φ(n) và gcd(e, φ(n)) = 1
  5. Tính d (private exponent) sao cho: e*d ≡ 1 (mod φ(n))

  Public Key = (e, n)   - Công khai, dùng để encrypt
  Private Key = (d, n)  - Bí mật, dùng để decrypt

  Encrypt: C = M^e mod n
  Decrypt: M = C^d mod n
"""

import random
import math


def gcd(a, b):
    """Tính ước chung lớn nhất (Greatest Common Divisor)"""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm - Tính GCD và coefficients x, y
    sao cho: a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1

    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return gcd_val, x, y


def mod_inverse(e, phi):
    """
    Tính modular inverse: d sao cho e*d ≡ 1 (mod phi)
    Dùng Extended GCD
    """
    gcd_val, x, _ = extended_gcd(e, phi)

    if gcd_val != 1:
        raise ValueError(f"Modular inverse không tồn tại (gcd({e}, {phi}) = {gcd_val})")

    return x % phi


def is_prime_miller_rabin(n, k=40):
    """
    Miller-Rabin Primality Test - Kiểm tra số n có phải số nguyên tố không

    n: số cần kiểm tra
    k: số lần kiểm tra (càng cao càng chính xác)

    Return: True nếu n là số nguyên tố (với xác suất 1 - 4^-k), False nếu hợp số
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Viết n-1 = 2^r * d (d lẻ)
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Chạy k lần kiểm tra
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # a^d mod n (dùng modular exponentiation)

        if x == 1 or x == n - 1:
            continue

        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True


def generate_prime(bit_length):
    """
    Sinh số nguyên tố ngẫu nhiên có độ dài bit_length bit

    bit_length: số bits mong muốn (e.g., 512, 1024)
    """
    while True:
        num = random.getrandbits(bit_length)
        # Đặt bit cao nhất = 1 để đảm bảo bit_length đủ
        num |= 1 << (bit_length - 1)
        # Đặt bit thấp nhất = 1 để đảm bảo số lẻ
        num |= 1

        if is_prime_miller_rabin(num):
            return num


def generate_keypair(bit_length=512):
    """
    Tạo cặp khóa RSA (public, private)

    bit_length: độ dài bit của mỗi số nguyên tố p, q
                => n sẽ có ~2*bit_length bits

    Return: (public_key, private_key)
    public_key = (e, n)
    private_key = (d, n)
    """
    print(f"[RSA] Generating {bit_length}-bit primes...")

    # Bước 1: Sinh 2 số nguyên tố lớn khác nhau
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)

    while p == q:
        q = generate_prime(bit_length)

    # Bước 2: Tính n = p * q
    n = p * q

    # Bước 3: Tính φ(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)

    # Bước 4: Chọn e (thường là 65537 - số nguyên tố phổ biến)
    e = 65537

    # Nếu e chia hết φ(n), tìm e khác
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Bước 5: Tính d = e^-1 mod φ(n)
    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    print(f"[RSA] Key generation complete")
    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = {n} ({n.bit_length()} bits)")
    print(f"  φ(n) = {phi}")
    print(f"  e = {e}")
    print(f"  d = {d}")

    return public_key, private_key


def rsa_encrypt(message, public_key):
    """
    Mã hóa RSA

    message: số nguyên (plaintext) < n
    public_key: tuple (e, n)

    Return: ciphertext (số nguyên)
    """
    e, n = public_key

    if message >= n:
        raise ValueError(f"Message {message} must be < n {n}")

    ciphertext = pow(message, e, n)  # C = M^e mod n
    return ciphertext


def rsa_decrypt(ciphertext, private_key):
    """
    Giải mã RSA

    ciphertext: số nguyên (ciphertext)
    private_key: tuple (d, n)

    Return: plaintext (số nguyên)
    """
    d, n = private_key

    plaintext = pow(ciphertext, d, n)  # M = C^d mod n
    return plaintext


def bytes_to_int(data):
    """Chuyển bytes thành integer (big-endian)"""
    return int.from_bytes(data, byteorder="big")


def int_to_bytes(num, byte_length):
    """Chuyển integer thành bytes (big-endian)"""
    return num.to_bytes(byte_length, byteorder="big")


def rsa_encrypt_message(message_bytes, public_key, block_size=None):
    """
    Mã hóa RSA với padding

    message_bytes: plaintext (bytes)
    public_key: (e, n)
    block_size: kích thước khối (nếu None, sẽ tính từ n)

    Return: ciphertext (bytes)

    Lưu ý: Đây là PKCS#1 v1.5 simplified (không dùng thư viện, nên đơn giản hơn)
    """
    e, n = public_key

    if block_size is None:
        # block_size = (n.bit_length() - 1) // 8
        block_size = (n.bit_length() + 7) // 8 - 1  # Để lạc an toàn

    # Chia message thành chunks
    ciphertext = b""
    for i in range(0, len(message_bytes), block_size):
        chunk = message_bytes[i : i + block_size]
        # Pad chunk: thêm 0x00 ở đầu để đảm bảo < n
        chunk_padded = b"\x00" + chunk
        msg_int = bytes_to_int(chunk_padded)
        ct_int = rsa_encrypt(msg_int, public_key)
        ct_byte_len = (n.bit_length() + 7) // 8
        ciphertext += int_to_bytes(ct_int, ct_byte_len)

    return ciphertext


def rsa_decrypt_message(ciphertext_bytes, private_key):
    """
    Giải mã RSA với unpadding

    ciphertext_bytes: ciphertext (bytes)
    private_key: (d, n)

    Return: plaintext (bytes)
    """
    d, n = private_key

    ct_byte_len = (n.bit_length() + 7) // 8
    plaintext = b""

    # Chia ciphertext thành chunks
    for i in range(0, len(ciphertext_bytes), ct_byte_len):
        chunk = ciphertext_bytes[i : i + ct_byte_len]
        ct_int = bytes_to_int(chunk)
        pt_int = rsa_decrypt(ct_int, private_key)

        # Unpad: loại bỏ leading zeros (padding)
        # pt_int được mã hóa từ (0x00 || original_data)
        # Vì vậy ta cần find vị trí của byte đầu tiên không phải 0
        pt_bytes = int_to_bytes(pt_int, ct_byte_len)

        # Tìm index của byte đầu tiên không phải 0x00
        j = 0
        while j < len(pt_bytes) and pt_bytes[j] == 0:
            j += 1

        plaintext += pt_bytes[j:]

    return plaintext


# ============================================================================
# TEST & DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RSA Encryption Test")
    print("=" * 70)

    # Test 1: Key generation (dùng 256-bit prime cho test nhanh)
    print("\n[Test 1] Key Generation (256-bit primes)")
    public_key, private_key = generate_keypair(bit_length=256)
    e, n = public_key
    d, _ = private_key

    print(f"\nPublic Key:  (e={e}, n={n})")
    print(f"Private Key: (d={d}, n={n})")

    # Test 2: Simple number encryption/decryption
    print("\n" + "=" * 70)
    print("[Test 2] Simple Message Encryption/Decryption")
    print("=" * 70)

    message = 123456789
    print(f"Original message: {message}")

    if message < n:
        ciphertext = rsa_encrypt(message, public_key)
        print(f"Ciphertext:       {ciphertext}")

        decrypted = rsa_decrypt(ciphertext, private_key)
        print(f"Decrypted:        {decrypted}")

        match = message == decrypted
        print(f"Match: {match} ✓" if match else f"Match: {match} ✗")
    else:
        print(f"Message too large (>= n={n})")

    # Test 3: Bytes message encryption/decryption
    print("\n" + "=" * 70)
    print("[Test 3] Bytes Message Encryption/Decryption")
    print("=" * 70)

    test_message = b"Hello RSA!"
    print(f"Original message: {test_message}")

    ciphertext_bytes = rsa_encrypt_message(test_message, public_key)
    print(f"Ciphertext (hex): {ciphertext_bytes.hex()}")

    decrypted_bytes = rsa_decrypt_message(ciphertext_bytes, private_key)
    print(f"Decrypted:        {decrypted_bytes}")

    match = test_message == decrypted_bytes
    print(f"Match: {match} ✓" if match else f"Match: {match} ✗")

    # Test 4: Longer message
    print("\n" + "=" * 70)
    print("[Test 4] Long Message Test")
    print("=" * 70)

    long_message = b"This is a longer message to test RSA encryption and decryption!"
    print(f"Original length: {len(long_message)} bytes")
    print(f"Original: {long_message}")

    ct = rsa_encrypt_message(long_message, public_key)
    print(f"Ciphertext length: {len(ct)} bytes")

    pt = rsa_decrypt_message(ct, private_key)
    print(f"Decrypted: {pt}")

    match = long_message == pt
    print(f"Match: {match} ✓" if match else f"Match: {match} ✗")
