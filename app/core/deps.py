from app.core.database import asyncSessionLocal


async def get_db():
    async with asyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise