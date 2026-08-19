from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

db=SQLAlchemy()

login_manager=LoginManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    from app.models import user, student, grade, absence
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(user_id)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.dashboard import home_bp
    app.register_blueprint(home_bp)
    from app.routes.students import students_bp
    app.register_blueprint(students_bp)
    from app.routes.grades import grades_bp
    app.register_blueprint(grades_bp)
    from app.routes.absences import absences_bp
    app.register_blueprint(absences_bp)
    from app.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)
    return app
