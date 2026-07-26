from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.master import bp as master_bp
    app.register_blueprint(master_bp, url_prefix='/master')

    from app.schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp, url_prefix='/schedule')

    from app.views import bp as views_bp
    app.register_blueprint(views_bp, url_prefix='/views')

    from app.database import bp as database_bp
    app.register_blueprint(database_bp, url_prefix='/database')

    from app import models

    with app.app_context():
        import os
        os.makedirs(app.config['BACKUP_DIR'], exist_ok=True)
        db.create_all()
        _seed_admin(app)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('schedule.index'))
        return redirect(url_for('auth.login'))

    return app


def _seed_admin(app):
    from app.models import User
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                email='admin@trac.edu.ph',
                role='admin',
                full_name='System Administrator',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
