import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.password_reset import PasswordReset
from app.models.user import User


def create_reset_token(
    db: Session,
    email: str
):
    token = secrets.token_urlsafe(32)

    expires = datetime.now(timezone.utc) + timedelta(minutes=30)

    reset = PasswordReset(
        email=email,
        token=token,
        expires_at=expires
    )

    db.add(reset)
    db.commit()

    return token


def reset_password(
    db: Session,
    token: str,
    new_password: str,
):
    reset_record = (
        db.query(PasswordReset)
        .filter(PasswordReset.token == token)
        .first()
    )

    if not reset_record:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )

    if reset_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Reset token expired"
        )

    user = (
        db.query(User)
        .filter(User.email == reset_record.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(new_password)

    db.delete(reset_record)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Password has been reset successfully"
    }