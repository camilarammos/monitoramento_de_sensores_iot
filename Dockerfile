FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/iot_consumer_spark_mysql.py /opt/app/iot_consumer_spark_mysql.py
