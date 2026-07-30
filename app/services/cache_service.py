import json

from app.redis.redis_client import redis_client


class CacheService:

    @staticmethod
    def get(key: str):

        data = redis_client.get(key)

        if data:
            return json.loads(data)

        return None

    @staticmethod
    def set(
        key: str,
        value,
        ttl: int = 60
    ):

        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )

    @staticmethod
    def delete(key: str):

        redis_client.delete(key)