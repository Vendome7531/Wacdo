from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database.database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)