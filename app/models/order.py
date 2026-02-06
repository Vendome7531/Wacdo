from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, Table, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
import enum

# 1. Définition des statuts
class OrderStatus(str, enum.Enum):
    EN_ATTENTE = "en_attente"          # Commande saisie par l'accueil
    EN_PREPARATION = "en_preparation"  # La cuisine a commencé
    PRETE = "prete"                    # La cuisine a fini, le sac attend au comptoir
    TERMINE = "termine"                # Le client est parti avec sa commande
    ANNULE = "annule"

# 2. Tables d'association pour le contenu (Many-to-Many)
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

# 3. Modèle principal
class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    final_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.EN_ATTENTE)
    
    # Relation avec l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # IMPORTANT : On utilise des noms en "string" (ex: "UserModel") 
    # pour éviter les imports circulaires en haut de fichier.
    user = relationship("UserModel", back_populates="orders")
    menus = relationship("MenuModel", secondary=order_menus)
    products = relationship("ProductModel", secondary=order_products)