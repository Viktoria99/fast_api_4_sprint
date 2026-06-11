import datetime
from datetime import datetime as datetime_format
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class Model:
    id: UUID


class FilmWork(BaseModel, Model):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    title: str
    description: str | None
    rating: float | None
    modified: datetime_format | None

    def __init__(
        self,
        id: UUID,
        title: str,
        description: str,
        rating: float,
        modified: datetime_format,
    ):
        super().__init__(
            id=id,
            title=title,
            description=description,
            rating=rating,
            modified=modified,
        )


class Genre(BaseModel, Model):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    name: str
    description: str | None
    created: datetime_format
    modified: datetime_format

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        created: datetime_format,
        modified: datetime_format,
    ):
        super().__init__(
            id=id,
            name=name,
            description=description,
            created=created,
            modified=modified,
        )


class Person(BaseModel, Model):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    full_name: str
    role: str
    created: datetime_format
    modified: datetime_format

    def __init__(
        self,
        id: UUID,
        full_name: str,
        role: str,
        created: datetime,
        modified: datetime,
    ):
        super().__init__(
            id=id,
            full_name=full_name,
            role=role,
            created=created,
            modified=modified,
        )

    @field_validator('created', mode='before')
    @classmethod
    def to_timezone(cls, v):
        if isinstance(v, str):
            fd = datetime_format.strptime(v + '00', '%Y-%m-%d %H:%M:%S.%f%z')
            return fd
        return v

    @field_validator('modified', mode='before')
    @classmethod
    def modified_timezone(cls, v):
        if isinstance(v, str):
            fd = datetime_format.strptime(v + '00', '%Y-%m-%d %H:%M:%S.%f%z')
            return fd
        return v


class Movie_item(dict):
    def __init__(self, Id: UUID, Name: str):
        dict.__init__(self, id=str(Id), name=Name)
