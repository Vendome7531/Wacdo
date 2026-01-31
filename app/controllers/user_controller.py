from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import UserModel
from app.schemas.user import UserCreate
import bcrypt

def get_all_users(db: Session):
    """Récupère tous les utilisateurs de la base."""
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: int):
    """Récupère un utilisateur spécifique par son ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user_data: UserCreate):
    """Crée un nouvel utilisateur avec hachage du mot de passe et vérification d'email."""
    # 1. Vérifier si l'email existe déjà
    email_exists = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé."
        )

    # 2. Hacher le mot de passe (Logique bcrypt)
    password_bytes = user_data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    # 3. Créer l'objet utilisateur
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        # On gère l'Enum pour éviter les erreurs de format en base
        role=user_data.role.value if hasattr(user_data.role, 'value') else user_data.role
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création : {str(e)}"
        )

def update_user(db: Session, user_id: int, user_update_data: dict):
    """Met à jour un utilisateur existant de façon partielle."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not db_user:
        return None

    for key, value in user_update_data.items():
        if value is not None:
            # 1. Cas particulier : EMAIL
            if key == "email":
                email_check = db.query(UserModel).filter(UserModel.email == value).first()
                if email_check and email_check.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Ce nouvel email est déjà utilisé par un autre compte."
                    )
                db_user.email = value # On l'assigne ici explicitement

            # 2. Cas particulier : PASSWORD (on hache)
            elif key == "password":
                password_bytes = value.encode('utf-8')
                salt = bcrypt.gensalt()
                db_user.hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
            
            # 3. Cas particulier : ROLE (Enum)
            elif key == "role":
                db_user.role = value.value if hasattr(value, 'value') else value
                
            # 4. Tous les autres champs (username, etc.)
            else:
                setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Désactive un compte (Soft Delete)."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db_user.is_active = False # On ne supprime plus, on désactive
        db.commit()
        return True
    return False