from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget,QVBoxLayout,QSplitter,QPushButton
from PyQt6.QtCore import Qt
from ui.student_widget import StudentWidget
from ui.grade_widget import GradeWidget
from ui.absence_widget import AbsenceWidget
from ui.dashboard_widget import DashboardWidget
from ui.rapport_widget import RapportWidget

class MainWindow(QMainWindow):
    def __init__(self,user_id):
        super().__init__()
        self.setWindowTitle("Edulens")
        self.resize(600, 400)
        self.user_id = user_id
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.split = QSplitter(Qt.Orientation.Horizontal)
        self.widget = QWidget()
        self.widget_right_content = QWidget()
        self.right_layout = QVBoxLayout(self.widget_right_content)
        self.sidebar_layout = QVBoxLayout(self.widget)
        self.buttondashboard = QPushButton("Dashboard")
        self.buttondashboard.clicked.connect(self.show_dashboard)
        self.buttonetudiant = QPushButton("Etudiant")
        self.buttonetudiant.clicked.connect(self.show_student)
        self.buttonabsence = QPushButton("Absence")
        self.buttonabsence.clicked.connect(self.show_absence)
        self.buttonnote = QPushButton("Note")
        self.buttonnote.clicked.connect(self.show_note)
        self.buttonrapport = QPushButton("Rapport")
        self.buttonrapport.clicked.connect(self.show_rapport)
        self.split.addWidget(self.widget)
        self.split.addWidget(self.widget_right_content)
        self.main_layout.addWidget(self.split)
        self.sidebar_layout.addWidget(self.buttondashboard)
        self.sidebar_layout.addWidget(self.buttonetudiant)
        self.sidebar_layout.addWidget(self.buttonnote)
        self.sidebar_layout.addWidget(self.buttonabsence)
        self.sidebar_layout.addWidget(self.buttonrapport)
        self.sidebar_layout.addStretch()
        self.widget.setMaximumWidth(200)
    
    def show_dashboard(self):
        dashboard = DashboardWidget(self.user_id)
        dashboard.load_data()
        self.clear_right()
        self.right_layout.addWidget(dashboard)
        self.widget_right_content.adjustSize()
        dashboard.setVisible(True)

    def show_student(self):
        student = StudentWidget(self.user_id)
        student.load_data()
        self.clear_right()
        self.right_layout.addWidget(student)
        self.widget_right_content.adjustSize()
        student.setVisible(True)

    def clear_right(self):
        while self.right_layout.count():
            child = self.right_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_absence(self):
        absences = AbsenceWidget(self.user_id)
        absences.load_data()
        self.clear_right()
        self.right_layout.addWidget(absences)
        self.widget_right_content.adjustSize()
        absences.setVisible(True)

    def show_note(self):
        grades = GradeWidget(self.user_id)
        grades.load_data()
        self.clear_right()
        self.right_layout.addWidget(grades)
        self.widget_right_content.adjustSize()
        grades.setVisible(True)
        

    def show_rapport(self):
        rapport = RapportWidget(self.user_id)
        rapport.load_pdf()
        self.clear_right()
        self.right_layout.addWidget(rapport)
        self.widget_right_content.adjustSize()
        rapport.setVisible(True)



