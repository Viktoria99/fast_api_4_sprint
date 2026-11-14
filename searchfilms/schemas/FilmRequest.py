from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class FilmRequest(BaseModel):
    sort: Annotated[
        str,
        Field(
            '-imdb_rating',
            description='Сортировка',
            title='sort1',
            alias='sort',
        ),
    ]
    genre: Annotated[
        str,
        Field(description='Поиск по жанру', title='genre1', alias='genre'),
    ]
    page_size: int | None = Field(default=10, ge=1, le=100)
    page_number: int | None = 1
