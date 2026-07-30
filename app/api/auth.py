from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.password_reset import ForgotPasswordRequest
from app.services.password_reset_service import create_reset_token
from app.celery.tasks import send_reset_email_task
from app.core.config import settings
from app.celery.celery_app import celery_app
from app.schemas.reset_password import ResetPasswordRequest
from app.services.password_reset_service import reset_password
from app.schemas.refresh_token import RefreshTokenRequest
from app.services.auth_service import refresh_access_token
from app.services.token_blacklist_service import blacklist_token
from fastapi import Depends

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from app.core.jwt_handler import (
    verify_token,
    get_token_remaining_time
)

security = HTTPBearer()
router = APIRouter()


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    token = create_reset_token(
        db,
        request.email
    )

    reset_link = (
        f"{settings.FRONTEND_URL}"
        f"/reset-password"
        f"?token={token}"
    )

    print("Broker:", celery_app.conf.broker_url)
    print("Connection:", celery_app.connection().as_uri())

    send_reset_email_task.delay(request.email, reset_link)

    return {
        "message": "Password reset email sent"
    }

@router.post("/reset-password")
def reset_password_api(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    # Step 1: Check password confirmation
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # Step 2: Call service
    return reset_password(
        db=db,
        token=request.token,
        new_password=request.new_password
    )

@router.post("/refresh-token")
def refresh_token_api(
    request: RefreshTokenRequest
):
    return refresh_access_token(
        request.refresh_token
    )

@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        print("Token:", token)

        payload = verify_token(token)
        print("Payload:", payload)

        expires_in = get_token_remaining_time(payload)
        print("Expires In:", expires_in)

        blacklist_token(token, expires_in)

        return {
            "message": "Logged out successfully"
        }

    except Exception as e:
        print("Logout Error:", repr(e))
        raise