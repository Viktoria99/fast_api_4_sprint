import aiohttp
import pytest

from tests.functional.settings import test_settings


@pytest.mark.parametrize('query_data', [({'film_id': ''})])
@pytest.mark.asyncio
async def test_film_uuid_empty_string_error(query_data):
    async with aiohttp.ClientSession() as session:
        url = test_settings.service_url + '/api/v1/films'
        async with session.get(url, params=query_data) as response:
            status = response.status
            body = await response.text()
            print(f'Body ОШИБКА: {body}')
            assert status == 404, f'Номер ошибки = {status}'
