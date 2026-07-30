from typing import Generator


from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL

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
        