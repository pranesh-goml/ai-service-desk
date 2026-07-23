import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

# ----------------------------------------------------
# Project Root
# ----------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# ----------------------------------------------------
# Test Environment
# ----------------------------------------------------

os.environ["ENV_FILE"] = ".env.test"

# ----------------------------------------------------
# Application Imports
# ----------------------------------------------------

from app.main import app
from app.core.deps import get_db
from app.core.database import asyncSessionLocal

# ----------------------------------------------------
# Database Session Fixture
# ----------------------------------------------------

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with asyncSessionLocal() as session:
        yield session
        await session.rollback()

# ----------------------------------------------------
# Override get_db Dependency
# ----------------------------------------------------

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