from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import bookings
from app.core.database import engine, Base


app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["reservas"])

@asynccontextmanager 
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized (tables created)")
    
    yield

    await engine.dispose()
    print("Database engine closed. Connections released.")


