from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str  # On utilise str au lieu de EmailStr

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: int
    
    class Config:
        from_attributes = True