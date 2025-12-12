import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from ui.DecryptAndEncrypt import Ui_MainWindow
import sys


class SecurityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Handle button event
        self.ui.btnOpen.clicked.connect(self.browse_input_file)  # Process to open file
        # self.ui.btnSaveAs.clicked.connect() # process to save the file
        # self.ui.btnDecrypt.clicked.connect() # call the encrypt function from the radio
        # self.ui.btnEncrypt.clicked.connect()  # call the decrypt function from the radio

    # Open file
    def browse_input_file(self):
        # Choose the file to open
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file to encrypt")

        if file_path:
            # Display file path on text field
            self.ui.txtInputFile.setText(file_path)

            # Suggest file path for output
            # Example: /home/user/doct.txt -> home/user/encrypted_doc.txt
            folder = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            new_name = f"encrypted_{file_name}"
            output_path = os.path.join(folder, new_name)

            # Display output file name after input
            self.ui.txtOutputFile.setText(output_path)

    # Save file
    def save_as(self):
        pass

    # Encrypt by calling algorithm function
    def encrypt_file(self):
        pass

    # Decrypt by calling algorithm function
    def decrypt_file(self):
        pass


class Algorithms:
    def __init__(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = SecurityApp()
    window.show()
    sys.exit(app.exec_())
