import os
import rsa

class RSACipher:
    def __init__(self):
        # Kiểm tra và tạo thư mục keys nếu chưa tồn tại (theo cấu trúc trang 12)
        if not os.path.exists("cipher/rsa/keys"):
            os.makedirs("cipher/rsa/keys")

    def generate_keys(self):
        # Tạo cặp key 1024 bit
        (public_key, private_key) = rsa.newkeys(1024)

        # Lưu Public Key format PEM
        with open("cipher/rsa/keys/publicKey.pem", "wb") as p:
            p.write(public_key.save_pkcs1("PEM"))

        # Lưu Private Key format PEM
        with open("cipher/rsa/keys/privateKey.pem", "wb") as p:
            p.write(private_key.save_pkcs1("PEM"))

        return public_key, private_key

    def load_keys(self):
        # Đọc Private Key từ file
        with open("cipher/rsa/keys/privateKey.pem", "rb") as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())

        # Đọc Public Key từ file
        with open("cipher/rsa/keys/publicKey.pem", "rb") as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())

        return private_key, public_key

    def encrypt(self, message, key):
        # Mã hóa message (cần encode sang bytes)
        return rsa.encrypt(message.encode("utf-8"), key)

    def decrypt(self, ciphertext, key):
        # Giải mã và decode về string
        try:
            return rsa.decrypt(ciphertext, key).decode("utf-8")
        except:
            return "Decryption Failed"

    def sign(self, message, key):
        # Ký số sử dụng thuật toán băm SHA-256
        return rsa.sign(message.encode("utf-8"), key, "SHA-256")

    def verify(self, message, signature, key):
        # Xác thực chữ ký
        try:
            rsa.verify(message.encode("utf-8"), signature, key)
            return True
        except rsa.VerificationError:
            return False