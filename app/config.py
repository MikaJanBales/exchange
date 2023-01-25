from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field('postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/fastapi_traefik', env='DATABASE_URL')


settings = Settings()
