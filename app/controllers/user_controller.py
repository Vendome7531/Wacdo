from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import UserModel
import bcrypt

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_new_user(db: Session, username, email, password, role, is_active):
    """Crée un utilisateur à partir des données du formulaire."""
    # Vérification si l'email existe déjà
    email_exists = db.query(UserModel).filter(UserModel.email == email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    # Hachage bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    new_user = UserModel(
        username=username,
        email=email,
        hashed_password=hashed_pwd,
        role=role,
        is_active=is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_in_db(db: Session, user_id, username, email, password, role, is_active):
    """Met à jour un utilisateur via les champs du formulaire."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return None

    if username is not None: db_user.username = username
    if email is not None: db_user.email = email
    if role is not None: db_user.role = role
    if is_active is not None: db_user.is_active = is_active
    
    if password: # Si un nouveau mot de passe est saisi
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        db_user.hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Désactive l'utilisateur (soft delete) au lieu de le supprimer."""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return False
    db_user.is_active = False 
    db.commit()
    return True