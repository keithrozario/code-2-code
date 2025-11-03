from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "0.1.0"
    BASE_URL: str = "http://localhost:8000"


settings = Settings()