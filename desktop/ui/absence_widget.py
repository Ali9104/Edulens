from PyQt6.QtWidgets import QTableWidget, QLabel, QWidget,QVBoxLayout,QSplitter,QPushButton,QTableWidgetItem
from PyQt6.QtCore import Qt
from database import get_connection

class AbsenceWidget(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.setWindowTitle("Liste des Absences")
        self.resize(400,300)
        self.user_id = user_id

        self.table = QTableWidget(0,4)
        self.main_layout = QVBoxLayout(self)
        self.table.setHorizontalHeaderLabels(["ID", "Etudiant", "Date", "Justifiee"])
        self.main_layout.addWidget(self.table)

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT a.absence_id, s.nom || ' ' || s.prenom,  a.date, a.Justifiee  FROM Abscence a INNER JOIN students s ON a.student_id = s.student_id WHERE s.user_id = ?", (self.user_id,))
        rows = cursor.fetchall()
        for i,row in enumerate(rows):
            self.table.insertRow(i)
            self.table.setItem(i,0, QTableWidgetItem(str(row[0]))) 
            self.table.setItem(i,1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i,2, QTableWidgetItem(str(row[2])))
            self.table.setItem(i,3, QTableWidgetItem(str(row[3])))