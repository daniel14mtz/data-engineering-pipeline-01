from src.ingest import validate_data
import pytest

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