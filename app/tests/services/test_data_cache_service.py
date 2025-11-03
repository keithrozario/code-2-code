import pytest
import json
from unittest.mock import mock_open, patch
from pathlib import Path

from app.moneynote.services.data_cache_service import DataCacheService
from app.moneynote.schemas.currency import Currency
from app.moneynote.schemas.book_template import BookTemplate, AccountTemplate
from pydantic import ValidationError

# Sample data for mocking
SAMPLE_CURRENCIES = [
    {"code": "USD", "name": "United States Dollar", "symbol": "$"},
    {"code": "EUR", "name": "Euro", "symbol": "€"}
]

SAMPLE_BOOK_TEMPLATES = [
    {
        "id": "personal_finance",
        "name": "Personal Finance",
        "description": "A template for managing personal finances.",
        "accounts": [
            {"name": "Checking Account", "type": "ASSET", "description": "Everyday spending account"}
        ]
    }
]

@pytest.fixture
def mock_data_files(monkeypatch):
    def mock_read_data(file_path):
        if "currency.json" in str(file_path):
            return json.dumps(SAMPLE_CURRENCIES)
        elif "book_tpl.json" in str(file_path):
            return json.dumps(SAMPLE_BOOK_TEMPLATES)
        raise FileNotFoundError

    monkeypatch.setattr(Path, "read_text", mock_read_data)

@patch('builtins.open', new_callable=mock_open)
@patch('json.load', side_effect=[SAMPLE_CURRENCIES, SAMPLE_BOOK_TEMPLATES])
def test_data_cache_service_loads_data_successfully(mock_json_load, mock_builtin_open):
    service = DataCacheService()
    assert len(service.get_currencies()) == len(SAMPLE_CURRENCIES)
    assert service.get_currencies()[0].code == SAMPLE_CURRENCIES[0]["code"]
    assert len(service.get_book_templates()) == len(SAMPLE_BOOK_TEMPLATES)
    assert service.get_book_templates()[0].id == SAMPLE_BOOK_TEMPLATES[0]["id"]

@patch('builtins.open', side_effect=FileNotFoundError)
def test_data_cache_service_file_not_found(mock_builtin_open):
    with pytest.raises(RuntimeError, match="Failed to load currency data"):
        DataCacheService()

@patch('builtins.open', new_callable=mock_open)
@patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
def test_data_cache_service_malformed_json(mock_json_load, mock_builtin_open):
    with pytest.raises(RuntimeError, match="Failed to parse currency data"):
        DataCacheService()

@patch('builtins.open', new_callable=mock_open)
@patch('json.load', side_effect=[[{"code": "USD"}], SAMPLE_BOOK_TEMPLATES]) # Missing name and symbol
def test_data_cache_service_pydantic_validation_error(mock_json_load, mock_builtin_open):
    with pytest.raises(RuntimeError, match="Failed to validate currency data"):
        DataCacheService()
