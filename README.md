# Simple setup for a temperature logging RaspberryPi

Uses [datalogd](https://datalogd.readthedocs.io) to log data in an [InfluxDB](https://www.influxdata.com) with a [Grafana](https://grafana.com) frontend.

## Setup

Connect DHT22-Sensor to Pin D4 of your RaspberryPi.

Start services:

```
docker volume create influxdb-data
docker volume create grafana-data
docker compose up -d
```

In Grafana create new InfluxDB data source with URL `influxdb:8086`.

Create Grafana dashboards at your own pleasure. Example query:

```
SELECT moving_average(last("temperature_room"), 12) FROM "default" WHERE ("temperature_room" > 15) AND $timeFilter GROUP BY time($__interval) fill(null)
```