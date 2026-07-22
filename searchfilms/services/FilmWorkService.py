from typing import List, Optional

from db.elc_store import ElcStore, get_elc_store
from db.redis_store import RedisStore, get_redis_store
from elasticsearch import NotFoundError
from fastapi import Depends
from models.FilmWork import FilmWork
from schemas.FilmRequest import FilmRequest


class FilmWorkService:
    def __init__(self, redis: RedisStore, elc: ElcStore):
        self.redis_store = redis
        self.elc_store = elc

    async def get_film(self, uuid: str) -> Optional[FilmWork]:
        data = await self.redis_store.get(uuid)
        if not data:
            try:
                film_elc = await self.elc_store.get('movies', uuid)
                film_fields = film_elc['_source']
                await self.redis_store.saveItems(uuid, film_fields)
                return FilmWork(
                    film_fields['id'],
                    film_fields['title'],
                    film_fields['description'],
                    film_fields['imdb_rating'],
                )
            except NotFoundError:
                raise ValueError(f'Нет фильмов по id = {uuid}')
            except Exception:
                raise
        return FilmWork(
            data['id'], data['title'], data['description'], data['imdb_rating']
        )

    async def search_films(
        self, request: FilmRequest
    ) -> Optional[List[FilmWork]]:
        try:
            films = await self.redis_store.get(str(request))
            if not films:
                films = await self.get_films_from_elastic(request)
                if not films:
                    raise ValueError(f'Нет фильмов по жанру {request.genre}')
                filmsCash = [film.model_dump() for film in films]
                await self.redis_store.saveItems(str(request), filmsCash)
            return films
        except Exception:
            raise

    async def get_films_from_elastic(
        self, request: FilmRequest
    ) -> Optional[List[FilmWork]]:
        query = {}
        try:
            if request.sort == '-imdb_rating':
                query['sort'] = {'imdb_rating': 'desc'}
            else:
                query['sort'] = {'imdb_rating': 'asc'}
            query['query'] = {'term': {'genres': request.genre}}
            query['from'] = (request.page_number - 1) * request.page_size
            query['size'] = request.page_size

            doc = await self.elc_store.get_films('movies', query)
        except NotFoundError:
            return None
        except Exception:
            raise

        if doc['hits']['total']['value'] == 0:
            return None
        films: List[FilmWork] = []
        for movie in doc['hits']['hits']:
            film = movie['_source']
            film_item = FilmWork(
                id=film['id'],
                title=film['title'],
                description=film['description'],
                imdb_rating=film['imdb_rating'],
            )
            films.append(film_item)
        return films


def film_service_di(
    elastic: ElcStore = Depends(get_elc_store),
    redis: RedisStore = Depends(get_redis_store),
) -> FilmWorkService:
    return FilmWorkService(redis, elastic)
