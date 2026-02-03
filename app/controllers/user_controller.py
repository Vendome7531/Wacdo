from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import UserModel
from app.schemas.user import UserCreate
import bcrypt

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user_data: UserCreate):
    email_exists = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    password_bytes = user_data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role=user_data.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user_update_data: UserCreate):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return None
    db_user.username = user_update_data.username
    db_user.email = user_update_data.email
    db_user.role = user_update_data.role
    db_user.is_active = user_update_data.is_active
    if user_update_data.password:
        password_bytes = user_update_data.password.encode('utf-8')
        salt = bcrypt.gensalt()
        db_user.hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return False
    db_user.is_active = False 
    db.commit()
    return True