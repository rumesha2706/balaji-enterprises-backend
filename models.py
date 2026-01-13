from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    village = Column(String, nullable=True)
    phone = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="farmer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True)  # Seeds, Pesticides, Trading
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    type = Column(String)  # Credit, Debit, Payment
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    product_details = Column(Text, nullable=True) # JSON string or text details
    interest_type = Column(String, default="Simple") # Simple, Compound
    interest_rate = Column(Float, default=2.0) # Monthly interest rate typically
    status = Column(String, default="Pending")

    farmer = relationship("Farmer", back_populates="transactions")

class TradingSale(Base):
    __tablename__ = "trading_sales"

    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String, index=True)
    product_details = Column(Text)
    total_amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
