from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.jwt_handler import ALGORITHM

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    payload = data.copy()

    payload.update(
        {
            "exp": expire,
            "type": "refresh"
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )