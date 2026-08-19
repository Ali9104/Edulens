from flask import Blueprint,request,render_template,redirect,url_for,send_file
from flask_login import login_required,current_user
from app.models.student import Student
from app import db
from app.services.data_processor import import_students_csv
from app.services.report_generator import generate_report
import os


students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/', methods=['GET'])
@login_required
def list_students():
    student = Student.query.filter_by(user_id=current_user.id).all()
    return render_template('students.html', students=student)

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        groupe = request.form.get('groupe')
        new_student = Student(nom=nom, prenom=prenom, groupe=groupe, user_id=current_user.id)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students.list_students'))
    return render_template('add_student.html')

@students_bp.route('/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student =Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unauthorized", 403
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students.list_students'))

@students_bp.route('/details/<int:student_id>', methods=['GET'])
@login_required
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unauthorized", 403
    return render_template('student_details.html', student=student)

@students_bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unaudthorized",403
    if request.method == 'POST':
        student.nom = request.form.get('nom')
        student.prenom = request.form.get('prenom')
        student.groupe = request.form.get('groupe')
        db.session.commit()
        return redirect(url_for('students.list_students'))
    return render_template('edit_student.html', student = student)

@students_bp.route('/import', methods=['GET', 'POST'])
@login_required
def send_csv():
    if request.method == 'POST':
        file = request.files.get('file')
        filepath = 'temp_file.csv'
        file.save(filepath)
        import_students_csv(filepath,current_user.id)
        return redirect(url_for('students.list_students'))
    return render_template('import_students.html')

@students_bp.route('/export/<int:student_id>', methods = ['GET'])
@login_required
def download_student_pdf(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unauthorized",403
    path = generate_report(student)
    return send_file(path, as_attachment = True)

@students_bp.route('/rapport/<int:student_id>', methods=['GET'])
@login_required
def list_rapport_by_students(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user_id != current_user.id:
        return "Unauthorized",403
    if not student.grades:
        return "Cet étudiant n'a pas encore de notes", 400
    path = generate_report(student)
    print(student.grades)
    return send_file(path, as_attachment = False)

@students_bp.route('/rapports', methods = ['GET'])
@login_required
def list_all_report():
    reports_dir = os.path.join(os.path.dirname(__file__), '..', )
    fichiers = [f for f in os.listdir(reports_dir) if f.startswith('rapport_')]
    print(os.path.abspath(reports_dir))
    print(os.listdir(reports_dir))
    return render_template('rapports.html', fichiers = fichiers)

@students_bp.route('/rapports/download/<filename>', methods=['GET'])
@login_required
def download_rapport(filename):
    path = os.path.join(os.path.dirname(__file__), '..', filename)
    return send_file(path, as_attachment = True)

@students_bp.route('/rapports/view/<filename>', methods=['GET'])
@login_required
def view_rapport(filename):
    path = os.path.join(os.path.dirname(__file__), '..', filename)
    return send_file(path, as_attachment = False)


    


    





