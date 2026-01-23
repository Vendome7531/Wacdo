from sqlalchemy import Column, Integer, Float, DateTime, String
from app.database.database import Base
from datetime import datetime

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="En cours") # En cours, Prête, Livrée