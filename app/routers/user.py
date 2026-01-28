from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import UserModel
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(user_data: dict, db: Session = Depends(get_db)):
    # 1. Vérifier si l'email existe déjà
    db_user = db.query(UserModel).filter(UserModel.email == user_data["email"]).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    # 2. Hacher le mot de passe avec notre nouvelle fonction bcrypt
    hashed_pwd = get_password_hash(user_data["password"])

    # 3. Créer l'objet utilisateur
    # On s'assure que les clés correspondent exactement à ton JSON Swagger
    new_user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hashed_pwd,
        role=user_data["role"]
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Utilisateur créé avec succès", "id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur base de données : {str(e)}")