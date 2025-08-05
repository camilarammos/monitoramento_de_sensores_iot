from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

class JsonParser:
    def __init__(self):
        self.schema = StructType([
            StructField("sensor_id", StringType()),
            StructField("timestamp", StringType()),
            StructField("latitude", DoubleType()),
            StructField("longitude", DoubleType()),
            StructField("tipo", StringType()),
            StructField("valor", DoubleType()),
            StructField("unidade", StringType())
        ])

    def parse(self, df: DataFrame) -> DataFrame:
        return df.selectExpr("CAST(value AS STRING)") \
                 .select(from_json(col("value"), self.schema).alias("data")) \
                 .select("data.*")
