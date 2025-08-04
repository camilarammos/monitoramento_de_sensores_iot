import time
import json
import random
import logging
from faker import Faker
from kafka import KafkaProducer

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

fake = Faker()

for attempt in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        break
    except Exception as e:
        print(f"Tentativa {attempt+1}: Kafka indisponível. Aguardando...")
        time.sleep(5)

SENSOR_TYPES = ["temperatura", "umidade", "pressao", "luminosidade"]

def generate_sensor_data():
    return {
        "sensor_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "tipo": random.choice(SENSOR_TYPES),
        "valor": round(random.uniform(10.0, 100.0), 2),
        "unidade": "C" if "temp" in SENSOR_TYPES else "%"
    }

while True:
    try:
        data = generate_sensor_data()
        producer.send("iot-sensores", value=data)
        logging.info(f"Enviado dado: {data}")
        time.sleep(1)
    except Exception as e:
        logging.error(f"Erro ao enviar dado: {e}")
