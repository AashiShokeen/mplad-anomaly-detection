# create_admin.py — Create admin and officer users
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()

    # Delete old users
    User.query.delete()
    db.session.commit()

    # Create admin
    admin = User(username='admin', email='admin@mplad.gov.in')
    admin.set_password('admin123')
    db.session.add(admin)

    # Create officer
    officer = User(username='officer', email='officer@mplad.gov.in')
    officer.set_password('officer123')
    db.session.add(officer)

    db.session.commit()

    print("✅ Users created:")
    print("   admin / admin123")
    print("   officer / officer123")
    print(f"   Total users: {User.query.count()}")