from PyQt6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QListWidget, QMessageBox
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

import os


class RapportWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Rapports PDF")
        self.resize(500, 400)

        self.main_layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.main_layout.addWidget(self.list_widget)
        self.button_voir_pdf = QPushButton("Ouvrir PDF")
        self.main_layout.addWidget(self.button_voir_pdf)
        self.button_voir_pdf.clicked.connect(self.voir_pdf)
        self.load_pdf()

    def load_pdf(self):
        reports_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        fichiers = [
            f for f in os.listdir(reports_dir)
            if f.startswith("rapport_") and f.endswith(".pdf")
        ]
        self.list_widget.clear()
        for fichier in fichiers:
            self.list_widget.addItem(fichier)

    def voir_pdf(self):
        item = self.list_widget.currentItem()
        if item is None:
            QMessageBox.warning(self, "Erreur", "Aucun fichier sélectionné")
            return
        nom_fichier = item.text()
        chemin_pdf = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                nom_fichier
            )
        )
        if os.path.exists(chemin_pdf):
            QDesktopServices.openUrl(
                QUrl.fromLocalFile(chemin_pdf)
            )
        else:
            QMessageBox.warning(self, "Erreur", "Fichier introuvable")