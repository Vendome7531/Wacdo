import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine, Base
from app.models.product import ProductModel
from app.models.menu import MenuModel
from app.models.user import UserModel
from app.core.security import get_password_hash
from sqlalchemy import text
from app.models.order import OrderModel

def seed_complete():
    db: Session = SessionLocal()
    try:
        print("🏗️  Recréation des tables sur Aiven...")
        Base.metadata.create_all(bind=engine)

        print("🧹 Nettoyage complet (Truncate)...")
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        db.execute(text("TRUNCATE TABLE menu_products;"))
        db.execute(text("TRUNCATE TABLE menus;"))
        db.execute(text("TRUNCATE TABLE products;"))
        db.execute(text("TRUNCATE TABLE users;"))
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        db.commit()

        print("👤 Création de l'admin 'vendome'...")
        admin = UserModel(
            username="vendome",
            email="admin@wacdo.com",
            hashed_password=get_password_hash("1234"),
            role="administrateur",
            is_active=True
        )
        db.add(admin)
        db.commit()

        print("🌱 Insertion des produits avec TOUTES les images...")
        p1 = ProductModel(
            name="Le Royal Cheese", 
            description="Boeuf, cheddar fondant", 
            price=8.50, 
            is_available=True,
            image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=500"
        )
        p2 = ProductModel(
            name="Frites Maison", 
            description="Croustillantes à souhait", 
            price=3.50, 
            is_available=True,
            image="https://images.unsplash.com/photo-1573080496219-bb080dd4f877?q=80&w=500"
        )
        p3 = ProductModel(
            name="Coca-Cola Zero", 
            description="33cl de fraîcheur", 
            price=2.50, 
            is_available=True,
            image="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?q=80&w=500"
        )
        p4 = ProductModel(
            name="Le Veggie Burger", 
            description="Galette de pois chiche et herbes", 
            price=9.00, 
            is_available=True,
            image="https://images.unsplash.com/photo-1550547660-d9450f859349?q=80&w=500"
        )
        p5 = ProductModel(
            name="Nuggets x9", 
            description="Poulet pané doré", 
            price=6.50, 
            is_available=True,
            image="https://images.unsplash.com/photo-1562967914-608f82629710?q=80&w=500"
        )
        p6 = ProductModel(
            name="Muffin Chocolat", 
            description="Cœur fondant", 
            price=3.00, 
            is_available=True,
            image="https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=500"
        )
        
        db.add_all([p1, p2, p3, p4, p5, p6])
        db.commit() 

        print("🍱 Création des menus complets...")
        m1 = MenuModel(
            name="Menu Royal", 
            description="Burger + Frites + Boisson", 
            price=12.50, 
            is_available=True,
            image="https://images.unsplash.com/photo-1513185158878-8d8c196b7f81?q=80&w=500"
        )
        m1.products = [p1, p2, p3]

        m2 = MenuModel(
            name="Menu Veggie", 
            description="Veggie Burger + Eau + Muffin", 
            price=13.00, 
            is_available=True,
            image="https://images.unsplash.com/photo-1525059696034-4967a8e1dca2?q=80&w=500"
        )
        m2.products = [p4, p3, p6]

        m3 = MenuModel(
            name="Box Partage", 
            description="Nuggets + Frites + Boisson", 
            price=18.00, 
            is_available=True,
            image="https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?q=80&w=500"
        )
        m3.products = [p5, p2, p3] 

        db.add_all([m1, m2, m3])
        db.commit()
        print("✅ Tout est sur Aiven : Admin, Produits (avec images) et Menus !")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_complete()