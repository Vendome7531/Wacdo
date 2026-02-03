from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import UserModel
from app.schemas.user import UserCreate
import bcrypt

def get_all_users(db: Session):
    """Récupère tous les utilisateurs, actifs ou non."""
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: int):
    """Récupère un utilisateur spécifique par son ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user_data: UserCreate):
    """Crée un nouvel utilisateur avec hachage bcrypt et vérification d'unicité email."""
    # 1. Vérification si l'email existe déjà
    email_exists = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé."
        )

    # 2. Hachage du mot de passe
    password_bytes = user_data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    # 3. Création de l'objet utilisateur
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role=user_data.role.value if hasattr(user_data.role, 'value') else user_data.role,
        is_active=True # Par défaut, un nouvel utilisateur est actif
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
    """
    Met à jour un utilisateur. 
    Hache le MDP automatiquement et vérifie l'unicité du nouvel email.
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not db_user:
        return None

    for key, value in user_update_data.items():
        if value is None:
            continue

        # Cas : Modification de l'email
        if key == "email":
            email_check = db.query(UserModel).filter(UserModel.email == value).first()
            if email_check and email_check.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Ce nouvel email est déjà utilisé."
                )
            db_user.email = value

        # Cas : Modification du mot de passe
        elif key == "password":
            password_bytes = value.encode('utf-8')
            salt = bcrypt.gensalt()
            db_user.hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        # Cas : Modification du rôle (réservé à l'Admin via le router)
        elif key == "role":
            db_user.role = value.value if hasattr(value, 'value') else value
            
        # Cas : Autres champs (username, is_active, etc.)
        else:
            setattr(db_user, key, value)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la sauvegarde des modifications."
        )

def delete_user(db: Session, user_id: int):
    """
    Désactive un compte (Soft Delete). 
    L'utilisateur ne peut plus se connecter mais reste dans l'historique.
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return False
        
    try:
        db_user.is_active = False 
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False