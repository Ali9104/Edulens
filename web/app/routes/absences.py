from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_required,current_user
from app.models.absence import Absence
from app.models.student import Student
from app import db
from datetime import datetime

absences_bp = Blueprint("absences", __name__, url_prefix ="/absences")
@absences_bp.route("/", methods = ['GET'])
@login_required
def list_absence():
    students = Student.query.filter_by(user_id=current_user.id).all()
    student_ids = [s.id for s in students]
    absences = Absence.query.filter(Absence.student_id.in_(student_ids)).all()
    return render_template("absence_list.html", absences = absences)

@absences_bp.route("/add/<int:student_id>", methods = ['GET', 'POST'])
@login_required
def add_absence(student_id):
    student =Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unauthorized", 403
    if request.method == 'POST':
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        justifiee = request.form.get("justifiee") == '1'
        new_absence = Absence(student_id = student_id, date = date, justifiee = justifiee)
        db.session.add(new_absence)
        db.session.commit()
        return redirect(url_for('absences.list_absence'))
    return render_template("add_absence.html", student = student)

@absences_bp.route('/delete/<int:absence_id>', methods = ['POST'])
@login_required
def delete_absence(absence_id):
    absence = Absence.query.get_or_404(absence_id)
    if absence.student.user_id != current_user.id:
        return "Unauthorized",403
    db.session.delete(absence)
    db.session.commit()
    return redirect(url_for('absences.list_absence'))

@absences_bp.route('/edit/<int:absence_id>', methods = ['GET', 'POST'])
@login_required
def edit_absence(absence_id):
    absence = Absence.query.get_or_404(absence_id)
    if request.method == 'POST':
        absence.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        absence.justifiee = request.form.get('justifiee') == '1'
        db.session.commit()
        return redirect(url_for('absences.list_absence'))
    return render_template("edit_absence.html", absence = absence)




