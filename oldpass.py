from ui_Login import Ui_Dialog
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
import sys


class MyLogin(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.login_func)

    def login_func(self):
        password = self.PassWord.text()  # Assuming PassWord is a QLineEdit

        # Replace with your actual login logic
        if password == "Click123":
            QMessageBox.information(self, "Success", "Login successful!")
            self.accept()  # Close the dialog with success status
        else:
            QMessageBox.warning(self, "Error", "Incorrect password!")
            self.PassWord.clear()  # Clear the password field
            self.PassWord.setFocus()  # Set focus back to password field


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = MyLogin()
    login.show()
    sys.exit(app.exec_())



