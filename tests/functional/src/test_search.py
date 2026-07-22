import aiohttp
import pytest

from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'generated_query_data, query_data',
    [
        (
            50,
            {
                'sort': '-imdb_rating',
                'genre': 'Action',
                'page_size': 5,
                'page_number': 1,
                'uuid': 'some',
            },
        )
    ],
    indirect=['generated_query_data'],
)
@pytest.mark.asyncio
async def test_search_genre_actions(
    generated_query_data, query_data, es_write_data
):

    bulk_query: list[dict] = []
    for row in generated_query_data:
        data = {'_index': 'test_movies', '_id': row['id'], '_source': row}
        bulk_query.append(data)

    await es_write_data(bulk_query)

    async with aiohttp.ClientSession() as session:
        url = test_settings.service_url + '/api/v1/films/search'
        async with session.get(url, params=query_data) as response:
            status = response.status
            body = await response.text()
            print(f'Body ОШИБКА: {body}')

    assert status == 200, f'Сервис вернул {status}: {body}'


@pytest.mark.parametrize(
    'query_data',
    [
        (
            {
                'genre': 'None',
                'sort': '-imdb_rating',
                'page_size': 5,
                'page_number': 1,
                'uuid': '',
            }
        )
    ],
)
@pytest.mark.asyncio
async def test_search_genre_none_error(query_data, es_write_data):
    async with aiohttp.ClientSession() as session:
        url = test_settings.service_url + '/api/v1/films/search'
        async with session.get(url, params=query_data) as response:
            status = response.status
            body = await response.text()
            print(f'Body ОШИБКА: {body}')

    assert status == 500, f'Сервис вернул номер ошибки = {status}'
