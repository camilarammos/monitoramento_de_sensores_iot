import os
import logging
import socket
import time
from pyspark.sql import DataFrame

MYSQL_URL = os.getenv("MYSQL_URL", "jdbc:mysql://mysql:3306/sensores")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "leituras")


def wait_for_mysql(host="mysql", port=3306, timeout=30):
    logging.info(f"Esperando MySQL em {host}:{port}...")
    for i in range(timeout):
        try:
            with socket.create_connection((host, port), timeout=2):
                logging.info("MySQL disponível!")
                return
        except OSError:
            time.sleep(1)
    raise Exception("MySQL não respondeu após vários segundos.")


def write_to_mysql(batch_df: DataFrame, epoch_id: int):
    try:
        wait_for_mysql()

        if batch_df.rdd.isEmpty():
            logging.info(f"Batch {epoch_id} vazio. Ignorando escrita.")
            return

        logging.info(f"Processando batch {epoch_id} com {batch_df.count()} registros.")
        batch_df.write.format("jdbc") \
            .option("url", MYSQL_URL) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", MYSQL_TABLE) \
            .option("user", MYSQL_USER) \
            .option("password", MYSQL_PASSWORD) \
            .option("batchsize", 1000) \
            .mode("append") \
            .save()

        logging.info(f"Batch {epoch_id} salvo no MySQL com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar batch {epoch_id}: {e}")
