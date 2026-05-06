import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from app.main import app

        
@pytest.mark.asyncio
async def test_pessimistic_concurrency(sample_room):
    """ 10 concurrent users are trying to book the same room (pessimistic locking)."""
    room_id = sample_room.id 
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        task = [
            client.post(f"/api/v1/bookings/pessimistic/{room_id}", json={"email": f"user{i}@test.com"})
            for i in range(10)
        ]       
        responses = await asyncio.gather(*task) 

    sucess_count = sum(1 for r in responses if r.status_code == 200)
    error_count = sum(1 for r in responses if r.status_code == 400)
    assert sucess_count == 1, f"Only one booking must be successful, but it gets {sucess_count}"
    assert error_count == 9, f"9 requests must fail, but {error_count} failed"


@pytest.mark.asyncio
async def test_optimistic_concurrency(sample_room):
    """“10 concurrent users attempt to reserve the same room (optimistic locking)"""
    room_id = sample_room.id
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tasks = [
            client.post(f"/api/v1/bookings/optimistic/{room_id}", json={"email": f"user{i}@test.com"})
            for i in range(10)
        ]
        responses = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in responses if r.status_code == 200)
    conflict_count = sum(1 for r in responses if r.status_code == 409)
    other_errors = sum(1 for r in responses if r.status_code == 400) 
    assert success_count == 1, "Only one must be succesful"
    assert conflict_count >= 1, "Some requests must return a 409 Conflict"