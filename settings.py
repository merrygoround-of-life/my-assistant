from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "postgres"
    pg_password: str = "postgres"
    pg_database: str = "my-assistant"

    mg_host: str = "localhost"
    mg_port: int = 27017
    mg_username: str = "mongo"
    mg_password: str = "mongo"
    mg_database: str = "my-assistant"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
