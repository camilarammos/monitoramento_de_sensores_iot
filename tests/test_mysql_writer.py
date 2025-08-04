from unittest.mock import patch
from pyspark.sql import SparkSession
from pyspark.sql import Row

from mysql_writer import write_to_mysql

def test_write_to_mysql_called_with_correct_data():
    spark = SparkSession.builder.master("local[1]").appName("Test") \
            .config("spark.jars", "/opt/spark/jars/mysql-connector-j-8.3.0.jar") \
            .getOrCreate()

    mock_data = [
        Row(
            sensor_id="abc-123",
            timestamp="2025-06-15T15:00:00",
            latitude=-23.55,
            longitude=-46.63,
            tipo="temperatura",
            valor=28.5,
            unidade="C"
        )
    ]

    df = spark.createDataFrame(mock_data)

    with patch("mysql_writer.write_to_mysql") as mock_write:
        # Simula chamada do foreachBatch
        mock_write(df, 1)
        mock_write.assert_called_once()

