import json
from typing import List, Type

from moneynote.schemas import BookTemplate, Currency
from pydantic import BaseModel, TypeAdapter, ValidationError


class DataFileError(Exception):
    pass


class DataLoaderService:
    def __init__(self):
        self.currencies: list[Currency] = []
        self.book_templates: list[BookTemplate] = []

    def _load_and_validate_json(
        self, file_path: str, model: Type[BaseModel]
    ) -> List[BaseModel]:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            adapter = TypeAdapter(List[model])
            return adapter.validate_python(data)
        except FileNotFoundError as e:
            raise DataFileError(f"Data file not found: {file_path}") from e
        except json.JSONDecodeError as e:
            raise DataFileError(f"Invalid JSON in data file: {file_path}") from e
        except ValidationError as e:
            raise DataFileError(f"Data validation error in file: {file_path}") from e

    def load_currencies(self, settings: "Settings"):
        self.currencies = self._load_and_validate_json(
            settings.CURRENCY_DATA_PATH, Currency
        )

    def load_book_templates(self, settings: "Settings"):
        self.book_templates = self._load_and_validate_json(
            settings.BOOK_TPL_DATA_PATH, BookTemplate
        )

    def load_all_data(self, settings: "Settings"):
        try:
            self.load_currencies(settings)
            self.load_book_templates(settings)
        except DataFileError as e:
            import logging

            logging.critical("Failed to load static data: %s", e)
            raise
