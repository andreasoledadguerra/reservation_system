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
        
        
    @staticmethod
    async def optimistic_booking(db: AsyncSession, room_id: int, email:str):
        # Read without locking
        result = await db.execute(select(Room).where(Room.id == room_id))
        room = result.scalar_one_or_none()

        if not room:
            return {"error": "Room not found"}
        if room.available <= 0:
            return {"error": "No availablity"}
        
        current_version = room.version

        # Conditional update (WHERE version = :current_version)
        stmt = (
            update(Room)
            .where(Room.id == room_id, Room.version == current_version)
            .values(available=Room.available -1, version=Room.version + 1)
        )
        result_update = await db.execute(stmt)

        if result_update.rowcount == 0:
            # Conflict: someone modified the row before us
            await db.rollback()
            return {"error": "Concurrency conflict. Please retry."}
        
        # If updated succesfully, create the booking record
        new_booking = Booking(room_id=room_id, user_email=email)
        db.add(new_booking)
        await db.commit()
        return {"message": f"Booking confirmed for {email} (Optimistic)"}