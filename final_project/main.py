import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import Qt
from ui.DecryptAndEncrypt import Ui_MainWindow
import sys
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "algorithms"))

from aes_io import (
    encrypt_file as aes_encrypt_file,
    decrypt_file as aes_decrypt_file,
)
from rsa_io import (
    encrypt_file as rsa_encrypt_file,
    decrypt_file as rsa_decrypt_file,
    load_public_key,
    load_private_key,
    generate_and_save_keypair,
)
from des import des_encrypt, des_decrypt
import binascii


class SecurityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Algorithm selection
        self.algorithm = "AES"  # Default: AES

        # Connect radio buttons
        self.ui.rdoAes.toggled.connect(
            lambda checked: self.on_algorithm_selected("AES", checked)
        )
        self.ui.rdoDes.toggled.connect(
            lambda checked: self.on_algorithm_selected("DES", checked)
        )
        self.ui.rdoTripleDes.toggled.connect(
            lambda checked: self.on_algorithm_selected("3DES", checked)
        )
        self.ui.rdoRSA.toggled.connect(
            lambda checked: self.on_algorithm_selected("RSA", checked)
        )

        # Set AES as default
        self.ui.rdoAes.setChecked(True)

        # Handle button event
        self.ui.btnOpen.clicked.connect(self.browse_input_file)
        self.ui.btnSaveAs.clicked.connect(self.save_as)
        self.ui.btnEncrypt.clicked.connect(self.encrypt_file)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_file)

    def on_algorithm_selected(self, algo_name, checked):
        """Called when a radio button is selected"""
        if checked:
            self.set_algorithm(algo_name)

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

        try:
            if self.algorithm == "AES":
                self._encrypt_aes(in_path, out_path)
            elif self.algorithm == "DES":
                self._encrypt_des(in_path, out_path)
            elif self.algorithm == "3DES":
                self._encrypt_3des(in_path, out_path)
            else:  # RSA
                self._encrypt_rsa(in_path, out_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _encrypt_aes(self, in_path, out_path):
        """Encrypt using AES"""
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

        aes_encrypt_file(in_path, out_path, key)
        QMessageBox.information(self, "Done", f"AES Encrypted: {out_path}")

    def _encrypt_rsa(self, in_path, out_path):
        """Encrypt using RSA"""
        # Ask for public key file
        key_file, _ = QFileDialog.getOpenFileName(
            self, "Choose RSA Public Key File", filter="JSON files (*.json)"
        )
        if not key_file:
            return

        try:
            public_key = load_public_key(key_file)
            rsa_encrypt_file(in_path, out_path, public_key)
            QMessageBox.information(self, "Done", f"RSA Encrypted: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"RSA encryption failed: {str(e)}")

    # Decrypt by calling algorithm function
    def decrypt_file(self):
        in_path = self.ui.txtInputFile.text()
        out_path = self.ui.txtOutputFile.text()
        if not in_path or not out_path:
            QMessageBox.warning(
                self, "Missing file", "Please choose input and output files first."
            )
            return

        try:
            if self.algorithm == "AES":
                self._decrypt_aes(in_path, out_path)
            elif self.algorithm == "DES":
                self._decrypt_des(in_path, out_path)
            elif self.algorithm == "3DES":
                self._decrypt_3des(in_path, out_path)
            else:  # RSA
                self._decrypt_rsa(in_path, out_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _decrypt_aes(self, in_path, out_path):
        """Decrypt using AES"""
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

        aes_decrypt_file(in_path, out_path, key)
        QMessageBox.information(self, "Done", f"AES Decrypted: {out_path}")

    def _decrypt_rsa(self, in_path, out_path):
        """Decrypt using RSA"""
        # Ask for private key file
        key_file, _ = QFileDialog.getOpenFileName(
            self, "Choose RSA Private Key File", filter="JSON files (*.json)"
        )
        if not key_file:
            return

        try:
            private_key = load_private_key(key_file)
            rsa_decrypt_file(in_path, out_path, private_key)
            QMessageBox.information(self, "Done", f"RSA Decrypted: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"RSA decryption failed: {str(e)}")

    def _encrypt_des(self, in_path, out_path):
        """Encrypt using DES"""
        key_text, ok = QInputDialog.getText(
            self, "DES Key", "Enter 8-byte key (hex 16 chars) or 8-char ASCII:"
        )
        if not ok:
            return

        try:
            # Convert key to bytes
            if len(key_text) == 16:  # Hex format
                key = binascii.unhexlify(key_text)
            elif len(key_text) == 8:  # ASCII format
                key = key_text.encode("utf-8")
            else:
                raise ValueError("Invalid key length")

            # Read input file
            with open(in_path, "rb") as f:
                plaintext_bytes = f.read()

            # Encrypt: DES works on 8-byte blocks
            ciphertext = b""
            for i in range(0, len(plaintext_bytes), 8):
                block = plaintext_bytes[i : i + 8]
                # Pad last block if necessary
                if len(block) < 8:
                    block = block + b"\x00" * (8 - len(block))

                # Convert to integers and encrypt
                pt_int = int.from_bytes(block, "big")
                key_int = int.from_bytes(key, "big")
                ct_int = des_encrypt(pt_int, key_int)
                ciphertext += ct_int.to_bytes(8, "big")

            # Write output file
            with open(out_path, "wb") as f:
                f.write(ciphertext)

            QMessageBox.information(self, "Done", f"DES Encrypted: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DES encryption failed: {str(e)}")

    def _decrypt_des(self, in_path, out_path):
        """Decrypt using DES"""
        key_text, ok = QInputDialog.getText(
            self, "DES Key", "Enter 8-byte key (hex 16 chars) or 8-char ASCII:"
        )
        if not ok:
            return

        try:
            # Convert key to bytes
            if len(key_text) == 16:  # Hex format
                key = binascii.unhexlify(key_text)
            elif len(key_text) == 8:  # ASCII format
                key = key_text.encode("utf-8")
            else:
                raise ValueError("Invalid key length")

            # Read input file
            with open(in_path, "rb") as f:
                ciphertext_bytes = f.read()

            # Decrypt: Process 8-byte blocks
            plaintext = b""
            for i in range(0, len(ciphertext_bytes), 8):
                block = ciphertext_bytes[i : i + 8]
                if len(block) < 8:
                    break  # Skip incomplete blocks

                # Convert to integers and decrypt
                ct_int = int.from_bytes(block, "big")
                key_int = int.from_bytes(key, "big")
                pt_int = des_decrypt(ct_int, key_int)
                plaintext += pt_int.to_bytes(8, "big")

            # Remove trailing null padding
            plaintext = plaintext.rstrip(b"\x00")

            # Write output file
            with open(out_path, "wb") as f:
                f.write(plaintext)

            QMessageBox.information(self, "Done", f"DES Decrypted: {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DES decryption failed: {str(e)}")

    def _encrypt_3des(self, in_path, out_path):
        """Encrypt using 3DES (Triple DES)"""
        QMessageBox.information(self, "3DES", "3DES coming soon!")

    def _decrypt_3des(self, in_path, out_path):
        """Decrypt using 3DES (Triple DES)"""
        QMessageBox.information(self, "3DES", "3DES coming soon!")

    def set_algorithm(self, algo_name):
        """Set the current algorithm (AES or RSA)"""
        if algo_name in ["AES", "RSA", "DES", "3DES"]:
            self.algorithm = algo_name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = SecurityApp()
    window.show()
    sys.exit(app.exec_())
