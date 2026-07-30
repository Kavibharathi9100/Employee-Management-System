from typing import List
from fastapi import Depends, HTTPException
from app.auth.oauth2 import get_current_user
from app.models.user import User


def require_role(required_roles: List[str]):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        print("=" * 50)
        print("Email :", current_user.email)
        print("Role  :", current_user.role)
        print("Allowed:", required_roles)
        print("=" * 50)

        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to perform this action."
            )

        return current_user

    return role_checker