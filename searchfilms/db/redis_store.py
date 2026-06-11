import json

import backoff
import redis
from core.logger import logger
from fastapi import Depends, Request
from redis.asyncio import Redis


def get_redis(request: Request) -> Redis:
    return request.app.state.redis_client


class RedisStore:
    def __init__(self, redis: Redis):
        self.redis_client = redis

    @backoff.on_exception(
        backoff.expo,
        redis.ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    @backoff.on_exception(
        backoff.expo,
        redis.TimeoutError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    async def get(self, key: str) -> dict | None:
        value = await self.redis_client.get(key)
        return json.loads(value) if value else None

    @backoff.on_exception(
        backoff.expo,
        redis.ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    @backoff.on_exception(
        backoff.expo,
        redis.TimeoutError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    async def saveItem(self, key: str, value: dict) -> None:
        await self.redis_client.set(key, json.dumps(value), ex=600)


def get_redis_store(redis: Redis = Depends(get_redis)) -> RedisStore:
    return RedisStore(redis)
