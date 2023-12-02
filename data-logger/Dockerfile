FROM python:3-alpine

RUN pip3 install RPi.bme280 influxdb-client

COPY data-logger.py .

CMD python -u data-logger.py
