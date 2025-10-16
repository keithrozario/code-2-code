import json
from unittest.mock import mock_open, patch

import pytest
from moneynote.services import data_loader


def test_load_currencies_success():
    mock_json_data = '[{"code": "USD", "name": "United States Dollar"}]'
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch.object(json, 'load', return_value=[{"code": "USD", "name": "United States Dollar"}]):
            data_loader.load_currencies()
            assert data_loader.CURRENCIES == [{"code": "USD", "name": "United States Dollar"}]

def test_load_currencies_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(RuntimeError, match="Failed to load currency.json: File not found"):
            data_loader.load_currencies()

def test_load_currencies_json_decode_error():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch.object(json, 'load', side_effect=json.JSONDecodeError("msg", "doc", 0)):
            with pytest.raises(RuntimeError, match="Failed to parse currency.json"):
                data_loader.load_currencies()

def test_load_book_templates_success():
    mock_json_data = '[{"id": "1", "name": "Template 1"}]'
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch.object(json, 'load', return_value=[{"id": "1", "name": "Template 1"}]):
            data_loader.load_book_templates()
            assert data_loader.BOOK_TEMPLATES == [{"id": "1", "name": "Template 1"}]

def test_load_book_templates_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(RuntimeError, match="Failed to load book_tpl.json: File not found"):
            data_loader.load_book_templates()

def test_load_book_templates_json_decode_error():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch.object(json, 'load', side_effect=json.JSONDecodeError("msg", "doc", 0)):
            with pytest.raises(RuntimeError, match="Failed to parse book_tpl.json"):
                data_loader.load_book_templates()