FROM python:3

RUN apt-get update && \
  apt-get install -y openjdk-17-jre-headless

WORKDIR /usr/src/app

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

#TO DO
RUN pip install --no-cache-dir pyspark[sql]==3.5
COPY mysql-connector-j-8.3.0.jar /opt/spark/jars/mysql-connector-j-8.3.0.jar

COPY iot_consumer_spark_mysql.py /opt/app/iot_consumer_spark_mysql.py
