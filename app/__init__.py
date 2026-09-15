# app/__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
import os
import csv

db = SQLAlchemy()
login_manager = LoginManager()

def _parse_mplad_row(raw_line):
    """Parse one line of the messy MPLAD CSV.
    Format: "field1;""field2"";""field3"";...",junk,junk,...
    Returns dict with keys: mp_name, work, category, state, constituency,
    ida, city, ward, block, village, recommended_date, allocation_amount,
    ida_approval, status, house
    """
    # Find first comma OUTSIDE quotes
    in_quotes = False
    split_at = -1
    for i, ch in enumerate(raw_line):
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            split_at = i
            break

    if split_at == -1:
        return None

    left = raw_line[:split_at]

    # Strip surrounding quotes from the whole field
    if left.startswith('"'):
        left = left[1:]
    if left.endswith('"'):
        left = left[:-1]

    # Split by semicolon
    parts = [p.strip() for p in left.split(';')]

    # Clean each part: remove surrounding double quotes and escaped quotes
    cleaned = []
    for p in parts:
        p = p.strip()
        # Remove leading/trailing double quotes
        while p.startswith('"'):
            p = p[1:]
        while p.endswith('"'):
            p = p[:-1]
        cleaned.append(p.strip())

    # Expected order (from header):
    # mp_name, work, category, state, constituency, ida, city, ward,
    # block, village, recommended_date, allocation_amount,
    # ida_approval, status, house
    keys = [
        'mp_name', 'work', 'category', 'state', 'constituency',
        'ida', 'city', 'ward', 'block', 'village',
        'recommended_date', 'allocation_amount', 'ida_approval',
        'status', 'house'
    ]
    out = {}
    for i, k in enumerate(keys):
        out[k] = cleaned[i] if i < len(cleaned) else ''
    return out


def _seed_projects_from_csv(csv_path, app):
    """Load projects from the messy MPLAD CSV. Returns count loaded."""
    from app.models import Project

    if not os.path.exists(csv_path):
        app.logger.warning(f'CSV not found at {csv_path} — skipping project seed')
        return 0

    count = 0
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        # Skip header line
        header = f.readline()

        for raw_line in f:
            raw_line = raw_line.rstrip('\n').rstrip('\r')
            if not raw_line.strip():
                continue

            row = _parse_mplad_row(raw_line)
            if not row:
                continue

            work = (row.get('work') or '').strip()
            if not work or work.lower() == 'unknown':
                continue

            # Amount
            amt_str = (row.get('allocation_amount') or '0').strip()
            try:
                amount = float(amt_str) if amt_str else 0.0
            except ValueError:
                amount = 0.0

            # Block is our "district" field
            district = (row.get('block') or '').strip()
            village = (row.get('village') or '').strip()

            p = Project(
                name=work,
                district=district,
                village=village,
                amount=amount,
                work_category=(row.get('category') or '').strip(),
                work_status='Action Pending'
            )
            db.session.add(p)
            count += 1

    db.session.commit()
    app.logger.info(f'Seeded {count} projects from CSV')
    return count


def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
        static_url_path='/static'
    )

    # Always resolve basedir
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

       # On Render, use /tmp (writable, ephemeral).
    # Locally, use instance/mplads.db
    if os.environ.get('RENDER'):
        db_path = os.path.join('/tmp', 'mplads.db')

        # On first boot, copy the pre-built DB (with 100 projects + 55 anomalies)
        # from the repo into /tmp so the demo has real data
        seed_db = os.path.join(basedir, 'instance', 'mplads.db')
        if not os.path.exists(db_path) and os.path.exists(seed_db):
            import shutil
            shutil.copy(seed_db, db_path)
    else:
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

    # ---- AUTO-SEED ON STARTUP ----
    with app.app_context():
        from app.models import Project

        db.create_all()

        # Seed users
        if not User.query.filter_by(username='admin').first():
            u = User(username='admin', email='admin@mplad.local')
            u.set_password('admin123')
            db.session.add(u)
            db.session.commit()
            app.logger.info('Seeded admin')

        if not User.query.filter_by(username='officer').first():
            u = User(username='officer', email='officer@mplad.local')
            u.set_password('officer123')
            db.session.add(u)
            db.session.commit()
            app.logger.info('Seeded officer')

        # Seed projects from CSV (only if empty)
        if Project.query.count() == 0:
            # Look in a few likely locations
            candidates = [
                os.path.join(basedir, 'data', 'mplad_cleaned_final.csv'),
                os.path.join(basedir, 'mplad_cleaned_final.csv'),
                os.path.join(basedir, 'data', 'mplad.csv'),
            ]
            for path in candidates:
                if os.path.exists(path):
                    _seed_projects_from_csv(path, app)
                    break
            else:
                app.logger.warning('No MPLAD CSV found in expected locations')
        else:
            app.logger.info(f'Projects already present ({Project.query.count()}), skipping seed')

    return app