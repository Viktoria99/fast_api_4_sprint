from typing import List

from constants import *
from logger import logger_load
from models.models import FilmWork, Movie_item
from psycopg.conninfo import make_conninfo
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from pydantic_settings import BaseSettings
from sql_command import *
from sql_command import get_first


class EnricherService:
    dsn: str

    def __init__(
        self, settings_db: BaseSettings, pool: ConnectionPool
    ) -> None:
        self.dsn = make_conninfo(**settings_db.database_settings.get_dsn())
        self.pool = pool

    def richer_films(self, id_list: List) -> List:
        film_list = []
        for id in id_list:
            try:
                film = self.get_film(id['id'])
                genres = self.get_film_genre(id['id'])
                film.genres = genres
                # film.__dict__[GENRES] = genres

                film_card = self.get_film_person(id['id'], film)
                film_list.append(film_card)
            except Exception as err:
                logger_load.error(
                    'Film_Id-{Id}: def richer_films -> {Errors}'.format(
                        Id=id['id'], Errors=err
                    )
                )
        return film_list

    def get_film(
        self,
        film_id: str,
    ) -> FilmWork:
        with self.pool.connection() as pg_conn:
            with pg_conn.cursor(row_factory=dict_row) as cur:
                sql = select_one_film.format(film_id)
                film = cur.execute(sql).fetchone()
                return FilmWork(**film)

    def get_film_genre(self, film_id: str) -> List:
        with self.pool.connection() as pg_conn:
            with pg_conn.cursor() as cur:
                genre_sql = select_film_genre.format(film_id)
                genre_list = cur.execute(genre_sql).fetchall()
                genres = [map(get_first, genre_list)]
                return genres

    def get_film_person(self, film_id: str, film: FilmWork) -> FilmWork:
        with self.pool.connection() as pg_conn:
            with pg_conn.cursor(row_factory=dict_row) as cur:
                person_list = cur.execute(
                    select_film_person.format(film_id)
                ).fetchall()

                film.directors_names = [
                    person['full_name']
                    for person in person_list
                    if person['role'] == DIRECTOR
                ]
                film.actors_names = [
                    person['full_name']
                    for person in person_list
                    if person['role'] == ACTOR
                ]
                film.writers_names = [
                    person['full_name']
                    for person in person_list
                    if person['role'] == WRITER
                ]
                film.directors = [
                    Movie_item(person['id'], person['full_name'])
                    for person in person_list
                    if person['role'] == DIRECTOR
                ]
                film.actors = [
                    Movie_item(person['id'], person['full_name'])
                    for person in person_list
                    if person['role'] == ACTOR
                ]
                film.writers = [
                    Movie_item(person['id'], person['full_name'])
                    for person in person_list
                    if person['role'] == WRITER
                ]

                return film
