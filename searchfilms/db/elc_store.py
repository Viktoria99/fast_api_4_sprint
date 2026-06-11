from typing import Any, Optional

import backoff
from core.logger import logger
from elasticsearch import (AsyncElasticsearch, ConnectionError,
                           ConnectionTimeout, NotFoundError)
from fastapi import Depends, Request


def get_elastic(request: Request) -> AsyncElasticsearch:
    print(request.app.state.elastic_client)
    return request.app.state.elastic_client


class ElcStore:
    def __init__(self, elc: AsyncElasticsearch):
        self.elc_client = elc

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    @backoff.on_exception(
        backoff.expo,
        ConnectionTimeout,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    async def get(
        self, index_name: str, uuid: str
    ) -> Optional[dict[str, Any]]:
        try:
            data = await self.elc_client.get(index=index_name, id=uuid)
            return data
        except NotFoundError:
            raise

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    @backoff.on_exception(
        backoff.expo,
        ConnectionTimeout,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger,
    )
    async def get_films(
        self, index_name: str, query: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        try:
            data = await self.elc_client.search(index=index_name, body=query)
            return data
        except NotFoundError:
            raise


def get_elc_store(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElcStore:
    return ElcStore(elastic)
