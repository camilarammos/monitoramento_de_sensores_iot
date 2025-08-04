# 📡 Monitoramento de Sensores IoT em Tempo Real

Projeto de Big Data que envia dados de sensores IoT em tempo real via Kafka, processando-os com PySpark Structured Streaming e armazenando-os em um banco MySQL. Arquitetura voltada à escalabilidade, resiliência e modularidade.

---

## 🧠 Objetivo

Enviar dados de sensores IoT, como temperatura, umidade, pressão, luminosidade para uma pipeline em tempo real, permitindo:

- Monitoramento contínuo dos dados
- Processamento e ingestão com tolerância a falhas
- Persistência confiável em banco de dados

---

## ⚙️ Tecnologias Utilizadas

- Python 3.9
- Kafka + Zookeeper
- Kafka UI
- Spark 3.5.0 (Structured Streaming)
- MySQL 8
- Faker
- Pytest
- Docker + Docker Compose

---

## 🏗️ Estrutura do Projeto

```
monitoramento_de_sensores_iot/
├── Dockerfile
├── README.md
├── docker-compose.yml
├── jars
│   └── mysql-connector-j-8.3.0.jar
├── producer
│   ├── Dockerfile
│   ├── __init__.py
│   └── iot_producer.py
├── requirements.txt
├── spark
│   ├── Dockerfile
│   ├── __init__.py
│   ├── __pycache__
│   │   └── mysql_writer.cpython-313.pyc
│   ├── iot_consumer_spark_mysql.py
│   └── mysql_writer.py
└── tests
    ├── __pycache__
    │   ├── conftest.cpython-39-pytest-8.4.1.pyc
    │   ├── test_consumer.cpython-39-pytest-8.4.1.pyc
    │   ├── test_mysql_writer.cpython-39-pytest-8.4.1.pyc
    │   └── test_producer.cpython-39-pytest-8.4.1.pyc
    ├── conftest.py
    ├── test_consumer.py
    ├── test_generate_sensor_data_structure.py
    └── test_mysql_writer.py
└── README.md
```

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/camilarammos/monitoramento_de_sensores_iot.git
cd monitoramento_de_sensores_iot
```

### 2. Caso necessite baixar o conector JDBC do MySQL

```bash
mkdir -p jars
wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar -P jars/
```

---

### 3. Suba os serviços com Docker Compose

```bash
docker-compose up --build -d
```

Serviços disponíveis:

| Serviço     | Porta | Descrição                            |
|-------------|-------|--------------------------------------|
| Kafka       | 9092  | Broker Kafka                         |
| Kafka UI    | 8081  | Interface web para visualização      |
| MySQL       | 3306  | Banco de dados para persistência     |
| Spark       | 4040+ | Leitura de dados via Structured Streaming |
| Producer    |       | Geração e envio dos dados ao Kafka   |
| Zookeeper   | 2121  | Gerenciamento dos brokers do Kafka   |							 |

---

## 🔄 Fluxo de Dados

```text
[Producer (Faker)] --> [Kafka Topic: iot-sensores] --> [Spark Structured Streaming] --> [MySQL (tabela: leituras)]
```

---

## 📜 Exemplo de Dado Gerado

```json
{
  "sensor_id": "8fbb1fd3-7b45-4b02-b8b4-cd2906c155e7",
  "timestamp": "2025-08-04T18:15:23",
  "latitude": -23.56,
  "longitude": -46.63,
  "tipo": "temperatura",
  "valor": 28.7,
  "unidade": "C"
}
```
---

## 📜 Acesso o banco de dados e consulta a tabela

```
sudo docker exec -it mysql_monitoramento mysql -uroot -proot sensores
```

```
select * from leituras limit 10;
```
---

## 🛡️ Logs e Resiliência

- Tentativas de reconexão ao Kafka
- Tratamento de exceções no `foreachBatch`
- Log estruturado com `logging`

---

## ✅ Testes Unitários

Testes disponíveis:

- Validação da estrutura dos dados gerados (`generate_sensor_data`)
- Teste de escrita no MySQL (mockado)
- Testes podem ser executados no contêiner do Spark:

```bash
docker exec -it spark bash
python -m pytest spark/test_mysql_writer.py -v
python -m pytest spark/test_consumer.py -v
```

```bash
docker exec -it producer bash
python -m pytest spark/test_generate_sensor_data_structure.py -v
```

---

## 🔐 Credenciais

| Sistema | Usuário | Senha     |
|---------|--------|-----------|
| MySQL   | root   | root      |
| Adminer | root   | root      |

---

## 🧑‍💻 Autor

Desenvolvido por **Camila Ramos de Oliveira** (https://github.com/camilarammos)

