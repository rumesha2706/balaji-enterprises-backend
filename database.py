from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL usage: postgresql+asyncpg://user:password@host/dbname
# For now using sqlite for easy setup/dev as placeholder, but plan specified Postgres.
# I will use an environment variable for the DB URL.
import os

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/balaji_db")
# Using SQLite for local dev run to avoid password issues
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./balaji.db")

engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
