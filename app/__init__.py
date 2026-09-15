# app/__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
        static_url_path='/static'
    )

    # On Render, no persistent disk -> use /tmp (writable, ephemeral)
    # Locally, use instance/mplads.db
    if os.environ.get('RENDER'):
        db_path = os.path.join('/tmp', 'mplads.db')
    else:
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        db_dir = os.path.join(basedir, 'instance')
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'mplads.db')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Auto-seed admin + officer on startup (fresh DB on Render)
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            u = User(username='admin')
            u.set_password('admin123')
            db.session.add(u)
            db.session.commit()
            app.logger.info('Seeded admin')
        if not User.query.filter_by(username='officer').first():
            u = User(username='officer')
            u.set_password('officer123')
            db.session.add(u)
            db.session.commit()
            app.logger.info('Seeded officer')

    return app