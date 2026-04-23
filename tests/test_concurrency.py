import asyncio
import pytest

from httpx import AsynClient
from app.main import app
from app.core.database import engine, Base
from app.models.booking import Room


@pytest.fixture(scope="module")
async def setup_db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Insert a test room with 1 available spot
    async with engine.begin() as conn:
        room = Room(name= "Test Room", total_capacity=1, available=1)
        conn.add(room)
        await conn.commit()
    yield
    # Teardown: drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        