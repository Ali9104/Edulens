from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from werkzeug.security import check_password_hash
from database import get_connection
from ui.main_window import MainWindow

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduLens — Connexion")
        self.resize(400, 300)

        self.main_layout = QVBoxLayout(self)
        self.label_title = QLabel("EduLens")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Email")        
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.buttonlogin = QPushButton("Se connecter")
        self.buttonlogin.clicked.connect(self.check_login)
        self.main_layout.addWidget(self.label_title)
        self.main_layout.addWidget(self.email)
        self.main_layout.addWidget(self.password)
        self.main_layout.addWidget(self.buttonlogin)

    def check_login(self):
        email = self.email.text()
        password = self.password.text()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result and check_password_hash(result[3], password):
            QMessageBox.information(self, "Succès", f"Bienvenue {result[1]} !")
            self.main_window = MainWindow(result[0])
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Erreur", "Email ou mot de passe incorrect.")