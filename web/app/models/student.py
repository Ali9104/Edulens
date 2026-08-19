from app import db
from .user import User

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column ("student_id",db.Integer,primary_key=True,autoincrement=True)
    nom = db.Column("Nom",db.String(100),nullable=False)
    prenom = db.Column("Prenom",db.String(100),nullable=False)
    groupe = db.Column("Groupe",db.String(50),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='students', lazy=True)

