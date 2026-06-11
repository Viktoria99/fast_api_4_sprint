from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.FilmRequest import FilmRequest
from schemas.FilmResponse import FilmResponse
from services.FilmWorkService import FilmWorkService, film_service_di

router = APIRouter()


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


@router.get(
    '/{film_id}',
    summary='Кино',
    description='Поиск по id',
    response_description='Название и рейтинг фильма',
)
async def film_details(
    film_id: str, film_service: FilmWorkService = Depends(film_service_di)
) -> FilmResponse:
    if is_valid_uuid(film_id) == True:
        film = await film_service.get_film(film_id)
        return FilmResponse(
            uuid=str(film.id), title=film.title, imdb_rating=film.rating
        )
    return None


@router.get(
    '/',
    response_model=List[FilmResponse],
    summary='Поиск кинопроизведений',
    description='Полнотекстовый поиск по кинопроизведениям',
    response_description='Название и рейтинг фильма',
)
async def film_search(
    request: Annotated[FilmRequest, Depends()],
    film_service: FilmWorkService = Depends(film_service_di),
) -> List[FilmResponse]:
    movies: List[FilmResponse] = []
    if request.genre != None:
        result = await film_service.get_films_from_elastic(request)
        for movie in result:
            item = FilmResponse(
                uuid=str(movie.id), title=movie.title, imdb_rating=movie.rating
            )
            movies.append(item)
    return movies
