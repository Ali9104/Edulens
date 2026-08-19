from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QWidget,QVBoxLayout,QSplitter,QPushButton,QTableWidgetItem,QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QDateEdit
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDate
from database import get_connection
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

class StudentWidget(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.setWindowTitle("Liste Etudiant")
        self.resize(400, 300)
        self.user_id = user_id

        self.table = QTableWidget(0,5)
        self.main_layout = QVBoxLayout(self)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prenom", "Groupe", "Actions"])
        self.table.setColumnWidth(4,200)
        self.main_layout.addWidget(self.table)
        self.button_import_csv = QPushButton("Importer CSV")
        self.main_layout.addWidget(self.button_import_csv)
        self.button_import_csv.clicked.connect(self.import_csv)


    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE user_id = ?", (self.user_id,))
        rows = cursor.fetchall()
        for i,row in enumerate(rows):
            self.table.insertRow(i)
            self.table.setItem(i,0, QTableWidgetItem(str(row[0]))) 
            self.table.setItem(i,1, QTableWidgetItem(row[1]))
            self.table.setItem(i,2, QTableWidgetItem(row[2]))
            self.table.setItem(i,3, QTableWidgetItem(row[3]))

            student_id = row[0]
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            btn_note = QPushButton("Note")
            btn_absence = QPushButton("Absence")
            btn_rapport = QPushButton("Rapport")
            actions_layout.addWidget(btn_note)
            actions_layout.addWidget(btn_absence)
            actions_layout.addWidget(btn_rapport)
            self.table.setCellWidget(i, 4, actions_widget)
            btn_note.clicked.connect(lambda checked, sid=student_id: self.add_note(sid))
            btn_absence.clicked.connect(lambda checked, sid=student_id: self.add_absence(sid))
            btn_rapport.clicked.connect(lambda checked, sid=student_id: self.generate_rapport(sid))
    
    def import_csv(self):
        conn = get_connection()
        filename,_ = QFileDialog.getOpenFileName(self, "ouvrir un fichier ")  
        if not filename:
            return
        else:
            df = pd.read_csv(filename, sep = ",")
            print(df.columns)
            cursor = conn.cursor()
            for index, row in df.iterrows():
                nom = row['nom']
                prenom = row['prenom']
                groupe = row['groupe']
                cursor.execute("INSERT INTO students(Nom, Prenom, Groupe, user_id) VALUES (?, ?, ?, ?)", (nom, prenom, groupe, self.user_id))
            conn.commit()
            self.table.setRowCount(0)
            self.load_data()
    
    def add_note(self, student_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter une note")
        layout = QFormLayout(dialog)
    
        matiere = QLineEdit()
        note = QLineEdit()
        semestre = QComboBox()
        semestre.addItems(["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10"])
        date = QDateEdit()
        date.setDate(QDate.currentDate())
    
        layout.addRow("Matière :", matiere)
        layout.addRow("Note :", note)
        layout.addRow("Semestre :", semestre)
        layout.addRow("Date :", date)
    
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
    
        if dialog.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO grades(student_id, Matiere, Note, Semestre, Date) VALUES (?,?,?,?,?)",
            (student_id, matiere.text(), float(note.text()), semestre.currentText(), date.date().toString("yyyy-MM-dd")))
            conn.commit()
            conn.close()

    def add_absence(self, student_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter une absence")
        layout = QFormLayout(dialog)
    
        date = QDateEdit()
        date.setDate(QDate.currentDate())
        justifiee = QComboBox()
        justifiee.addItems(["Non", "Oui"])
    
        layout.addRow("Date :", date)
        layout.addRow("Justifiée :", justifiee)
    
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
    
        if dialog.exec() == QDialog.DialogCode.Accepted:
            conn = get_connection()
            cursor = conn.cursor()
            justifiee_val = 1 if justifiee.currentText() == "Oui" else 0
            cursor.execute("INSERT INTO Abscence(student_id, Date, Justifiee) VALUES (?,?,?)",
            (student_id, date.date().toString("yyyy-MM-dd"), justifiee_val))
            conn.commit()
            conn.close()

    def generate_rapport(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        students = cursor.fetchone()
        cursor.execute("SELECT g.Matiere, g.Note, g.Semestre FROM grades g WHERE g.student_id = ?", (student_id,))
        grades = cursor.fetchall()
        if not grades :
            return "etudiant a pas de note"
        filepath = os.path.join(os.path.dirname(__file__), '..', f"rapport_{students[1]}_{students[2]}.pdf")
        doc = SimpleDocTemplate(filepath, pagesize = A4)
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_titre = styles["Title"]
        story = []
        story.append(Spacer(1, 12))
        story.append(Paragraph("Rapport EduLens", style_titre))
        nom = students[1]
        prenom = students[2]
        groupe = students[3]
        story.append(Paragraph(f"Nom : {nom}", style_normal))
        story.append(Paragraph(f"Prenom : {prenom}", style_normal))
        story.append(Paragraph(f"Groupe : {groupe}", style_normal))
        notes = [g[1] for g in grades]
        average = round(sum(notes)/len(notes), 2) if notes else 0
        story.append(Paragraph(f"Moyenne : {average}", style_normal))
        semestres = {}
        for grade in grades:
            if grade[2] not in semestres:
                semestres[grade[2]] = []
            semestres[grade[2]].append(grade)
        for semestre, grades in semestres.items():
            story.append(Paragraph(f"Semestre : {semestre}", style_titre))
            for g in grades:
                story.append(Paragraph(f"{g[0]} : {g[1]}/20", style_normal))
            notes_sem = [g[1] for g in grades]
            moyenne_sem = round(sum(notes_sem)/len(notes_sem), 2)
            story.append(Paragraph(f"Moyenne du semestre : {moyenne_sem}", style_normal))
        doc.build(story)
        os.startfile(filepath)
        return filepath
            




            
  

        



    