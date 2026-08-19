import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.login_widget import LoginWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWidget()
    login.show()
    sys.exit(app.exec())