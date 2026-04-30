import asyncio
import pytest

from httpx import AsynClient, ASGITransport
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
        
@pytest.mark.asyncio
async def test_pessimistic_concurrency(setup_db):
    room_1 = 1
    async with AsynClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        task = [
            client.post(f"/api/v1/reservas/pessimistic/{room_1}", json={"email": f"user{i}@test.com"})
            for i in range(10)
        ]       
        responses = await asyncio.gather(*task) #throw 10 requestes at the same time

    sucess_count = sum(1 for r in responses if r.status_code == 200)
    error_count = sum(1 for r in responses if r.status_code == 400)


    assert sucess_count == 1, f"Only one booking must be successful, but it gets {sucess_count}"
    assert error_count == 9, f"9 requests must fail, but {error_count} failed"
        