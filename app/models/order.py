from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, Table, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
import enum

class OrderStatus(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    EN_PREPARATION = "en_preparation"
    TERMINE = "termine"
    ANNULE = "annule"

# Tables d'association pour le contenu de la commande
order_menus = Table(
    'order_menus', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True)
)

order_products = Table(
    'order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    final_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.EN_ATTENTE)
    
    # Relation avec l'utilisateur qui commande
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel")

    # Contenu de la commande
    menus = relationship("MenuModel", secondary=order_menus)
    products = relationship("ProductModel", secondary=order_products)