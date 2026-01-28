from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Authentification"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Import local pour éviter l'erreur "partially initialized"
    from app.models.user import UserModel 

    # 2. On cherche l'utilisateur par l'email (le champ "username" de Swagger)
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # 3. Vérification de l'existence et du mot de passe
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Extraction du rôle pour le token (évite l'Erreur 500 avec les Enum)
    # Si user.role est un objet Enum, on prend sa .value (ex: "administrateur")
    role_name = user.role.value if hasattr(user.role, 'value') else user.role

    # 5. Génération du badge (Token)
    access_token = create_access_token(
        data={"sub": user.email, "role": role_name}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}