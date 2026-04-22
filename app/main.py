from fastapi import FastAPI
from app.api.v1.endpoints import bookings
from app.core.database import engine, Base

app = FastAPI(title="Concurrent booking system")

