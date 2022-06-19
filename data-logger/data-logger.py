import os
import time
from datetime import datetime
import logging
import board
import adafruit_dht
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    loglevel = os.environ.get("LOGLEVEL", "INFO")
    set_loglevel(loglevel)

    dht_pin = board.D4
    dht_device = adafruit_dht.DHT22(dht_pin)

    influxdb_host = os.environ["INFLUXDB_HOST"]
    influxdb_port = os.environ["INFLUXDB_PORT"]
    influxdb_org = os.environ["INFLUXDB_ORG"]
    influxdb_token = os.environ["INFLUXDB_TOKEN"]
    influxdb_bucket = os.environ["INFLUXDB_BUCKET"]

    influx_db_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
    influx_db_write_api = influx_db_client.write_api(write_options=SYNCHRONOUS)

    logging.info("data-logger started")

    data_log_loop(dht_device, influx_db_write_api, influxdb_bucket, influxdb_org)


def set_loglevel(loglevel):
    loglevel1 = getattr(logging, loglevel, None)

    if not isinstance(loglevel1, int):
        raise ValueError(f"Invalid log level: {loglevel}")

    logging.basicConfig(level=loglevel1)


def data_log_loop(dht_device, influx_db_write_api, influxdb_bucket, influxdb_org):
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
        except RuntimeError as error:
            logging.debug(f"error reading sensor: {error}")
            continue

        point = Point("default") \
            .field("temperature", temperature) \
            .field("humidity", humidity) \
            .time(datetime.utcnow(), WritePrecision.NS)

        influx_db_write_api.write(influxdb_bucket, influxdb_org, point)

        logging.debug(f"logged temperature: {temperature}, humidity {humidity}")

        time.sleep(5.0)


if __name__ == "__main__":
    main()
