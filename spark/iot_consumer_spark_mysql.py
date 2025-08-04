from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *
import logging

# Configuração do logger do Spark (stdout dos containers)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

spark = SparkSession.builder.appName("IoTConsumerMySQL") \
        .config("spark.jars", "/opt/spark/jars/mysql-connector-j-8.3.0.jar") \
        .getOrCreate()

schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("latitude", DoubleType()),
    StructField("longitude", DoubleType()),
    StructField("tipo", StringType()),
    StructField("valor", DoubleType()),
    StructField("unidade", StringType())
])

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "iot-sensores") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

def write_to_mysql(batch_df, epoch_id):
    try:
        logging.info(f"Processando batch {epoch_id} com {batch_df.count()} registros.")
        batch_df.write.format("jdbc") \
            .option("url", "jdbc:mysql://mysql:3306/sensores") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", "leituras") \
            .option("user", "root") \
            .option("password", "root") \
            .mode("append") \
            .save()
        logging.info(f"Batch {epoch_id} salvo no MySQL com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar batch {epoch_id}: {e}")

query = json_df.writeStream.foreachBatch(write_to_mysql).start()
query.awaitTermination()
