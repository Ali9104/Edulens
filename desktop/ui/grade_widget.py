from PyQt6.QtWidgets import QTableWidget, QLabel, QWidget,QVBoxLayout,QSplitter,QPushButton,QTableWidgetItem
from PyQt6.QtCore import Qt
from database import get_connection

class GradeWidget(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.setWindowTitle("Liste des Notes")
        self.resize(400,300)
        self.user_id = user_id

        self.table = QTableWidget(0,6)
        self.main_layout = QVBoxLayout(self)
        self.table.setHorizontalHeaderLabels(["ID", "Etudiant", "Matiere", "Note", "Semestre", "Date"])
        self.main_layout.addWidget(self.table)

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(" SELECT g.grade_id, s.Nom || ' ' || s.Prenom, g.Matiere, g.Note, g.Semestre, g.Date FROM grades g INNER JOIN students s ON g.student_id = s.student_id WHERE s.user_id = ?", (self.user_id,))
        rows = cursor.fetchall()
        for i,row in enumerate(rows):
            self.table.insertRow(i)
            self.table.setItem(i,0, QTableWidgetItem(str(row[0]))) 
            self.table.setItem(i,1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i,2, QTableWidgetItem(row[2]))
            self.table.setItem(i,3, QTableWidgetItem(str(row[3])))
            self.table.setItem(i,4, QTableWidgetItem(row[4]))
            self.table.setItem(i,5, QTableWidgetItem(str(row[5])))


        
