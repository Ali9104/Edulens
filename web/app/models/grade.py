from app import db
from .student import Student
class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column ("grade_id",db.Integer,primary_key=True,autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    matiere = db.Column("Matiere",db.String(100),nullable=False)
    note = db.Column("Note",db.Float,nullable=False)
    date = db.Column("Date",db.Date,nullable=False)
    semestre = db.Column("Semestre",db.String(50),nullable=False)
    student = db.relationship('Student', backref='grades', lazy=True)