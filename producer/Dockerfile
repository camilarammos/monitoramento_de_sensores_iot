FROM python:3.9-slim

WORKDIR /app

COPY producer/iot_producer.py .
COPY requirements.txt .
COPY tests/*.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "iot_producer.py"]
