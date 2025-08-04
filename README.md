# Monitoramento de Sensores IoT

Sistema de simulação e monitoramento em tempo real de sensores IoT com Kafka, Spark e MySQL.

## Como executar

1. Suba os serviços:
```bash
docker-compose up -d
```

2. Instale dependências:
```bash
pip install -r requirements.txt
```

3. Execute o producer:
```bash
python producer/iot_producer.py
```

4. Execute o consumer Spark:
```bash
spark-submit consumer/iot_consumer_spark_mysql.py
```

