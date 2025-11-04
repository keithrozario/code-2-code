from typing import List
from pathlib import Path
import json
import logging

from pydantic import ValidationError, TypeAdapter
from app.moneynote.schemas.currency import Currency
from app.moneynote.schemas.book_template import BookTemplate

logger = logging.getLogger(__name__)


class DataCacheService:
    _currencies: List[Currency]
    _book_templates: List[BookTemplate]

    def __init__(self):
        self._currencies = []
        self._book_templates = []
        data_dir = Path(__file__).parent.parent / "data"
        currency_file_path = data_dir / "currency.json"

        try:
            with open(currency_file_path, "r", encoding="utf-8") as f:
                currencies_data = json.load(f)
            self._currencies = TypeAdapter(List[Currency]).validate_python(
                currencies_data
            )

        except FileNotFoundError:
            logger.critical(f"Currency data file not found: {currency_file_path}")
            raise RuntimeError(f"Failed to load currency data: {currency_file_path}")

        except json.JSONDecodeError:
            logger.critical(
                f"Currency data file is malformed JSON: {currency_file_path}"
            )
            raise RuntimeError(f"Failed to parse currency data: {currency_file_path}")

        except ValidationError as e:
            logger.critical(
                f"Currency data failed Pydantic validation: {currency_file_path}\n{e}"
            )
            raise RuntimeError(
                f"Failed to validate currency data: {currency_file_path}"
            )

        book_tpl_file_path = data_dir / "book_tpl.json"
        try:
            with open(book_tpl_file_path, "r", encoding="utf-8") as f:
                book_templates_data = json.load(f)
            self._book_templates = TypeAdapter(List[BookTemplate]).validate_python(
                book_templates_data
            )
        except FileNotFoundError:
            logger.critical(f"Book template data file not found: {book_tpl_file_path}")
            raise RuntimeError(
                f"Failed to load book template data: {book_tpl_file_path}"
            )
        except json.JSONDecodeError:
            logger.critical(
                f"Book template data file is malformed JSON: {book_tpl_file_path}"
            )
            raise RuntimeError(
                f"Failed to parse book template data: {book_tpl_file_path}"
            )
        except ValidationError as e:
            logger.critical(
                f"Book template data failed Pydantic validation: {book_tpl_file_path}\n{e}"
            )
            raise RuntimeError(
                f"Failed to validate book template data: {book_tpl_file_path}"
            )

    def get_currencies(self) -> List[Currency]:
        return self._currencies.copy()

    def get_book_templates(self) -> List[BookTemplate]:
        return self._book_templates.copy()

    def get_book_template_by_id(self, template_id: str) -> BookTemplate | None:
        for template in self._book_templates:
            if template.id == template_id:
                return template
        return None


data_cache_service = DataCacheService()


def get_data_cache_service() -> DataCacheService:
    return data_cache_service
