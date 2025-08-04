import pytest
from iot_producer import generate_sensor_data


def test_generate_sensor_data_structure():
    data = generate_sensor_data()

    # Verifica se todos os campos existem
    expected_keys = {
        "sensor_id", "timestamp", "latitude", "longitude",
        "tipo", "valor", "unidade"
    }
    assert set(data.keys()) == expected_keys

    # Tipos dos campos
    assert isinstance(data["sensor_id"], str)
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
    assert isinstance(data["tipo"], str)
    assert isinstance(data["valor"], float)
    assert isinstance(data["unidade"], str)

    # Valores plausíveis
    assert -90 <= data["latitude"] <= 90
    assert -180 <= data["longitude"] <= 180
    assert 0 <= data["valor"] <= 100
    assert data["tipo"] in ["temperatura", "umidade", "pressao", "luminosidade"]

