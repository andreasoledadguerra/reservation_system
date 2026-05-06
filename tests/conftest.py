import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import engine, Base
from app.models. booking import Room

# Create an asynchronous session factory (using actual engine)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def create_tables():
    """One key responsibility: create all tables before the test and delete them afterward."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)