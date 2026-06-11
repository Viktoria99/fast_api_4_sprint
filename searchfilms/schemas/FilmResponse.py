from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class FilmResponse(BaseModel):
    uuid: Annotated[
        str, Field(validation_alias=AliasChoices('id', 'uuid'))
    ] = 'some_id'
    title: str = 'some_title'
    imdb_rating: float = 0.0
