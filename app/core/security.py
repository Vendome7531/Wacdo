import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

# Paramètres du Token
SECRET_KEY = "ton_secret_key_tres_securise" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str):
    """Vérifie le mot de passe en utilisant SHA256 (compatible Python 3.13)."""
    # On hache le mot de passe saisi par l'utilisateur
    current_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    # On compare avec ce qui est stocké en base
    return current_hash == hashed_password

def get_password_hash(password: str):
    """Génère un hash SHA256 (compatible Python 3.13)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Génère le token JWT (inchangé)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)