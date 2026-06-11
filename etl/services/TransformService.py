import json
from typing import List

import backoff
from elasticsearch import ConnectionError, ConnectionTimeout, Elasticsearch
from elasticsearch.helpers import BulkIndexError, bulk
from logger import logger_load
from pydantic_settings import BaseSettings


class TransformService:
    def __init__(self, settings: BaseSettings):
        connect_etl = settings.elasticsearch_settings.get_host()
        self.etl_client = Elasticsearch(connect_etl)
        self.elt_index = settings.elt_settings.index

    def gendata(self, films: List):
        for item in films:
            item.id = str(item.id)
            del item.modified
            result = item.model_dump(mode='json')
            yield dict(_index=self.elt_index, _id=item.id, _source=result)

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger_load,
    )
    @backoff.on_exception(
        backoff.expo,
        ConnectionTimeout,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger_load,
    )
    def save_etl(self, films: List):
        try:
            bulk(self.etl_client, self.gendata(films))
        except BulkIndexError as e:
            logger_load.error(json.dumps(e.errors[0], indent=2))
            raise
