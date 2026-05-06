import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import engine, Base
from app.models. booking import Room

# Create an asynchronous session factory (using actual engine)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def create_tables():
    """One key responsibility: create all tables before the test and delete them afterward."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def sample_room(create_tables):
    """“Single responsibility: insert a test room with available=1 and version=0."""
    async with AsyncSessionLocal() as session:
        room = Room(name="Test Room", total_capacity=1, available=1, version=0)
        session.add(room)
        await session.commit()
        return room  # The test can access the Room object if necessary