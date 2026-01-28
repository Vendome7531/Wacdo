from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    
    # Lien vers l'ID de l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id"))


    user = relationship("UserModel", back_populates="orders")