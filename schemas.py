from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

# --- Farmer Schemas ---
class FarmerBase(BaseModel):
    name: str
    village: Optional[str] = None
    phone: Optional[str] = None

class FarmerCreate(FarmerBase):
    pass

class Farmer(FarmerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    category: str # Seeds, Pesticides, Trading
    price: float
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    farmer_id: int
    type: str # Credit, Debit, Payment
    amount: float
    product_details: Optional[str] = None
    interest_type: str = "Simple"
    interest_rate: float = 2.0
    status: str = "Pending"

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

class FarmerWithTransactions(Farmer):
    transactions: List[Transaction] = []

class TransactionBulkCreate(BaseModel):
    transactions: List[TransactionCreate]

class InterestRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    rate_per_month: Optional[float] = 2.0
    interest_type: Optional[str] = "Simple"

class InterestResult(BaseModel):
    principal: float
    interest: float
    total_amount: float
    details: List[dict] = []
