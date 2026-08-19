from flask import Blueprint,request,render_template,redirect,url_for,flash
from flask_login import login_user,logout_user
from werkzeug.security import check_password_hash
from app.models.user import User
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()
        is_email_exist=user is not None
        if is_email_exist:
            is_valid= check_password_hash(user.password,request.form.get('password'))
            if is_valid:
                login_user(user)
                return redirect(url_for('home.home'))
            else:
                flash("Email ou mot de passe incorrect", "danger")
                return render_template('login.html')
        else:
            flash("Email ou mot de passe incorrect", "danger")
            return render_template('login.html')
    else:
        return render_template('login.html') 
@auth_bp.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


