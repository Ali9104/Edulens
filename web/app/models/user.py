from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column("user_id",db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column("Nom",db.String(100),nullable=False)
    email = db.Column("Email",db.String(150),nullable=False)
    password = db.Column("Password",db.String(500),nullable=False)
    role = db.Column("Role",db.String(50),nullable=False)


    