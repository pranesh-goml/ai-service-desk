import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


os.environ["ENV_FILE"] = ".env.test"

from app.main import app
from app.core.deps import get_db
from app.core.database import asyncSessionLocal, engine, Base
from app.models.ticket_model import Ticket
import asyncio

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    async def _setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_setup())
    yield
    
    async def _teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            
    asyncio.run(_teardown())


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with asyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()