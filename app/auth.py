from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "mysql+aiomysql://your_username:your_password@your_mysql_host/your_database"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create Session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI Routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session