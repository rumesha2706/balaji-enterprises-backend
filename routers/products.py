from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import models, schemas, database
from sqlalchemy.future import select

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[schemas.Product])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products
