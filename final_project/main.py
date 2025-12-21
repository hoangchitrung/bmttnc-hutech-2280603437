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
    QPushButton,
)
from PyQt5.QtCore import Qt
from ui.DecryptAndEncrypt import Ui_MainWindow
from ui.rsa_key_dialog import RSAKeyDialog
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
from triple_des import triple_des_encrypt, triple_des_decrypt
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

        # Connect Generate RSA Key button
        if hasattr(self.ui, "btnGenRSA"):
            self.ui.btnGenRSA.clicked.connect(self.generate_rsa_keypair)

        self.statusBar().showMessage("Ready")

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
        try:
            # Ask for three 8-byte keys
            key1_text, ok1 = QInputDialog.getText(
                self, "3DES Key 1", "Enter Key 1 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok1:
                return

            key2_text, ok2 = QInputDialog.getText(
                self, "3DES Key 2", "Enter Key 2 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok2:
                return

            key3_text, ok3 = QInputDialog.getText(
                self, "3DES Key 3", "Enter Key 3 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok3:
                return

            # Convert keys from string to bytes
            if len(key1_text) == 16:  # Hex format
                key1 = bytes.fromhex(key1_text)
            else:  # ASCII format
                key1 = key1_text.encode("utf-8")[:8]
                key1 += b"\x00" * (8 - len(key1))  # Pad if needed

            if len(key2_text) == 16:  # Hex format
                key2 = bytes.fromhex(key2_text)
            else:  # ASCII format
                key2 = key2_text.encode("utf-8")[:8]
                key2 += b"\x00" * (8 - len(key2))  # Pad if needed

            if len(key3_text) == 16:  # Hex format
                key3 = bytes.fromhex(key3_text)
            else:  # ASCII format
                key3 = key3_text.encode("utf-8")[:8]
                key3 += b"\x00" * (8 - len(key3))  # Pad if needed

            # Read plaintext file in binary mode
            with open(in_path, "rb") as f:
                plaintext = f.read()

            # Encrypt in 8-byte blocks with padding
            ciphertext = b""
            for i in range(0, len(plaintext), 8):
                block = plaintext[i : i + 8]
                # Pad with null bytes if block is incomplete
                if len(block) < 8:
                    block += b"\x00" * (8 - len(block))

                # Convert block to int, encrypt, convert back to bytes
                block_int = int.from_bytes(block, "big")
                encrypted_int = triple_des_encrypt(block_int, key1, key2, key3)
                encrypted_block = encrypted_int.to_bytes(8, "big")
                ciphertext += encrypted_block

            # Write ciphertext to output file
            with open(out_path, "wb") as f:
                f.write(ciphertext)

            QMessageBox.information(
                self, "Success", f"3DES encryption completed!\nOutput: {out_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"3DES encryption failed:\n{str(e)}")

    def _decrypt_3des(self, in_path, out_path):
        """Decrypt using 3DES (Triple DES)"""
        try:
            # Ask for three 8-byte keys
            key1_text, ok1 = QInputDialog.getText(
                self, "3DES Key 1", "Enter Key 1 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok1:
                return

            key2_text, ok2 = QInputDialog.getText(
                self, "3DES Key 2", "Enter Key 2 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok2:
                return

            key3_text, ok3 = QInputDialog.getText(
                self, "3DES Key 3", "Enter Key 3 (8-byte hex 16 chars or 8-char ASCII):"
            )
            if not ok3:
                return

            # Convert keys from string to bytes
            if len(key1_text) == 16:  # Hex format
                key1 = bytes.fromhex(key1_text)
            else:  # ASCII format
                key1 = key1_text.encode("utf-8")[:8]
                key1 += b"\x00" * (8 - len(key1))  # Pad if needed

            if len(key2_text) == 16:  # Hex format
                key2 = bytes.fromhex(key2_text)
            else:  # ASCII format
                key2 = key2_text.encode("utf-8")[:8]
                key2 += b"\x00" * (8 - len(key2))  # Pad if needed

            if len(key3_text) == 16:  # Hex format
                key3 = bytes.fromhex(key3_text)
            else:  # ASCII format
                key3 = key3_text.encode("utf-8")[:8]
                key3 += b"\x00" * (8 - len(key3))  # Pad if needed

            # Read ciphertext file in binary mode
            with open(in_path, "rb") as f:
                ciphertext = f.read()

            # Decrypt in 8-byte blocks
            plaintext = b""
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i : i + 8]

                # Convert block to int, decrypt, convert back to bytes
                block_int = int.from_bytes(block, "big")
                decrypted_int = triple_des_decrypt(block_int, key1, key2, key3)
                decrypted_block = decrypted_int.to_bytes(8, "big")
                plaintext += decrypted_block

            # Remove trailing null bytes (padding)
            plaintext = plaintext.rstrip(b"\x00")

            # Write plaintext to output file
            with open(out_path, "wb") as f:
                f.write(plaintext)

            QMessageBox.information(
                self, "Success", f"3DES decryption completed!\nOutput: {out_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"3DES decryption failed:\n{str(e)}")

    def generate_rsa_keypair(self):
        """Open dialog to generate RSA keypair"""
        try:
            dialog = RSAKeyDialog(self)
            if dialog.exec_() == dialog.Accepted:
                key_size, description = dialog.get_values()

                # Ask where to save keys
                save_dir = QFileDialog.getExistingDirectory(
                    self, "Select folder to save RSA keys"
                )

                if save_dir:
                    # Create file paths for public and private keys
                    public_key_file = os.path.join(
                        save_dir, f"rsa_{description}_public.json"
                    )
                    private_key_file = os.path.join(
                        save_dir, f"rsa_{description}_private.json"
                    )

                    # Show progress message (key generation can take a while)
                    QMessageBox.information(
                        self,
                        "Generating Keys",
                        f"Generating {key_size}-bit RSA keys...\n\n"
                        f"This may take a few moments depending on key size.\n"
                        f"Please wait...",
                    )

                    # Generate keypair (key_size is already int from dialog)
                    public_key, private_key = generate_and_save_keypair(
                        public_key_file, private_key_file, bit_length=key_size
                    )

                    QMessageBox.information(
                        self,
                        "Success",
                        f"RSA Key Generated!\n\n"
                        f"Key Size: {key_size} bits\n"
                        f"Description: {description}\n"
                        f"Public Key: {public_key_file}\n"
                        f"Private Key: {private_key_file}",
                    )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to generate RSA keys:\n{str(e)}"
            )

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
