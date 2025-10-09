import json
from pathlib import Path

CURRENCIES: list = []
BOOK_TEMPLATES: list = []

def _load_json_from_data_dir(filename: str) -> list:
    data_dir = Path(__file__).parent.parent / "data"
    file_path = data_dir / filename

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Failed to load {filename}: File not found at {file_path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse {filename}: {e}")

def load_currencies():
    global CURRENCIES
    CURRENCIES = _load_json_from_data_dir("currency.json")

def load_book_templates():
    global BOOK_TEMPLATES
    BOOK_TEMPLATES = _load_json_from_data_dir("book_tpl.json")