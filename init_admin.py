import sys
import os


sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.core.security import get_password_hash

# IMPORT DE TOUS LES MODÈLES (pour résoudre les relations circulaires)
from app.models.user import UserModel, UserRole
from app.models.order import OrderModel      
from app.models.product import ProductModel
from app.models.menu import MenuModel        

def create_first_admin():
    # 1. On ouvre une connexion à la base MySQL
    db: Session = SessionLocal()
    try:
        # 2. On vérifie si l'admin existe déjà
        admin_check = db.query(UserModel).filter(UserModel.username == "vendome").first()
        
        if admin_check:
            print("\n---")
            print(f"L'utilisateur '{admin_check.username}' existe déjà avec le rôle {admin_check.role}.")
            print("---\n")
            return

        # 3. On prépare le nouvel admin
        new_admin = UserModel(
            username="vendome",
            email="vendome@wacdo.fr",
            hashed_password=get_password_hash("1234"),
            role=UserRole.ADMINISTRATEUR 
        )

        # 4. On l'ajoute et on valide
        db.add(new_admin)
        db.commit()
        print("\n---")
        print("✅ SUCCÈS : L'administrateur 'vendome' a été créé.")
        print("Identifiants : vendome / 1234")
        print("---\n")

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_first_admin()