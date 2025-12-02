import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_generate.clicked.connect(self.call_api_gen_keys)
        self.ui.button_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.button_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.button_sign.clicked.connect(self.call_api_sign)
        self.ui.button_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public",
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private",
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    # Phương thức thực hiện Ký số (Sign)
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        # Lấy dữ liệu từ ô nhập liệu "Information"
        payload = {"message": self.ui.txt_infomation_text.toPlainText()}
        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị chữ ký trả về lên ô "Signature"
                self.ui.txt_signature_text.setText(data["signature"])

                # Hiển thị thông báo thành công
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    # Phương thức thực hiện Xác thực chữ ký (Verify)
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        # Lấy dữ liệu từ ô "Information" và "Signature"
        payload = {
            "message": self.ui.txt_infomation_text.toPlainText(),
            "signature": self.ui.txt_signature_text.toPlainText(),
        }
        try:
            # Gửi yêu cầu POST đến API
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Kiểm tra kết quả xác thực trả về từ Server
                if data["is_verified"]:
                    self.ui.txt_infomation_text.setPlainText("this is my signature")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Fail")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
