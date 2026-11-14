from pydantic import BaseModel, ConfigDict


class FilmWork(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')
    id: str
    title: str
    description: str | None
    imdb_rating: float | 0
