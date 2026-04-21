# pessimistic & optimistic endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.booking_service import BookingService
from pydantic import BaseModel

router = APIRouter()

