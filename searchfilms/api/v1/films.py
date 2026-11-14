from typing import Annotated, List, Optional
from uuid import UUID
from core.logger import logger

from core.http_code import (HTTP_CLIENT_ERROR, HTTP_SERVER_ERROR,
                            HTTP_VALIDATION_ERROR)
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from schemas.FilmRequest import FilmRequest
from schemas.FilmResponse import FilmResponse
from services.FilmWorkService import FilmWorkService, film_service_di

router = APIRouter()


@router.get(
    '/search',
    summary='Поиск кинопроизведений по жанру',
    response_description='Название и рейтинг фильма',
)
async def film_search(
    request: Annotated[FilmRequest, Depends()],
    film_service: FilmWorkService = Depends(film_service_di),
) -> List[FilmResponse]:

    movies: List[FilmResponse] = []
    try:
        result = await film_service.search_films(request)
        for movie in result:
            item = FilmResponse.model_validate(movie)
            movies.append(item)
        return movies
    except ValidationError as exp:
        logger.error(str(exp))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Ошибка валидации данных',
        )
    except ValueError as exp:
        logger.error(str(exp))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ошибка на стороне клиентского запроса: нет фильмов по жанру.',
        )
    except Exception as exp:
        logger.error(str(exp))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка сервера'
        )


@router.get(
    '/{film_id}',
    summary='Кино',
    description='Поиск по id',
    response_description='Название и рейтинг фильма',
)
async def film_details(
    film_id: UUID, film_service: FilmWorkService = Depends(film_service_di)
) -> Optional[FilmResponse]:
    try:
        film = await film_service.get_film(str(film_id))
        if film:
            return FilmResponse(
                uuid=str(film.id), title=film.title, imdb_rating=film.rating
            )
    except ValueError as exp:
        logger.error(str(exp))
        raise HTTPException(
            status_code=HTTP_CLIENT_ERROR,
            detail=f'Ошибка на стороне клиентского запроса',
        )
    except Exception as exp:
        logger.error(str(exp))
        raise HTTPException(
            status_code=HTTP_SERVER_ERROR, detail=f'Ошибка сервера'
        )
