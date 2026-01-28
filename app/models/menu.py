from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base

# Cette table "invisible" fait le lien entre les deux
menu_products = Table(
    'menu_products',
    Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class MenuModel(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    image = Column(String(255)) # Important pour le diagramme !
    price = Column(Float, nullable=False)
    
    # La relation Many-to-Many vers Produit
    products = relationship("ProductModel", secondary=menu_products)
    
    