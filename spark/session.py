from pyspark.sql import SparkSession

class SparkSessionBuilder:
    @staticmethod
    def create(app_name: str, jar_path: str) -> SparkSession:
        return SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars", jar_path) \
            .config("spark.sql.shuffle.partitions", "2") \
            .getOrCreate()

