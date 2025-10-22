from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "0.1.0"
    BASE_URL: str = "http://localhost:8000"
    CURRENCY_DATA_PATH: str = "new_app/moneynote/data/currency.json"
    BOOK_TPL_DATA_PATH: str = "new_app/moneynote/data/book_tpl.json"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
