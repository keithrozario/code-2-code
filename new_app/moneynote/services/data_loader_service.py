import json
import logging
from typing import Type

from config import Settings
from moneynote.schemas import BookTemplate, Currency
from pydantic import BaseModel, ValidationError


class DataFileError(Exception):
    pass


class DataLoaderService:
    def __init__(self):
        self.currencies: list[Currency] = []
        self.book_templates: list[BookTemplate] = []

    def _load_and_validate_json(
        self, file_path: str, model: Type[BaseModel]
    ) -> list[BaseModel]:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return [model.model_validate(item) for item in data]
        except FileNotFoundError:
            raise DataFileError(f"Data file not found: {file_path}")
        except json.JSONDecodeError:
            raise DataFileError(f"Failed to decode JSON from {file_path}")
        except ValidationError as e:
            raise DataFileError(f"Data validation error in {file_path}: {e}")

    def load_currencies(self, settings: Settings):
        self.currencies = self._load_and_validate_json(
            settings.CURRENCY_DATA_PATH, Currency
        )

    def load_book_templates(self, settings: Settings):
        self.book_templates = self._load_and_validate_json(
            settings.BOOK_TPL_DATA_PATH, BookTemplate
        )

    def load_all_data(self, settings: Settings):
        try:
            self.load_currencies(settings)
            self.load_book_templates(settings)
        except DataFileError as e:
            logging.critical("Failed to load static data: %s", e)
            raise
