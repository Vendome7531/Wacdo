import enum
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from app.database.database import Base

class CategoryEnum(str, enum.Enum):
    Burgers = "Burgers"
    Accompagnements = "Accompagnements"
    Boissons = "Boissons"
    Desserts = "Desserts"
    Menus = "Menus"

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    # ICI : On remet la catégorie DANS la classe avec native_enum=False
    category = Column(Enum(CategoryEnum, native_enum=False), nullable=True)
    image = Column(String(255), nullable=True)
    is_available = Column(Boolean, default=True)
