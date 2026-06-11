from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticsearchSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='elk_',
    )
    host: str
    port: str
    index: str

    def get_url(self):
        return f'http://{self.host}:{self.port}'


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='redis_',
    )
    host: str
    port: str
    cash_time: int

    def get_url(self):
        return f'redis://{self.host}:{self.port}'


class Settings(BaseSettings):
    elastic: ElasticsearchSettings = ElasticsearchSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
