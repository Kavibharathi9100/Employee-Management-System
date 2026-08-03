from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.core.security import hash_password, verify_password

from app.core.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
)

from app.auth.oauth2 import get_current_user
from app.services.email_service import send_reset_email
from app.core.config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==================================================
# Get Logged-in User
# ==================================================
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# ==================================================
# Register User
# ==================================================
@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role="employee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==================================================
# Login
# ==================================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": user.email}
    )

    refresh_token = create_refresh_token(
        {"sub": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ==================================================
# Refresh Access Token
# ==================================================
@router.post("/refresh")
def refresh_access_token(
    request: RefreshTokenRequest
):

    payload = verify_token(request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    access_token = create_access_token(
        {"sub": email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==================================================
# Change Password
# ==================================================
@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not verify_password(
        request.current_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Current password is incorrect"
        )

    if verify_password(
        request.new_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as current password"
        )

    current_user.password = hash_password(
        request.new_password
    )

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Password changed successfully"
    }


# ==================================================
# Forgot Password
# ==================================================
@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    reset_token = create_access_token(
        {"sub": user.email}
    )

    reset_link = (
        f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    )

    send_reset_email(
        to_email=user.email,
        reset_link=reset_link
    )

    return {
        "message": "Password reset link sent successfully"
    }


# ==================================================
# Reset Password
# ==================================================
@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    payload = verify_token(request.token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(
        request.new_password
    )

    db.commit()
    db.refresh(user)

    return {
        "message": "Password reset successfully"
    }