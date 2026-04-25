from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='alice@jobmatch.test').first()
    if user:
        print(f"User Alice found: {user.email}")
    else:
        print("User Alice NOT found!")
