from app.redis.redis_client import redis_client


def blacklist_token(token: str, expires_in: int):
    redis_client.setex(
        f"blacklist:{token}",
        expires_in,
        "true"
    )


def is_blacklisted(token: str) -> bool:
    return redis_client.exists(
        f"blacklist:{token}"
    ) == 1