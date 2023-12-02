import os
import time
from datetime import datetime
import logging
import smbus2
import bme280
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    loglevel = os.environ.get("LOGLEVEL", "INFO")
    set_loglevel(loglevel)

    bme280_smbus_port = 1
    bme280_smbus_address = 0x76

    bme280_smbus = smbus2.SMBus(bme280_smbus_port)

    bme280.load_calibration_params(bme280_smbus, bme280_smbus_address)

    influxdb_host = os.environ["INFLUXDB_HOST"]
    influxdb_port = os.environ["INFLUXDB_PORT"]
    influxdb_org = os.environ["INFLUXDB_ORG"]
    influxdb_token = os.environ["INFLUXDB_TOKEN"]
    influxdb_bucket = os.environ["INFLUXDB_BUCKET"]

    influx_db_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
    influx_db_write_api = influx_db_client.write_api(write_options=SYNCHRONOUS)

    logging.info("data-logger started")

    data_log_loop(bme280_smbus, bme280_smbus_address, influx_db_write_api, influxdb_bucket, influxdb_org)


def set_loglevel(loglevel):
    loglevel1 = getattr(logging, loglevel, None)

    if not isinstance(loglevel1, int):
        raise ValueError(f"Invalid log level: {loglevel}")

    logging.basicConfig(level=loglevel1)


def data_log_loop(bme280_smbus, bme280_smbus_address, influx_db_write_api, influxdb_bucket, influxdb_org):
    while True:
        try:
            bme280_data = bme280.sample(bme280_smbus, bme280_smbus_address)
            temperature = bme280_data.temperature
            humidity = bme280_data.humidity
            #pressure = bme280_data.pressure
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
