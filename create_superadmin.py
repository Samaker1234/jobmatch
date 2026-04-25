from app import app, db
from models import User
import sys

def create_superadmin():
    with app.app_context():
        # Check if admin already exists
        email = "admin@jobmatch.fr"
        existing_admin = User.query.filter_by(email=email).first()
        
        if existing_admin:
            print(f"L'utilisateur {email} existe deja. Mise a jour vers Superadmin...")
            existing_admin.is_admin = True
            existing_admin.profession = "Super Administrateur"
            db.session.commit()
            print("Utilisateur mis a jour en Superadmin.")
            return

        # Create new superadmin
        admin = User(
            firstname="Super",
            lastname="Admin",
            email=email,
            profession="Super Administrateur",
            is_admin=True
        )
        admin.set_password("admin123")
        
        try:
            db.session.add(admin)
            db.session.commit()
            print(f"Superadmin cree avec succes !")
            print(f"Email    : {email}")
            print(f"Password : admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la creation : {e}")

if __name__ == "__main__":
    create_superadmin()
