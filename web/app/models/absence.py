from app import db
from .student import Student

class Absence(db.Model):
    __tablename__ = "Abscence"
    id = db.Column("absence_id", db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    date = db.Column("Date",db.Date,nullable=False)
    justifiee = db.Column("Justifiee", db.Boolean, nullable = False)
    student = db.relationship('Student', backref='abscences', lazy=True)


