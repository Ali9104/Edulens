from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_required,current_user
from app.models.student import Student
from app.models.absence import Absence
from app.services.ml_engine import cluster_students

analytics_bp = Blueprint('analytics', __name__, url_prefix ="/analytics")
@analytics_bp.route("/", methods = ['GET'] )
@login_required
def analytics():
    students = Student.query.filter_by(user_id=current_user.id).all()
    cluster = cluster_students(students)
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
    absences_par_etudiant = [len(s.abscences) for s in students]
    semestres_data = {}
    for student in students:
        for grade in student.grades:
            if grade.semestre not in semestres_data:
                semestres_data[grade.semestre] = []
            semestres_data[grade.semestre].append(grade.note)
    occurance_non_evalue = list(cluster.values()).count("Non évalué")
    return render_template('analytics.html', total_students=total_students, average=round(average, 2), noms = noms, moyenne = moyenne, cluster = cluster, students = students, occurance_difficulte = occurance_difficulte , occurance_moyen = occurance_moyen , occurance_excellent = occurance_excellent, taux_absence = taux_absence,  occurance_non_evalue =  occurance_non_evalue, absences_par_etudiant = absences_par_etudiant, semestres_data = semestres_data  )
