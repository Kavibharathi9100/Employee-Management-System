from app.redis.redis_client import redis_client

redis_client.set("company", "HRMS")

print(redis_client.get("company"))