from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):

    host: str
    port: int
    dbname: str
    user: str
    password: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='sql_',
    )

    def get_dsn(self) -> dict:
        return self.model_dump()


class ElasticsearchSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='elk_',
    )
    host: str
    port: str

    def get_host(self):
        return f'http://{self.host}:{self.port}'


class EltSettings(BaseSettings):
    index: str
    batch_size: int
    film_count: str
    state_key: str
    state_path: str
    max_tries: int
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='elt_',
    )


class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()
    elasticsearch_settings: ElasticsearchSettings = ElasticsearchSettings()
    elt_settings: EltSettings = EltSettings()


settings = Settings()
