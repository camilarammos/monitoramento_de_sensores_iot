import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *
from mysql_writer import write_to_mysql

# =========================
# Configuração de Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

# =========================
# Configurações via Ambiente
# =========================
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "iot-sensores")
CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", "/tmp/spark-checkpoint")
JDBC_JAR_PATH = os.getenv("MYSQL_JAR_PATH", "/opt/spark/jars/mysql-connector-j-8.3.0.jar")

# ==========================
# Inicializa SparkSession
# ==========================
spark = SparkSession.builder \
    .appName("IoTConsumerMySQL") \
    .config("spark.jars", JDBC_JAR_PATH) \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

logging.info("Sessão Spark iniciada.")

# ===================
# Define o Esquema
# ===================
schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("latitude", DoubleType()),
    StructField("longitude", DoubleType()),
    StructField("tipo", StringType()),
    StructField("valor", DoubleType()),
    StructField("unidade", StringType())
])

# ============================
# Leitura do Kafka Streaming
# ============================
logging.info("Conectando ao Kafka...")

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# ============================
# Conversão do JSON (Kafka)
# ============================
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# =====================
# Inicia o Streaming
# =====================
logging.info("Iniciando streaming de leitura...")

if __name__ == "__main__":
    query = json_df.writeStream \
        .outputMode("append") \
        .trigger(processingTime="10 seconds") \
        .option("checkpointLocation", CHECKPOINT_PATH) \
        .foreachBatch(write_to_mysql) \
        .start()

    query.awaitTermination()

