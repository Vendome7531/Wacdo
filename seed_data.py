import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# On force l'accès aux dossiers du projet
sys.path.append(os.getcwd())
from app.database.database import Base
# ... (tes autres imports restent les mêmes)

# --- MODIFICATION ICI ---
# On essaye de récupérer l'URL via le système (pour Render/GitHub)
# Si elle n'existe pas, on met ton URL Aiven par défaut (pour ton Mac)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://avnadmin:AVNS_mC88vnTwUWGWxZJwD5S@wacdo-mysql-db-wacdo-project.i.aivencloud.com:27384/defaultdb")
# ------------------------

# Configuration avec SSL (Obligatoire pour Aiven)
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "check_hostname": False,
            "fake_user": "true" 
        }
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_complete():
    db = SessionLocal()
    try:
        print("🔗 Connexion à Aiven (Port 27384)...")
        Base.metadata.create_all(bind=engine)

        print("🧹 Nettoyage des anciennes données...")
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in ["menu_products", "orders", "menus", "products", "users"]:
            db.execute(text(f"TRUNCATE TABLE {table};"))
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        db.commit()

        print("👤 Création des utilisateurs...")
        # L'admin principal
        admin_orig = UserModel(
            username="vendome", email="vendome@wacdo.fr",
            hashed_password=get_password_hash("1234"),
            role="administrateur", is_active=True
        )
        # Le deuxième admin
        admin_new = UserModel(
            username="administrateur01", email="admin01@wacdo.fr",
            hashed_password=get_password_hash("1234"),
            role="administrateur", is_active=True
        )
        # L'agent d'accueil
        accueil = UserModel(
            username="accueil01", email="accueil01@wacdo.fr",
            hashed_password=get_password_hash("1234"),
            role="agent_accueil", is_active=True
        )
        # Le préparateur
        preparateur = UserModel(
            username="preparateur01", email="preparateur01@wacdo.fr",
            hashed_password=get_password_hash("1234"),
            role="preparateur", is_active=True
        )
        
        db.add_all([admin_orig, admin_new, accueil, preparateur])

        print("🍔 Insertion des produits avec images...")
        p1 = ProductModel(
            name="Le Royal Cheese", description="Bœuf, cheddar fondant, cornichons et oignons.", 
            price=8.50, is_available=True, image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80"
        )
        p2 = ProductModel(
            name="Frites Maison", description="Frites fraîches coupées au couteau.", 
            price=3.90, is_available=True, image="https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500&q=80"
        )
        p3 = ProductModel(
            name="Coca-Cola Zero", description="33cl de fraîcheur intense.", 
            price=2.50, is_available=True, image="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&q=80"
        )
        p4 = ProductModel(
            name="Le Veggie Burger", description="Galette de quinoa et avocat.", 
            price=9.50, is_available=True, image="https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&q=80"
        )
        p5 = ProductModel(
            name="Muffin Chocolat", description="Cœur fondant chocolat noir.", 
            price=3.50, is_available=True, image="https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500&q=80"
        )
        
        db.add_all([p1, p2, p3, p4, p5])
        db.commit()

        print("🍱 Création du Menu...")
        m1 = MenuModel(
            name="Menu Royal", description="Le Royal Cheese + Frites + Boisson", 
            price=13.50, is_available=True, image="https://images.unsplash.com/photo-1513185158878-8d8c196b7f81?w=500&q=80"
        )
        m1.products = [p1, p2, p3]
        db.add(m1)
        db.commit()

        print("\n✅ RÉUSSITE : Aiven est à jour avec les nouveaux utilisateurs !")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_complete()