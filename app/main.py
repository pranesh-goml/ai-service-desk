from contextlib import asynccontextmanager


from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.response_time import add_response_time_header
from app.api.ticket_routes import router as ticket_routes
from app.api.ai import router as ai_routes
from app.core.deps import get_db
import boto3
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    app.state.bedrock = boto3.client(
        "bedrock-runtime",
        region_name=settings.AWS_REGION,
    )
    yield
    print("Application stopped")
    app.state.bedrock.close()

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
app.include_router(ai_routes)

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Database session not available"
        )

    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}
