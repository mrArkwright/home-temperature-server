# Simple setup for a temperature logging RaspberryPi

Logs data in an [InfluxDB](https://www.influxdata.com) with a [Grafana](https://grafana.com) frontend.

## Setup

### Hardware Setup

Connect DHT22-Sensor to Pin D4 of your RaspberryPi.

### Create Volumes

```
docker volume create influxdb
docker volume create grafana
```

### Setup InfluxDB

Choose username, password, organization name (e.g. _default_) and bucket name (e.g. _home_). Then start influxdb service and execute setup:
```
docker compose up -d influxdb
docker compose exec influxdb influx setup -f --username <username> --password <password> --org <organiation> --bucket <bucket> --retention 0
```

Retrieve generated API token:
```
docker compose exec influxdb influx auth list --user <username>
```

Create a file named _.env_ with the following content:
```
INFLUXDB_ORG=<organization>
INFLUXDB_TOKEN=<api token>
INFLUXDB_BUCKET=<bucket>
```

### Start remaining services:

```
docker compose up -d
```

### Setup Grafana

Log in to Grafana with standard username _admin_ and password _admin_.

Create new InfluxDB data source with query language _Flux_ and URL _http://influxdb:8086_. Set the values for organization and token.

Create Grafana dashboards at your own pleasure.<br/>
Example query:
```
from(bucket: "<bucket>")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) => r._field == "temperature")
```

Example query with smoothing and extreme value filtering:
```
maxDuration = (a, b) => {
  aInt = int(v: a)
  bInt = int(v: b)
  return duration(v: if (aInt > bInt) then aInt else bInt)
}

interval = maxDuration(a: $__interval, b: 5s)

from(bucket: "<bucket>")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) => r._field == "temperature")
  |> filter(fn: (r) => r._value > 0.0 and r._value < 70.0)
  |> aggregateWindow(every: interval, fn: mean, createEmpty: true)
  |> timedMovingAverage(every: duration(v: int(v: interval) * 3), period: duration(v: int(v: interval) * 6))
```