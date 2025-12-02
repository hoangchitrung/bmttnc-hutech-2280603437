import ecdsa
import os


class ECCCipher:
    def __init__(self):
        # Kiểm tra và tạo thư mục keys nếu chưa tồn tại
        if not os.path.exists("cipher/ecc/keys"):
            os.makedirs("cipher/ecc/keys")

    def generate_keys(self):
        # Tạo khóa riêng tư (Signing Key)
        sk = ecdsa.SigningKey.generate()
        # Lấy khóa công khai (Verifying Key) từ khóa riêng
        vk = sk.get_verifying_key()

        # Lưu Private Key
        with open("cipher/ecc/keys/privateKey.pem", "wb") as p:
            p.write(sk.to_pem())

        # Lưu Public Key
        with open("cipher/ecc/keys/publicKey.pem", "wb") as p:
            p.write(vk.to_pem())

        return sk, vk

    def load_keys(self):
        # Load Private Key
        with open("cipher/ecc/keys/privateKey.pem", "rb") as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        # Load Public Key
        with open("cipher/ecc/keys/publicKey.pem", "rb") as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk

    def sign(self, message, key):
        # Ký dữ liệu bằng khóa riêng tư
        return key.sign(message.encode("ascii"))

    def verify(self, message, signature, key):
        # Xác thực chữ ký
        try:
            return key.verify(signature, message.encode("ascii"))
        except ecdsa.BadSignatureError:
            return False
