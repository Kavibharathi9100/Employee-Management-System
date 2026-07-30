from typing import Generator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.core.config import settings

password = quote_plus(settings.DB_PASSWORD)
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{password}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

# Create SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)


# Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all models
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI routes
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        