#!/usr/bin/env python3
"""
Script để sinh và lưu RSA keypair
Usage: python generate_rsa_keys.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "algorithms"))

from rsa_io import generate_and_save_keypair

if __name__ == "__main__":
    # Tạo thư mục keys nếu chưa có
    keys_dir = os.path.join(os.path.dirname(__file__), "keys")
    os.makedirs(keys_dir, exist_ok=True)

    pub_key_file = os.path.join(keys_dir, "rsa_public.json")
    priv_key_file = os.path.join(keys_dir, "rsa_private.json")

    print("=" * 70)
    print("RSA Key Pair Generation")
    print("=" * 70)
    print()
    print(f"Public key will be saved to: {pub_key_file}")
    print(f"Private key will be saved to: {priv_key_file}")
    print()

    # Ask for bit length
    while True:
        try:
            bit_length = int(
                input("Enter key size (256/512/1024/2048) [default 1024]: ") or "1024"
            )
            if bit_length not in [256, 512, 1024, 2048]:
                print("Invalid! Choose 256, 512, 1024, or 2048")
                continue
            break
        except ValueError:
            print("Invalid input! Enter a number")

    print()
    print(f"Generating {bit_length}-bit RSA keys... (this may take a while)")
    print()

    generate_and_save_keypair(pub_key_file, priv_key_file, bit_length=bit_length)

    print()
    print("=" * 70)
    print("✓ Keys generated successfully!")
    print("=" * 70)
