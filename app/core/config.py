#Gestión de variables de entorno y configuración

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME:str = "Concurrent Reservation System"
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/bookings_db"

    class Config:
        env_file = ".env"

settings = Settings()