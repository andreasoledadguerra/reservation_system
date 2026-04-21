from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.booking import Room, Booking

class BookingService:

    @staticmethod
    async def pessimistic_booking(db: AsyncSession, room_id: int, email:str):
        # Lock the row to prevent dirty reads
        stmt = select(Room).where(Room.id == room_id).with_for_update()
        result = await db.execute(stmt)
        room = result.scalar_one_or_none()

        if not room:
            return {"error":"Room not found"}
        
        if room.available > 0:
            room.available -= 1
            new_booking = Booking(room_id, user_email=email)
            db.add(new_booking)
            await db.commit()
            return {"message": f"Booking confirmed for {email}", "available": room.available}
        else:
            await db.rollback()
            return {"error": "No availability"}
        
