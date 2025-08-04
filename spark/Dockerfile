FROM python:3

RUN apt-get update && \
  apt-get install -y openjdk-17-jre-headless

WORKDIR /usr/src/app

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

COPY spark/iot_consumer_spark_mysql.py .
COPY spark/mysql_writer.py .
COPY jars/mysql-connector-j-8.3.0.jar /opt/spark/jars/mysql-connector-j-8.3.0.jar
COPY requirements.txt .
COPY tests/*.py .
RUN pip install --no-cache-dir -r requirements.txt
