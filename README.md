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
├── README.md
├── dist
│   └── common-0.1-py3-none-any.whl
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
│   ├── consumer_main.py
│   ├── json_parser.py
│   ├── kafka_reader.py
│   ├── mysql_writer.py
│   ├── pipeline.py
│   └── session.py
└── tests
    ├── conftest.py
    ├── test_consumer.py
    ├── test_generate_sensor_data_structure.py
    └── test_mysql_writer.py
```
---

## ⚙️ Variáveis de Ambiente

| Variável                | Descrição                            | Valor padrão      |
|-------------------------|----------------------------------------|-------------------|
| KAFKA_BOOTSTRAP_SERVERS | Endereço do broker Kafka              | kafka:9092        |
| KAFKA_TOPIC             | Nome do tópico Kafka                  | iot-sensores      |
| SEND_INTERVAL           | Intervalo entre envios do Producer    | 1.0 (segundos)    |
| MYSQL_URL               | URL JDBC para conexão com MySQL       | jdbc:mysql://...  |
| MYSQL_USER              | Usuário do banco                      | root              |
| MYSQL_PASSWORD          | Senha do banco                        | root              |
| MYSQL_TABLE             | Tabela onde os dados serão gravados   | leituras          |
| CHECKPOINT_PATH         | Caminho de checkpoint do Spark        | /tmp/spark-checkpoint |

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

Os testes abaixo devem ser executados no contêiner do Spark:

```bash
docker exec -it spark bash
python -m pytest spark/test_mysql_writer.py -v
python -m pytest spark/test_consumer.py -v
```

Os testes abaixo devem ser executados no contêiner do Producer:
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

