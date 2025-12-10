from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.DecryptAndEncrypt import Ui_MainWindow
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
