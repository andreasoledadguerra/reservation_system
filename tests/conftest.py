import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import engine, Base
from app.models. booking import Room

# Create an asynchronous session factory (using actual engine)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
