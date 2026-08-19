from PyQt6.QtWidgets import QTableWidget, QLabel, QWidget,QVBoxLayout,QSplitter,QPushButton,QTableWidgetItem,QHBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from database import get_connection



class DashboardWidget(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(400,300)
        self.user_id = user_id

        self.main_layout = QVBoxLayout(self)
        self.stats_layout = QHBoxLayout()
        self.label_total_student = QLabel("Total etudiant")
        self.label_moyenne_generale = QLabel("Moyenne generale")
        self.label_taux_absence = QLabel("Taux Absence")
        self.label_student_risk = QLabel("Nombre d'etudiant a risque")
        self.stats_layout.addWidget(self.label_total_student)
        self.stats_layout.addWidget(self.label_moyenne_generale)
        self.stats_layout.addWidget(self.label_taux_absence)
        self.stats_layout.addWidget(self.label_student_risk)
        self.main_layout.addLayout(self.stats_layout)
        self.main_layout.addStretch()

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE user_id = ?", (self.user_id,))
        total_student = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(g.Note) FROM grades g INNER JOIN students s ON g.student_id = s.student_id WHERE s.user_id=?", (self.user_id,))
        moyenne_generale = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Abscence a INNER JOIN students s ON a.student_id = s.student_id WHERE s.user_id=?", (self.user_id,))
        total_absences = cursor.fetchone()[0]
        taux_absences = round((total_absences / total_student) *100) if total_student > 0 else 0
        cursor.execute("SELECT AVG(g.Note), s.nom || ' ' || s.prenom FROM grades g INNER JOIN students s ON g.student_id = s.student_id WHERE s.user_id=? GROUP BY s.student_id", (self.user_id,))
        nom_prenom_student = cursor.fetchall()
        noms = [row[1] for row in nom_prenom_student]
        moyenne_par_etudiant = [row[0] for row in nom_prenom_student]
        self.label_total_student.setText(f"Total étudiants : {total_student}")
        self.label_moyenne_generale.setText(f"Moyenne générale : {moyenne_generale}")
        self.label_taux_absence.setText(f"Taux Absences : {taux_absences}")
        self.label_student_risk.setText("Taux de risque: N/A")
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.bar(noms,moyenne_par_etudiant)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.main_layout.addWidget(self.canvas)


        




