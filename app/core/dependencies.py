from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM

# Dit à Swagger où aller chercher le badge (le token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    """
    Cette fonction ouvre le badge et regarde quel est le rôle à l'intérieur.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Badge invalide")
        return role
    except JWTError:
        raise HTTPException(status_code=401, detail="Session expirée ou invalide")

def admin_only(role: str = Depends(get_current_user_role)):
    """
    C'est le videur : si le rôle n'est pas admin, il bloque TOUT.
    """
    if role != "administrateur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit : Seul le gérant peut faire ça."
        )
    return role