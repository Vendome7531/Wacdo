📂 DOSSIER TECHNIQUE : PROJET WACDO

1. Ma démarche de sécurité et d'initialisation
Pour ce projet, j'ai mis en place une gestion des droits d'accès stricte : seul un administrateur possède les permissions nécessaires pour créer des comptes utilisateurs.

Cette configuration crée cependant un blocage lors de la première installation puisque la base de données est vide. Pour résoudre ce problème de manière professionnelle, j'ai développé un script d'amorçage du système (init_admin.py). Ce script permet d'injecter directement le premier compte administrateur en base de données, ce qui permet ensuite de se connecter à l'API et de gérer le reste du personnel.



2. Mon script d'initialisation (init_admin.py)
J'utilise ce script pour créer l'accès maître. Pour garantir la sécurité, j'ai intégré la bibliothèque bcrypt afin de ne jamais stocker de mots de passe en clair.

"""
import sys
import os

# On s'assure que le script peut trouver le dossier 'app'
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.core.security import get_password_hash

# IMPORT DE TOUS LES MODÈLES (pour résoudre les relations circulaires)
from app.models.user import UserModel, UserRole
from app.models.order import OrderModel      
from app.models.product import ProductModel
from app.models.menu import MenuModel        # Ajouté pour éviter l'erreur de mapping

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
        print("SUCCÈS : L'administrateur 'vendome' a été créé.")
        print("Identifiants : vendome / 1234")
        print("---\n")

    except Exception as e:
        print(f"\n ERREUR CRITIQUE : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_first_admin()
"""


3. Guide d'installation et d'utilisation (README)

Voici les étapes que j'ai définies pour mettre en place et tester mon API :
Installation des dépendances : pip install -r requirements.txt
Amorçage du compte admin : python init_admin.py
Démarrage du serveur : uvicorn main:app --reload
Exécution de ma suite de tests : pytest -v -W ignore

4. Validation de mon travail

J'ai validé l'intégralité de la logique métier et de la sécurité via une suite de tests automatisés. Mon projet affiche actuellement un résultat de 3/3 PASSED.
À travers ces tests, j'ai prouvé que :
L'administrateur accède correctement à la gestion des utilisateurs.
L'agent d'accueil peut créer des commandes de manière fluide via le formulaire dédié.
Le préparateur (cuisine) est restreint aux fonctions de consultation et ne peut pas créer de commandes, respectant ainsi la hiérarchie des rôles que j'ai établie.