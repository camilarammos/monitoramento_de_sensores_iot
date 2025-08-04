import pytest
from pyspark.sql import Row

def test_parse_schema_from_json(spark):
    sample = [Row(sensor_id="123", timestamp="2024-01-01T12:00:00",
                  latitude=1.23, longitude=4.56, tipo="temperatura", valor=23.4, unidade="C")]
    df = spark.createDataFrame(sample)
    assert df.count() == 1
    assert df.columns == ["sensor_id", "timestamp", "latitude", "longitude", "tipo", "valor", "unidade"]
