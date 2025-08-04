FROM python:3.9-slim
WORKDIR /app
COPY iot_producer.py .
RUN pip install faker kafka-python
CMD ["python", "iot_producer.py"]
