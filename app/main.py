from fastapi import FastAPI
from app.api.ticket_routes import router as ticket_routes
app = FastAPI()
app.include_router(ticket_routes)