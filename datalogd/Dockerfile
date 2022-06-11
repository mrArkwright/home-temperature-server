FROM python:3-alpine

RUN apk add --no-cache gcc libc-dev &&\
    pip3 install RPi.GPIO adafruit-circuitpython-dht pyserial pyserial-asyncio influxdb pyvisa pyvisa-py pyusb ThorlabsPM100 datalogd

COPY config/datalogd.conf /root/.config/datalogd/
COPY datalogd_plugins /root/datalogd_plugins

CMD ["datalogd"]
