from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.product import ProductModel, CategoryEnum
from app.models.menu import MenuModel

def seed_data():
    db: Session = SessionLocal()
    try:
        print("🚀 Début du remplissage de la base de données...")

        # --- 1. CRÉATION DES PRODUITS ---
        # On définit une liste de produits avec tes catégories (Enum)
        product_list = [
            {"name": "Big Wac", "description": "Le burger iconique", "price": 5.50, "category": CategoryEnum.Burgers},
            {"name": "WacDouble", "description": "Double dose de plaisir", "price": 6.80, "category": CategoryEnum.Burgers},
            {"name": "Frites XL", "description": "Croustillantes à souhait", "price": 3.20, "category": CategoryEnum.Accompagnements},
            {"name": "WacCola", "description": "Boisson rafraîchissante", "price": 2.50, "category": CategoryEnum.Boissons},
            {"name": "WacFlurry", "description": "Glace vanille et éclats de biscuits", "price": 3.90, "category": CategoryEnum.Desserts},
        ]

        for p_data in product_list:
            # On vérifie si le produit existe déjà pour éviter les doublons
            exists = db.query(ProductModel).filter(ProductModel.name == p_data["name"]).first()
            if not exists:
                db.add(ProductModel(**p_data))
        
        # On valide l'ajout des produits pour qu'ils aient des IDs exploitables
        db.commit()
        print("✅ Produits insérés ou déjà présents.")

        # --- 2. CRÉATION DU MENU (Liaison Many-to-Many) ---
        menu_name = "Menu Best-Wac"
        
        # Vérification si le menu existe déjà
        if not db.query(MenuModel).filter(MenuModel.name == menu_name).first():
            # On récupère les produits que l'on veut mettre dans le menu
            burger = db.query(ProductModel).filter(ProductModel.name == "Big Wac").first()
            frite = db.query(ProductModel).filter(ProductModel.name == "Frites XL").first()
            boisson = db.query(ProductModel).filter(ProductModel.name == "WacCola").first()

            if burger and frite and boisson:
                nouveau_menu = MenuModel(
                    name=menu_name,
                    description="Le menu complet classique (Burger + Frite + Boisson)",
                    price=10.90
                )

                # Utilisation de la relation 'products' définie dans ton modèle MenuModel
                # Cela remplit automatiquement la table 'menu_products'
                nouveau_menu.products.append(burger)
                nouveau_menu.products.append(frite)
                nouveau_menu.products.append(boisson)

                db.add(nouveau_menu)
                db.commit()
                print(f"✅ Menu '{menu_name}' créé avec ses produits liés !")
            else:
                print("⚠️ Impossible de créer le menu : certains produits sont introuvables.")
        else:
            print(f"ℹ️ Le menu '{menu_name}' existe déjà.")

        print("🏁 Fin du script de seed.")

    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()