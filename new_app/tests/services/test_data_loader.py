import json
from unittest.mock import MagicMock, mock_open, patch

import pytest
from moneynote.services.data_loader_service import DataLoaderService, DataFileError
from config import Settings

@pytest.fixture
def mock_settings():
    return Settings(
        CURRENCY_DATA_PATH="dummy/path/currencies.json",
        BOOK_TPL_DATA_PATH="dummy/path/book_templates.json"
    )

def test_load_currencies_success(mock_settings):
    service = DataLoaderService()
    mock_json_data = '[{"id": "USD", "name": "United States Dollar", "description": "...", "rate": 1.0}]'
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        service.load_currencies(mock_settings)
        assert len(service.currencies) == 1
        assert service.currencies[0].id == "USD"

def test_load_currencies_file_not_found(mock_settings):
    service = DataLoaderService()
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(DataFileError, match="Data file not found"):
            service.load_currencies(mock_settings)

def test_load_currencies_json_decode_error(mock_settings):
    service = DataLoaderService()
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch.object(json, 'load', side_effect=json.JSONDecodeError("msg", "doc", 0)):
            with pytest.raises(DataFileError, match="Failed to decode JSON"):
                service.load_currencies(mock_settings)

def test_load_book_templates_success(mock_settings):
    service = DataLoaderService()
    mock_json_data = '[{"id": "personal", "name": "Personal", "description": "...", "categories": [], "tags": [], "payees": []}]'
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        service.load_book_templates(mock_settings)
        assert len(service.book_templates) == 1
        assert service.book_templates[0].id == "personal"

def test_load_book_templates_file_not_found(mock_settings):
    service = DataLoaderService()
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(DataFileError, match="Data file not found"):
            service.load_book_templates(mock_settings)

def test_load_book_templates_json_decode_error(mock_settings):
    service = DataLoaderService()
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch.object(json, 'load', side_effect=json.JSONDecodeError("msg", "doc", 0)):
            with pytest.raises(DataFileError, match="Failed to decode JSON"):
                service.load_book_templates(mock_settings)

def test_load_all_data_success(mock_settings):
    service = DataLoaderService()
    with patch.object(service, 'load_currencies') as mock_load_currencies, \
         patch.object(service, 'load_book_templates') as mock_load_book_templates:
        service.load_all_data(mock_settings)
        mock_load_currencies.assert_called_once_with(mock_settings)
        mock_load_book_templates.assert_called_once_with(mock_settings)

@patch('logging.critical')
def test_load_all_data_error(mock_critical_log, mock_settings):
    service = DataLoaderService()
    with patch.object(service, 'load_currencies', side_effect=DataFileError("test error")):
        with pytest.raises(DataFileError):
            service.load_all_data(mock_settings)
        mock_critical_log.assert_called_once()
