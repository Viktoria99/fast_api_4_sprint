import logging
from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from api.v1.films import router
from core.settings import settings
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = redis.ConnectionPool.from_url(
        settings.redis.get_url(), decode_responses=True
    )
    app.state.redis_client = redis.Redis(connection_pool=pool)
    app.state.elastic_client = AsyncElasticsearch(
        hosts=[settings.elastic.get_url()]
    )
    yield
    await app.state.redis_client.aclose()
    await app.state.elastic_client.close()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    openapi_url='/api/openapi.json',
    version='1.0.0',
)

app.include_router(router, prefix='/api/v1/films')

if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='localhost', port=8055, log_level=logging.DEBUG
    )
