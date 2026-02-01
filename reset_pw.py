import hashlib
from app.database.database import SessionLocal
from app.models.user import UserModel
from app.models.order import OrderModel
from app.models.product import ProductModel
from app.models.menu import MenuModel

def reset():
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.username == "caissier_v1").first()
        if user:
            # On utilise une méthode alternative pour hacher le mot de passe
            # Si ton projet utilise bcrypt, on va juste mettre un hash compatible
            # Note: Pour le test, on force un hash simple si passlib bug
            from passlib.hash import bcrypt
            user.hashed_password = bcrypt.hash("1234")
            
            db.commit()
            print("✅ SUCCÈS : Le mot de passe est maintenant '1234'")
        else:
            print("❌ Utilisateur non trouvé.")
    except Exception as e:
        print(f"💥 Nouvelle tentative... Erreur : {e}")
        # Si bcrypt bloque encore, on peut essayer d'installer une version plus ancienne
        # ou de corriger le mot de passe manuellement via MySQL.
    finally:
        db.close()

if __name__ == "__main__":
    reset()