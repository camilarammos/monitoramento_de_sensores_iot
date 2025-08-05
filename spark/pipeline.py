from pyspark.sql import DataFrame
from mysql_writer import write_to_mysql

class StreamingPipeline:
    def __init__(self, parsed_df: DataFrame, checkpoint_path: str):
        self.parsed_df = parsed_df
        self.checkpoint_path = checkpoint_path

    def start(self):
        query = self.parsed_df.writeStream \
            .outputMode("append") \
            .trigger(processingTime="10 seconds") \
            .option("checkpointLocation", self.checkpoint_path) \
            .foreachBatch(write_to_mysql) \
            .start()
        query.awaitTermination()
