from flask import Blueprint,request,render_template,redirect,url_for
from flask_login import login_required,current_user
from app.models.grade import Grade
from app.models.student import Student
from app import db
from datetime import datetime

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')
@grades_bp.route('/', methods=['GET'])
@login_required
def get_grades():
    students = Student.query.filter_by(user_id=current_user.id).all()
    student_ids = [s.id for s in students]
    grades = Grade.query.filter(Grade.student_id.in_(student_ids)).all()
    return render_template('grades.html', grades = grades)

@grades_bp.route('/add/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_grade(student_id):
     student =Student.query.get_or_404(student_id)
     if student.user_id != current_user.id:
        return "Unauthorized", 403
     if request.method == 'POST':
          matiere = request.form.get('matiere')
          note = request.form.get('note')
          date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
          semestre = request.form.get('semestre')
          new_grade = Grade(student_id = student_id, matiere = matiere, note = note, date = date, semestre = semestre)
          db.session.add(new_grade)
          db.session.commit()
          return redirect(url_for('grades.get_grades'))
     return render_template('add_grade.html', student = student)

@grades_bp.route('/delete/<int:grade_id>', methods=['POST'])
@login_required
def delete_grade(grade_id):
    grade=Grade.query.get_or_404(grade_id)
    if grade.student.user_id != current_user.id:
        return "Unauthorized", 403
    db.session.delete(grade)
    db.session.commit()
    return redirect(url_for('grades.get_grades'))

@grades_bp.route('/edit/<int:grade_id>', methods = ['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    grade=Grade.query.get_or_404(grade_id)
    if request.method == 'POST':
        grade.matiere = request.form.get('matiere')
        grade.note = request.form.get('note')
        grade.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        grade.semestre = request.form.get('semestre')
        db.session.commit()
        return redirect(url_for('grades.get_grades'))
    return render_template('edit_grade.html', grade = grade) 
     




          
          
        
    

