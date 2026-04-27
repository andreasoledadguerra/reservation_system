from pydantic import BaseModel

class RoomCreate(BaseModel):
    name: str
    total_capacity: int

class RoomResponse(BaseModel):
    id: int
    name: str
    available: int
    class Config:
        from_attributes = True