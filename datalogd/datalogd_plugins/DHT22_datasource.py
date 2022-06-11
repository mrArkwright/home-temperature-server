import asyncio
import time
import board
import adafruit_dht
from datalogd import DataSource

dhtDevice = adafruit_dht.DHT22(board.D4)

class DHT22DataSource(DataSource):
    def __init__(self, sinks=[]):
        super().__init__(sinks=sinks)
        asyncio.get_event_loop().call_soon(self.get_temperature)

    def get_temperature(self):
        while True:
            try:
                temperature = dhtDevice.temperature
                humidity = dhtDevice.humidity
                self.send([{"type": "temperature", "id": "room", "value": temperature}, {"type": "humidity", "id": "room", "value": humidity}])
                break
            except RuntimeError as error:
                time.sleep(0.1)
                continue

        asyncio.get_event_loop().call_later(5, self.get_temperature)
