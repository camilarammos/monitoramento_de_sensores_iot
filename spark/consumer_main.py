import os
import logging
from session import SparkSessionBuilder
from kafka_reader import KafkaStreamReader
from json_parser import JsonParser
from pipeline import StreamingPipeline

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "iot-sensores")
CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", "/tmp/spark-checkpoint")
JDBC_JAR_PATH = os.getenv("MYSQL_JAR_PATH", "/opt/spark/jars/mysql-connector-j-8.3.0.jar")

def main():
    logging.info("Iniciando sessão Spark...")
    spark = SparkSessionBuilder.create("IoTConsumerMySQL", JDBC_JAR_PATH)

    logging.info("Conectando ao Kafka...")
    kafka_reader = KafkaStreamReader(spark, KAFKA_TOPIC, KAFKA_BOOTSTRAP)
    kafka_df = kafka_reader.read()

    parser = JsonParser()
    parsed_df = parser.parse(kafka_df)

    logging.info("Iniciando streaming...")
    pipeline = StreamingPipeline(parsed_df, CHECKPOINT_PATH)
    pipeline.start()

if __name__ == "__main__":
    main()
