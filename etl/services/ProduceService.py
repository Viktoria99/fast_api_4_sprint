import backoff
import psycopg
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic_settings import BaseSettings
from sql_command import get_batch_count, select_film, select_film_count


class ProducerService:
    dsn: str

    def __init__(self, settings: BaseSettings, pool: ConnectionPool) -> None:
        self.dsn = make_conninfo(**settings.database_settings.get_dsn())
        self.batch = settings.elt_settings.batch_size
        self.film_count = settings.elt_settings.film_count
        self.pool = pool

    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionTimeout,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionException,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionFailure,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    def get_film(self, load_date: str) -> None:
        with self.pool.connection() as pg_conn:
            with pg_conn.cursor(row_factory=dict_row) as cur:
                raws = cur.execute(
                    select_film_count.format(load_date)
                ).fetchone()
                batch_count = get_batch_count(
                    raws[self.film_count], self.batch
                )

                sql_film = select_film.format(load_date)
                cur.execute(sql_film)
                for i in range(batch_count):
                    film_list = cur.fetchmany(self.batch)
                    yield film_list
                pg_conn.commit()
