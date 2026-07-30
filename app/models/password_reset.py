from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False)

    token = Column(String, unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, server_default=func.now())