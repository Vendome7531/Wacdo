from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base

# Table d'association pour la relation Many-to-Many entre Menus et Produits
menu_products = Table(
    "menu_products",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menus.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)

class MenuModel(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True) 

    # Relation avec les produits
    products = relationship("ProductModel", secondary=menu_products, backref="menus")