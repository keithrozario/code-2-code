from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    APP_VERSION: str = '1.0.0'
    BASE_URL: str = 'http://localhost:8000'

    model_config = ConfigDict(env_file=".env")


settings = Settings()