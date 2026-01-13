from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import models, schemas, database
from ..services import interest
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Transaction)
async def create_transaction(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(database.get_db)):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

@router.post("/bulk", response_model=List[schemas.Transaction])
async def create_bulk_transactions(bulk_data: schemas.TransactionBulkCreate, db: AsyncSession = Depends(database.get_db)):
    db_transactions = []
    for txn in bulk_data.transactions:
        db_txn = models.Transaction(**txn.dict())
        db.add(db_txn)
        db_transactions.append(db_txn)
    
    await db.commit()
    for txn in db_transactions:
        await db.refresh(txn)
    return db_transactions

@router.get("/", response_model=List[schemas.Transaction])
async def read_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Transaction).offset(skip).limit(limit))
    transactions = result.scalars().all()
    return transactions

@router.get("/{transaction_id}/calculate-interest")
async def calculate_transaction_interest(transaction_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.id == transaction_id))
    transaction = result.scalars().first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    calc = interest.calculate_interest(
        principal=transaction.amount,
        rate_per_month=transaction.interest_rate,
        start_date=transaction.date,
        end_date=datetime.utcnow(),
        interest_type=transaction.interest_type
    )
    return calc
