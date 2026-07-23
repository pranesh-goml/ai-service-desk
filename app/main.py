from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.middleware.response_time import add_response_time_header
from app.api.ticket_routes import router as ticket_routes
from app.core.deps import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    yield
    print("Application stopped")
app = FastAPI(title="Ticket API",lifespan=lifespan)
app.middleware("http")(add_response_time_header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ticket_routes)

@app.get("/health")
async def health():
    return {"status": "healthy"}
@app.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )