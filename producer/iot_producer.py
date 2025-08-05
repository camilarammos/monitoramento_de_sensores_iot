import os
import time
import json
import random
import logging
import socket
from typing import Dict
from faker import Faker
from kafka import KafkaProducer

# =========================
# Configuração de Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

# =========================
# Variáveis de Ambiente
# =========================
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "iot-sensores")
SEND_INTERVAL = float(os.getenv("SEND_INTERVAL", 1.0))


class KafkaConnectionManager:
    def __init__(self, host: str, port: int, retries: int = 10, timeout: int = 30):
        self.host = host
        self.port = port
        self.retries = retries
        self.timeout = timeout

    def wait_for_kafka(self):
        logging.info(f"Esperando Kafka em {self.host}:{self.port}...")
        for i in range(self.timeout):
            try:
                with socket.create_connection((self.host, self.port), timeout=2):
                    logging.info("Kafka disponível!")
                    return
            except OSError:
                time.sleep(1)
        raise Exception("Kafka não respondeu após vários segundos.")

    def connect(self) -> KafkaProducer:
        self.wait_for_kafka()
        for attempt in range(self.retries):
            try:
                producer = KafkaProducer(
                    bootstrap_servers=f"{self.host}:{self.port}",
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
                logging.info("Conectado ao Kafka com sucesso.")
                return producer
            except Exception as e:
                logging.warning(f"Tentativa {attempt + 1}: Kafka indisponível. Aguardando 5s...")
                time.sleep(5)

        raise ConnectionError("Não foi possível conectar ao Kafka após várias tentativas.")


class SensorDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.sensor_types = ["temperatura", "umidade", "pressao", "luminosidade"]

    def generate(self) -> Dict:
        tipo = random.choice(self.sensor_types)
        unidade = "C" if tipo == "temperatura" else "%"
        return {
            "sensor_id": self.fake.uuid4(),
            "timestamp": self.fake.iso8601(),
            "latitude": float(self.fake.latitude()),
            "longitude": float(self.fake.longitude()),
            "tipo": tipo,
            "valor": round(random.uniform(10.0, 100.0), 2),
            "unidade": unidade
        }


class KafkaProducerService:
    def __init__(self, producer: KafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    def send(self, data: Dict):
        self.producer.send(self.topic, value=data)
        logging.info(f"Dado enviado: {data}")


# =========================
# Execução principal (main)
# =========================
def main():
    logging.info("Iniciando envio de dados IoT para o Kafka...")

    kafka_manager = KafkaConnectionManager(host="kafka", port=9092)
    producer = kafka_manager.connect()

    data_generator = SensorDataGenerator()
    kafka_service = KafkaProducerService(producer, KAFKA_TOPIC)

    while True:
        try:
            data = data_generator.generate()
            kafka_service.send(data)
            time.sleep(SEND_INTERVAL)
        except Exception as e:
            logging.error(f"Erro ao enviar dado para o Kafka: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()

