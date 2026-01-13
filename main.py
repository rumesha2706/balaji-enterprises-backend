from fastapi import FastAPI
from database import engine, Base
from routers import farmers, products, transactions, ocr
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Sri Balaji Enterprises API", lifespan=lifespan)

app.include_router(farmers.router)
app.include_router(products.router)
app.include_router(transactions.router)
app.include_router(ocr.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sri Balaji Enterprises API"}

