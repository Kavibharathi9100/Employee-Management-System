from fastapi import HTTPException, status

from app.core.jwt_handler import (
    verify_token,
    create_access_token
)


def refresh_access_token(refresh_token: str):

    payload = verify_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    access_token = create_access_token(
        {
            "sub": payload["sub"],
            "role": payload["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }