from pyspark.sql import SparkSession, DataFrame

class KafkaStreamReader:
    def __init__(self, spark: SparkSession, topic: str, bootstrap_servers: str):
        self.spark = spark
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers

    def read(self) -> DataFrame:
        return self.spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_servers) \
            .option("subscribe", self.topic) \
            .load()
