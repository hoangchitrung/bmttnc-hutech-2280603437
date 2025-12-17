import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QInputDialog,
)
from ui.DecryptAndEncrypt import Ui_MainWindow
import sys
from algorithms.aes_io import encrypt_file, decrypt_file
import binascii


class SecurityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Handle button event
        self.ui.btnOpen.clicked.connect(self.browse_input_file)
        self.ui.btnSaveAs.clicked.connect(self.save_as)
        self.ui.btnEncrypt.clicked.connect(self.encrypt_file)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_file)

    # Open file
    def browse_input_file(self):
        # Choose the file to open
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file to encrypt")

        if file_path:
            # Display file path on text field
            self.ui.txtInputFile.setText(file_path)

            # Suggest file path for output
            # Example: /home/user/doc.txt -> home/user/encrypted_doc.txt
            folder = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            new_name = f"encrypted_{file_name}"
            output_path = os.path.join(folder, new_name)

            # Display output file name after input
            self.ui.txtOutputFile.setText(output_path)

    # Save file
    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save output file as")
        if file_path:
            self.ui.txtOutputFile.setText(file_path)

    # Encrypt by calling algorithm function
    def encrypt_file(self):
        in_path = self.ui.txtInputFile.text()
        out_path = self.ui.txtOutputFile.text()
        if not in_path or not out_path:
            QMessageBox.warning(
                self, "Missing file", "Please choose input and output files first."
            )
            return
        key_text, ok = QInputDialog.getText(
            self, "AES Key", "Enter 16-byte key (hex 32 chars) or 16-char ASCII:"
        )
        if not ok:
            return
        key = None
        try:
            # hex?
            if len(key_text) == 32:
                key = binascii.unhexlify(key_text)
            elif len(key_text) == 16:
                key = key_text.encode("utf-8")
            else:
                raise ValueError("Invalid key length")
        except Exception:
            QMessageBox.critical(
                self, "Key error", "Key must be 32 hex chars or 16 ASCII chars"
            )
            return
        try:
            encrypt_file(in_path, out_path, key)
            QMessageBox.information(self, "Done", f"Encrypted saved to: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # Decrypt by calling algorithm function
    def decrypt_file(self):
        in_path = self.ui.txtInputFile.text()
        out_path = self.ui.txtOutputFile.text()
        if not in_path or not out_path:
            QMessageBox.warning(
                self, "Missing file", "Please choose input and output files first."
            )
            return
        key_text, ok = QInputDialog.getText(
            self, "AES Key", "Enter 16-byte key (hex 32 chars) or 16-char ASCII:"
        )
        if not ok:
            return
        key = None
        try:
            if len(key_text) == 32:
                key = binascii.unhexlify(key_text)
            elif len(key_text) == 16:
                key = key_text.encode("utf-8")
            else:
                raise ValueError("Invalid key length")
        except Exception:
            QMessageBox.critical(
                self, "Key error", "Key must be 32 hex chars or 16 ASCII chars"
            )
            return
        try:
            decrypt_file(in_path, out_path, key)
            QMessageBox.information(self, "Done", f"Decrypted saved to: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class Algorithms:
    def __init__(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = SecurityApp()
    window.show()
    sys.exit(app.exec_())
