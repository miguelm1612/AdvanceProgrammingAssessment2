
from ui_Login import Ui_Dialog
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox  # CHANGED
import sys
from Housing_Allocation_Ui import HousingAllocationApp


class MyLogin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.login_func)

    def login_func(self):
        if self.PassWord.text() == "Click123":
            QMessageBox.information(self, "Success", "Login successful!")
            self.accept()
            self.main_window = HousingAllocationApp()
            self.main_window.show()

        else:
            QMessageBox.warning(self, "Error", "Incorrect password!")
            self.PassWord.clear()
            self.PassWord.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = MyLogin()
    login.show()
    sys.exit(app.exec())