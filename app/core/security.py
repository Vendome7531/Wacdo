import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

# Paramètres du Token
SECRET_KEY = "ton_secret_key_tres_securise" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str):
    """Vérifie le mot de passe en utilisant bcrypt directement."""
    # On transforme le texte en bytes pour bcrypt
    password_byte = plain_password.encode('utf-8')
    hashed_byte = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte, hashed_byte)

def get_password_hash(password: str):
    """Hache le mot de passe en utilisant bcrypt directement."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Génère le token JWT (inchangé)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)