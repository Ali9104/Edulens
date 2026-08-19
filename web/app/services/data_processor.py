import pandas as pd
from app.models.student import Student
from app import db

def import_students_csv(filepath, user_id):
    data = pd.read_csv(filepath)
    for index, row in data.iterrows():
        nom = row['nom']
        prenom = row['prenom']
        groupe = row['groupe']
        student = Student(user_id=user_id,nom=nom, prenom=prenom, groupe=groupe)
        db.session.add(student)
    db.session.commit()
    