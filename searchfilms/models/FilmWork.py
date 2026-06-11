from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class Model:
    id: UUID


class FilmWork(BaseModel, Model):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    title: str
    description: str | None
    rating: float | None

    def __init__(self, id: UUID, title: str, description: str, rating: float):
        super().__init__(
            id=id, title=title, description=description, rating=rating
        )
