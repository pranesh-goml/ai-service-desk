import os
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

if os.getenv("ENV_FILE") == ".env.test":
    engine=create_async_engine(settings.DATABASE_URL,echo=True,poolclass=NullPool)
else:
    engine=create_async_engine(settings.DATABASE_URL,echo=True,pool_size=5,max_overflow=10,pool_recycle=1800)

asyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass