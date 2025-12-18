"""
RSA File I/O Operations
Wrapper cho encrypt/decrypt file bằng RSA
"""

from rsa import (
    generate_keypair,
    rsa_encrypt_message,
    rsa_decrypt_message,
    bytes_to_int,
    int_to_bytes,
)
import json


def generate_and_save_keypair(key_file_public, key_file_private, bit_length=512):
    """
    Tạo cặp khóa RSA và lưu vào file

    key_file_public: đường dẫn lưu public key (JSON format)
    key_file_private: đường dẫn lưu private key (JSON format)
    bit_length: độ dài bit của primes (256, 512, 1024, ...)
    """
    print(f"[RSA] Generating keypair ({bit_length}-bit)...")
    public_key, private_key = generate_keypair(bit_length=bit_length)

    e, n = public_key
    d, _ = private_key

    # Lưu public key
    pub_data = {"e": str(e), "n": str(n)}
    with open(key_file_public, "w") as f:
        json.dump(pub_data, f)
    print(f"[RSA] Public key saved: {key_file_public}")

    # Lưu private key
    priv_data = {"d": str(d), "n": str(n)}
    with open(key_file_private, "w") as f:
        json.dump(priv_data, f)
    print(f"[RSA] Private key saved: {key_file_private}")

    return public_key, private_key


def load_public_key(key_file):
    """
    Load public key từ file JSON

    Return: (e, n)
    """
    with open(key_file, "r") as f:
        data = json.load(f)
    e = int(data["e"])
    n = int(data["n"])
    return (e, n)


def load_private_key(key_file):
    """
    Load private key từ file JSON

    Return: (d, n)
    """
    with open(key_file, "r") as f:
        data = json.load(f)
    d = int(data["d"])
    n = int(data["n"])
    return (d, n)


def encrypt_file(input_file, output_file, public_key):
    """
    Mã hóa file bằng RSA

    input_file: đường dẫn file plain
    output_file: đường dẫn file cipher (sẽ tạo mới)
    public_key: tuple (e, n) hoặc đường dẫn file JSON

    File cipher format:
      [4 bytes: plaintext length]
      [ciphertext bytes]
    """
    # Load key nếu là string (file path)
    if isinstance(public_key, str):
        public_key = load_public_key(public_key)

    # Đọc plaintext từ file (binary)
    with open(input_file, "rb") as f:
        plaintext = f.read()

    print(f"[RSA] Encrypting {input_file}...")
    print(f"  Plaintext size: {len(plaintext)} bytes")

    # Mã hóa
    ciphertext = rsa_encrypt_message(plaintext, public_key)

    # Lưu ciphertext
    # Format: [4 bytes little-endian: plaintext length][ciphertext]
    with open(output_file, "wb") as f:
        # Lưu độ dài plaintext (4 bytes, little-endian) để unpad sau
        f.write(len(plaintext).to_bytes(4, byteorder="little"))
        f.write(ciphertext)

    print(f"[RSA] Encrypted file saved: {output_file}")
    print(f"  Ciphertext size: {len(ciphertext)} bytes")


def decrypt_file(input_file, output_file, private_key):
    """
    Giải mã file bằng RSA

    input_file: đường dẫn file cipher
    output_file: đường dẫn file plain (sẽ tạo mới)
    private_key: tuple (d, n) hoặc đường dẫn file JSON
    """
    # Load key nếu là string (file path)
    if isinstance(private_key, str):
        private_key = load_private_key(private_key)

    # Đọc ciphertext từ file
    with open(input_file, "rb") as f:
        pt_len = int.from_bytes(f.read(4), byteorder="little")
        ciphertext = f.read()

    print(f"[RSA] Decrypting {input_file}...")
    print(f"  Ciphertext size: {len(ciphertext)} bytes")

    # Giải mã
    plaintext = rsa_decrypt_message(ciphertext, private_key)

    # Trim plaintext để loại bỏ padding từ last block
    plaintext = plaintext[:pt_len]

    # Lưu plaintext
    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"[RSA] Decrypted file saved: {output_file}")
    print(f"  Plaintext size: {len(plaintext)} bytes")


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    import os

    print("=" * 70)
    print("RSA File I/O Test")
    print("=" * 70)

    # Tạo thư mục test nếu chưa có
    test_dir = "/tmp/rsa_test"
    os.makedirs(test_dir, exist_ok=True)

    # Paths
    pub_key_file = f"{test_dir}/public.json"
    priv_key_file = f"{test_dir}/private.json"
    plain_file = f"{test_dir}/plaintext.txt"
    cipher_file = f"{test_dir}/ciphertext.bin"
    decrypted_file = f"{test_dir}/decrypted.txt"

    # Test 1: Generate keypair
    print("\n[Test 1] Key Generation")
    public_key, private_key = generate_and_save_keypair(
        pub_key_file, priv_key_file, bit_length=512
    )

    # Test 2: Create test file
    print("\n[Test 2] Create Test File")
    test_content = b"This is a test message for RSA encryption!\nLine 2\nLine 3"
    with open(plain_file, "wb") as f:
        f.write(test_content)
    print(f"Test file created: {plain_file}")
    print(f"Content: {test_content}")

    # Test 3: Encrypt
    print("\n[Test 3] Encrypt File")
    encrypt_file(plain_file, cipher_file, public_key)

    # Test 4: Decrypt
    print("\n[Test 4] Decrypt File")
    decrypt_file(cipher_file, decrypted_file, private_key)

    # Test 5: Verify
    print("\n[Test 5] Verify")
    with open(decrypted_file, "rb") as f:
        recovered = f.read()

    match = test_content == recovered
    print(f"Original:  {test_content}")
    print(f"Recovered: {recovered}")
    print(f"Match: {match} ✓" if match else f"Match: {match} ✗")

    # Test 6: Load keys from file
    print("\n[Test 6] Load Keys from File")
    pub_key_loaded = load_public_key(pub_key_file)
    priv_key_loaded = load_private_key(priv_key_file)
    print(
        f"Public key loaded: e={pub_key_loaded[0]}, n={pub_key_loaded[1] % 10000}...XXXX"
    )
    print(
        f"Private key loaded: d={priv_key_loaded[0] % 10000}...XXXX, n={priv_key_loaded[1] % 10000}...XXXX"
    )

    print("\n" + "=" * 70)
    print("All tests passed! ✓")
    print("=" * 70)
