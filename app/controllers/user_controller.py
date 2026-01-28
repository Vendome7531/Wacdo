from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user import UserCreate
import bcrypt

def create_user(db: Session, user_data: UserCreate):
    # Encodage du mot de passe en bytes
    password_bytes = user_data.password.encode('utf-8')
    
    # Génération du sel et hachage
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password_bytes, salt)
    
    # On convertit le hash en string pour le stocker dans MySQL
    hashed_pwd_str = hashed_pwd.decode('utf-8')

    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd_str,
        role=user_data.role.value if hasattr(user_data.role, 'value') else user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(UserModel).all()