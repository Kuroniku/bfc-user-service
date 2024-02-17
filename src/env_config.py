from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    db_name: str = Field(alias='DB_NAME', default='user-db')
    db_user: str = Field(alias='DB_USER', default='psql')
    db_password: str = Field(alias='DB_PASSWORD', default='psql')
    db_host: str = Field(alias='DB_HOST', default='localhost')
    db_port: str = Field(alias='DB_PORT', default='5432')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    @property
    def sync_psql_url(self) -> str:
        return (f'postgresql+psycopg2://{self.db_user}:{self.db_password}@'
                f'{self.db_host}:{self.db_port}/{self.db_name}')

    @property
    def async_psql_url(self) -> str:
        return (f'postgresql+asyncpg://{self.db_user}:{self.db_password}@'
                f'{self.db_host}:{self.db_port}/{self.db_name}')


env_config = EnvConfig()

__all__ = ['env_config']
