from elasticsearch import AsyncElasticsearch
import pytest_asyncio
import pytest
from elasticsearch.helpers import async_bulk
from tests.functional.settings import test_settings
from tests.functional.testdata.es_data import get_test_data

@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='es_write_data')
async def es_write_data(es_client):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index,
                                       body={"settings": test_settings.es_index_settings,
                                              "mappings": test_settings.es_index_mapping
                                            }
                                       )
        action_info, errors = await async_bulk(client=es_client, actions=data, raise_on_error=False)

        if errors:
            for error in errors:
                print('ES error:', error)
            print('ES error:', errors)
            raise Exception(f'Ошибка записи: {errors}')
    return inner


@pytest.fixture(name='generated_query_data')
def generated_query_data(request):
    count = request.param
    return get_test_data(count)