from functools import wraps
import time
import redis
from fastapi import HTTPException, status, Request


class RateLimiter:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis_pool = redis.ConnectionPool(
            host=redis_host, port=redis_port, db=0, decode_responses=True)

    def get_redis(self):
        return redis.Redis(connection_pool=self.redis_pool)

    def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
        current = int(time.time())
        window_start = current - window
        redis_conn = self.get_redis()
        with redis_conn.pipeline() as pipe:
            try:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {current: current})
                pipe.expire(key, window)
                results = pipe.execute()
            except redis.RedisError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Redis error: {str(e)}"
                ) from e
        return results[1] > max_requests


rate_limiter = RateLimiter('cache', 6379)

def rate_limit(max_requests: int, window: int):
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            key = f"rate_limit:{request.client.host}:{request.url.path}"
            if rate_limiter.is_rate_limited(key, max_requests, window):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
