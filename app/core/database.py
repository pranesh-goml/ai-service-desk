from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine=create_async_engine(settings.DATABASE_URL,echo=True,pool_size=5,max_overflow=10,pool_recycle=1800)
asyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass