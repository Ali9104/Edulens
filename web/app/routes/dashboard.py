from flask import Blueprint,render_template
from flask_login import login_required,current_user
from app.models.user import User
from app.models.student import Student
from app.models.absence import Absence
from app.services.ml_engine import cluster_students


home_bp=Blueprint('home',__name__,url_prefix='/home')
@home_bp.route('/',methods=['GET'])
@login_required
def home():
    students = Student.query.filter_by(user_id=current_user.id).all()
    cluster =  cluster_students(students)
    occurance_difficulte  = list(cluster.values()).count("En difficulté")
    occurance_moyen = list(cluster.values()).count("Moyen")
    occurance_excellent = list(cluster.values()).count("Excellent")
    total_students =  len(students)
    student_ids = [s.id for s in students]
    total_absences = Absence.query.filter(Absence.student_id.in_(student_ids)).count()
    taux_absence = round((total_absences / total_students * 100), 1) if total_students > 0 else 0
    all_grades = []
    for student in students:
        for grade in student.grades:
            all_grades.append(grade.note)
    if all_grades:
        average = sum(all_grades) / len(all_grades)
    else:
        average = 0
    noms=[s.nom + ' ' + s.prenom for s in students]
    moyenne = []
    for student in students:
        notes = [g.note for g in student.grades]
        if notes:
            moyenne.append(round(sum(notes)/len(notes), 2))
        else:
            moyenne.append(0)
    return render_template('home.html', total_students=total_students, average=round(average, 2), noms = noms, moyenne = moyenne, cluster = cluster, students = students, occurance_difficulte = occurance_difficulte , occurance_moyen = occurance_moyen , occurance_excellent = occurance_excellent, taux_absence = taux_absence  )
    
