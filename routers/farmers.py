from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import models, schemas, database
from ..services import interest
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(
    prefix="/farmers",
    tags=["farmers"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Farmer)
async def create_farmer(farmer: schemas.FarmerCreate, db: AsyncSession = Depends(database.get_db)):
    db_farmer = models.Farmer(**farmer.dict())
    db.add(db_farmer)
    await db.commit()
    await db.refresh(db_farmer)
    return db_farmer

@router.get("/", response_model=List[schemas.Farmer])
async def read_farmers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Farmer).offset(skip).limit(limit))
    farmers = result.scalars().all()
    return farmers

@router.get("/{farmer_id}", response_model=schemas.Farmer)
async def read_farmer(farmer_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Farmer).filter(models.Farmer.id == farmer_id))
    farmer = result.scalars().first()
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

@router.post("/{farmer_id}/calculate-interest", response_model=schemas.InterestResult)
async def calculate_farmer_interest(
    farmer_id: int, 
    request: schemas.InterestRequest, 
    db: AsyncSession = Depends(database.get_db)
):
    # Fetch all credit transactions for the farmer
    query = select(models.Transaction).filter(
        models.Transaction.farmer_id == farmer_id,
        models.Transaction.type == "Credit"
    )
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    total_principal = 0.0
    total_interest = 0.0
    details = []
    
    end_date = request.end_date or datetime.utcnow()
    
    for txn in transactions:
        # Use transaction date if specific start date not provided, or max of both
        start_date = txn.date
        if request.start_date and request.start_date > start_date:
            start_date = request.start_date
            
        calc = interest.calculate_interest(
            principal=txn.amount,
            rate_per_month=request.rate_per_month,
            start_date=start_date,
            end_date=end_date,
            interest_type=request.interest_type
        )
        
        total_principal += txn.amount
        total_interest += calc['interest']
        
        details.append({
            "transaction_id": txn.id,
            "date": txn.date,
            "principal": txn.amount,
            "interest": calc['interest'],
            "months": calc['months']
        })
        
    return {
        "principal": total_principal,
        "interest": total_interest,
        "total_amount": total_principal + total_interest,
        "details": details
    }
