FROM python:3-alpine

RUN apk add --no-cache gcc libc-dev &&\
    pip3 install RPi.GPIO adafruit-circuitpython-dht influxdb-client

COPY data-logger.py .

CMD python data-logger.py
