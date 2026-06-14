from datetime import datetime
from pathlib import Path
from time import sleep

from logger import logger_load
from psycopg_pool import ConnectionPool
from services.EnricherService import EnricherService
from services.ProduceService import ProducerService
from services.TransformService import TransformService
from settings import settings
from state.State import State
from state.StateStorage import FileStorage


def main():

    state_path = (
        Path(__file__).resolve().parent.parent
        / settings.elt_settings.state_path
    )
    db_pool = ConnectionPool(
        conninfo='host={host} port={port} dbname={db} user={us} password={pas}'.format(
            host=settings.database_settings.host,
            port=settings.database_settings.port,
            db=settings.database_settings.dbname,
            us=settings.database_settings.user,
            pas=settings.database_settings.password,
        ),
        min_size=1,
        max_size=10,
    )

    state_storage = FileStorage(state_path)
    state = State(state_storage)

    producer_service = ProducerService(settings, db_pool)
    richer_service = EnricherService(settings, db_pool)
    transform_service = TransformService(settings)

    key_state = settings.elt_settings.state_key
    load_date = state.get_state(key_state)
    load = key_state if load_date == None else load_date
    logger_load.info(
        'Дата начала импорта данных = {date_load}'.format(date_load=load)
    )
    for item in producer_service.get_film(load):
        films = richer_service.richer_films(item)
        transform_service.save_etl(films)

    loc_dt = datetime.now()
    str_date = loc_dt.strftime('%Y-%m-%d %H:%M:%S')
    state.set_state(key_state, str_date)
    logger_load.info(
        'Окончание импорта данных = {end_date}'.format(end_date=str_date)
    )


if __name__ == '__main__':

    while True:
        try:
            main()
            sleep(600)
        except Exception as e:
            logger_load.exception(e)
