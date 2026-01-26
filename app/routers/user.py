from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import UserModel
from app.schemas.user import UserSchema, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserSchema)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # On vérifie si l'email existe déjà
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    new_user = UserModel(username=user_data.username, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()