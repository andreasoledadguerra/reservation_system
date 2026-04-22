from fastapi import FastAPI
from app.api.v1.endpoints import bookings
from app.core.database import engine, Base

app = FastAPI(title="Concurrent booking system")

app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["reservas"])

