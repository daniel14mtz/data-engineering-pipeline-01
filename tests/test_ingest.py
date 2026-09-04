from src.ingest import validate_data
import pytest
import requests

def test_validate_data_success():
    data = [
        {
            "id": 1,
            "name": "Juan",
            "email": "juan@example.com"
        }
    ]
    validate_data(data)

def test_validate_data_missing_email():
    data = [
        {
            "id": 1,
            "name": "Juan"
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)

def test_validate_data_duplicate_id():
    data = [
        {
            "id": 1,
            "name": "Juan",
            "email": "juan@example.com"
        },
        {
            "id": 1,
            "name": "Pedro",
            "email": "pedro@example.com"
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)

def test_transform_data():
    from src.ingest import transform_data

    data = [
        {
            "id": 1,
            "name": "  Juan  ",
            "email": "JUAN@EXAMPLE.COM",
            "company": "Empresa"
        }
    ]

    result = transform_data(data)

    assert result == [
        {
            "id": 1,
            "name": "Juan",
            "email": "juan@example.com"
        }
    ]

def test_validate_data_empty():
    data = []

    with pytest.raises(ValueError):
        validate_data(data)

def test_save_json(tmp_path):
    from src.ingest import save_json
    import json

    data = [
        {
            "id": 1,
            "name": "Juan",
            "email": "juan@example.com"
        }
    ]

    file_path = tmp_path / "users.json"

    save_json(data, file_path)

    assert file_path.exists()

    with open(file_path) as file:
        result = json.load(file)

    assert result == data

def test_extract_data_retry(monkeypatch):
    from src.ingest import extract_data

    attempts = []

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return [
                {
                    "id": 1,
                    "name": "Juan",
                    "email": "juan@example.com"
                }
            ]

    def mock_get(url, timeout):
        attempts.append(1)

        if len(attempts) < 3:
            raise requests.RequestException("Error temporal")

        return MockResponse()

    monkeypatch.setattr("src.ingest.requests.get", mock_get)

    monkeypatch.setattr("src.ingest.time.sleep", lambda seconds: None)

    data = extract_data()

    assert len(attempts) == 3
    assert data[0]["id"] == 1

def test_validate_data_invalid_id_type():
    data = [
        {
            "id": "ABC",
            "name": "Juan",
            "email": "juan@example.com"
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)

def test_validate_data_empty_name():
    data = [
        {
            "id": 1,
            "name": "",
            "email": "juan@example.com"
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)

def test_validate_data_invalid_email():
    data = [
        {
            "id": 1,
            "name": "Juan",
            "email": "juan@example"
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)

def test_validate_data_empty_email():
    data = [
        {
            "id": 1,
            "name": "Juan",
            "email": ""
        }
    ]

    with pytest.raises(ValueError):
        validate_data(data)