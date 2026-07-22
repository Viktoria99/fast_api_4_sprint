from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import ValidationError
import traceback
import sys

from fastapi import APIRouter, Depends, HTTPException
from schemas.FilmRequest import FilmRequest
from schemas.FilmResponse import FilmResponse
from services.FilmWorkService import FilmWorkService, film_service_di
from core.http_code import HTTP_VALIDATION_ERROR, HTTP_SERVER_ERROR

router = APIRouter()


@router.get(
    '/search',
    summary='Поиск кинопроизведений',
    description='Полнотекстовый поиск по кинопроизведениям',
    response_description='Название и рейтинг фильма',
)
async def film_search(
        request: Annotated[FilmRequest, Depends()],
        film_service: FilmWorkService = Depends(film_service_di)
) -> List[FilmResponse]:

    movies: List[FilmResponse] = []
    try:
        result = await film_service.search_films(request)
        for movie in result:
            print('movie в API:')
            print(type(movie))
            print(movie)
            item = FilmResponse.model_validate(movie)
            movies.append(item)
        return movies
    except ValidationError as exp:
        stack_message = traceback.extract_stack()
        raise HTTPException(
            status_code=HTTP_VALIDATION_ERROR,
            detail=f"Ошибка валидации данных: {str(exp)}"
        )
    except ValueError as exp:
        raise HTTPException(
            status_code=HTTP_VALIDATION_ERROR,
            detail=f"Ошибка валидации данных в search: {str(exp)}, "

        )
    except Exception as exp:
        traceback.print_exception(exp, limit=2, file=sys.stdout)
        raise HTTPException(
            status_code=HTTP_SERVER_ERROR,
            detail=f"Ошибка сервера в search: {str(exp)}"
        )



@router.get(
    '/{film_id}',
    summary='Кино',
    description='Поиск по id',
    response_description='Название и рейтинг фильма',
)
async def film_details(
    film_id: str, film_service: FilmWorkService = Depends(film_service_di)
) -> Optional[FilmResponse]:
    try:
        UUID(film_id, version=4)
        film = await film_service.get_film(film_id)
        if film:
            return FilmResponse(
                uuid=str(film.id), title=film.title, imdb_rating=film.rating
            )
    except ValueError as exp:
        raise HTTPException(
            status_code=HTTP_VALIDATION_ERROR,
            detail=f"Ошибка валидации данных: {str(exp)}, "

        )
    except Exception as exp:
        raise HTTPException(
            status_code=HTTP_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(exp)}"
        )

