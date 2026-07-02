import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Single Redis client used across the project
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def check_redis_connection():
    """
    Check whether Redis is available.
    """
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False