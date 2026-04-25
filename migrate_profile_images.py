# Script de migration pour ajouter les colonnes profile_picture et banner_image
from app import app, db

with app.app_context():
    try:
        # Exécuter les commandes SQL pour ajouter les colonnes
        from sqlalchemy import text
        
        # Vérifier si les colonnes existent déjà
        result = db.session.execute(text("PRAGMA table_info(user)"))
        columns = [row[1] for row in result]
        
        if 'profile_picture' not in columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN profile_picture VARCHAR(200)"))
            print("✓ Colonne profile_picture ajoutée")
        else:
            print("ℹ Colonne profile_picture existe déjà")
            
        if 'banner_image' not in columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN banner_image VARCHAR(200)"))
            print("✓ Colonne banner_image ajoutée")
        else:
            print("ℹ Colonne banner_image existe déjà")
        
        db.session.commit()
        print("\n✅ Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {str(e)}")
        db.session.rollback()
