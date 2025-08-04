import logging

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

