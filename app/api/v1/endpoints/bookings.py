# pessimistic & optimistic endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.booking_service import BookingService
from pydantic import BaseModel

router = APIRouter()

class BookingRequest(BaseModel):
    email: str

@router.post("/pessimistic/{room_id}")
async def create_pessimistic_booking(
    room_id: int,
    payload: BookingRequest,
    db: AsyncSession = Depends(deps.get_db)    
):
    result = await BookingService.pessimistic_booking(db, room_id, payload.email)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("optimistic/{room_id}")
async def create_optimistic_booking(
    room_id: int,
    payload: BookingRequest,
    db: AsyncSession = Depends(deps.get_db)
):
    result = await BookingService.optimistic_booking(db, room_id, payload.email)
    if "error" in result:
        #Return 409 Conflict so tehe frontend can automatically  retry
        status_code = 409 if "Conflict" in result["error"] else 400
        raise HTTPException(status_code=status_code, detail=result["error"])
    return result