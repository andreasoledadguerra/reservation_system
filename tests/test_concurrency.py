import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.main import app
from app.core.database import engine, Base
from app.models.booking import Room

# Create an asynchronous session factory (using actual engine)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

#@pytest_asyncio.fixture(scope="module")
@pytest_asyncio.fixture(scope="function")

async def setup_db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Insert a test room with 1 available spot
    async with AsyncSession(engine) as conn:
        room = Room(name= "Test Room", total_capacity=1, available=1)
        conn.add(room)
        await conn.commit()
    
    ## Insert fresh room
    #async with async_session() as session:
    #    room = Room(name="Test Room", available=1, version=0)
    #    session.add(room)
    #    await session.commit()
    yield
    # Teardown: drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
@pytest.mark.asyncio
async def test_pessimistic_concurrency(setup_db):
    room_1 = 1
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        task = [
            client.post(f"/api/v1/reservas/pessimistic/{room_1}", json={"email": f"user{i}@test.com"})
            for i in range(10)
        ]       
        responses = await asyncio.gather(*task) #throw 10 requestes at the same time

    sucess_count = sum(1 for r in responses if r.status_code == 200)
    error_count = sum(1 for r in responses if r.status_code == 400)
    assert sucess_count == 1, f"Only one booking must be successful, but it gets {sucess_count}"
    assert error_count == 9, f"9 requests must fail, but {error_count} failed"

@pytest.mark.asyncio
async def test_optimistic_concurrency(setup_db):
    """10 usuarios concurrentes intentan reservar la misma habitación (bloqueo optimista)"""
    room_id = 1
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tasks = [
            client.post(f"/api/v1/reservas/optimistic/{room_id}", json={"email": f"user{i}@test.com"})
            for i in range(10)
        ]
        responses = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in responses if r.status_code == 200)
    conflict_count = sum(1 for r in responses if r.status_code == 409)
    other_errors = sum(1 for r in responses if r.status_code == 400) 
    assert success_count == 1, "Only one must be succesful"
    assert conflict_count >= 1, "Some requests must return a 409 Conflict"