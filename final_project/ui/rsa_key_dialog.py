"""
RSA Key Generation Dialog - Nhập thông tin sinh khóp RSA
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt


class RSAKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_size = None
        self.description = None
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện dialog"""
        self.setWindowTitle("RSA Key Generation")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Row 1: Key Size
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Key Size:"))
        self.combo_key_size = QComboBox()
        self.combo_key_size.addItems(["512", "1024", "2048"])
        self.combo_key_size.setCurrentText("1024")  # Default (faster for testing)
        row1.addWidget(self.combo_key_size)
        layout.addLayout(row1)

        # Row 2: Description
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Description:"))
        self.txt_description = QLineEdit()
        self.txt_description.setPlaceholderText("Ví dụ: Server RSA Key")
        row2.addWidget(self.txt_description)
        layout.addLayout(row2)

        # Row 3: Buttons
        row3 = QHBoxLayout()
        btn_ok = QPushButton("Generate")
        btn_cancel = QPushButton("Cancel")
        row3.addWidget(btn_ok)
        row3.addWidget(btn_cancel)
        layout.addLayout(row3)

        # Connect signals
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        self.setLayout(layout)

    def accept(self):
        """Xác nhận và lưu dữ liệu"""
        self.key_size = int(self.combo_key_size.currentText())
        self.description = self.txt_description.text().strip()

        if not self.description:
            self.description = f"RSA-{self.key_size}"

        super().accept()

    def get_values(self):
        """Trả về key_size và description"""
        return self.key_size, self.description
