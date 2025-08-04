import time
import json
import random
import logging
from faker import Faker
from kafka import KafkaProducer

# ======================
# Configuração de Logging
# ======================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

fake = Faker()
SENSOR_TYPES = ["temperatura", "umidade", "pressao", "luminosidade"]

# ====================================
# Tentativas de conexão com o Kafka
# ====================================
producer = None
for attempt in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logging.info("Conectado ao Kafka com sucesso.")
        break
    except Exception as e:
        logging.warning(f"Tentativa {attempt + 1}: Kafka indisponível. Aguardando 5s...")
        time.sleep(5)

if not producer:
    logging.error("Não foi possível conectar ao Kafka após várias tentativas.")
    exit(1)

# ===========================
# Função para gerar os dados
# ===========================
def generate_sensor_data():
    tipo = random.choice(SENSOR_TYPES)
    unidade = "C" if tipo == "temperatura" else "%"
    return {
        "sensor_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "tipo": tipo,
        "valor": round(random.uniform(10.0, 100.0), 2),
        "unidade": unidade
    }

# ===============================
# Loop contínuo para enviar dados
# ===============================
while True:
    try:
        data = generate_sensor_data()
        producer.send("iot-sensores", value=data)
        logging.info(f"Dado enviado: {data}")
        time.sleep(1)
    except Exception as e:
        logging.error(f"Erro ao enviar dado para o Kafka: {e}")
        time.sleep(2)

