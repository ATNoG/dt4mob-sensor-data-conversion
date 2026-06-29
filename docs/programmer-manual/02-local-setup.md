## Local Setup

**Clone the repository**

```bash
git clone https://github.com/ATNoG/dt4mob-sensor-data-conversion.git
cd dt4mob-sensor-data-conversion
```

**Install uv (if not installed)**

Follow the instructions at <https://docs.astral.sh/uv/getting-started/installation/> in order to install `uv`.

**Install dependencies**

```bash
uv sync
```

This installs both runtime and dev dependencies (mypy, ruff) into a virtual environment.

**Configure the service**

```bash
cp config.example.toml config.toml
```

Edit `config.toml` with your local settings. At minimum, configure:

- `atb_realtime_topic` and `atb_history_topic` for output topics
- `[consumer]` backend with connection details
- `[sender]` URL pointing to your MQTT broker
- `[converter]` reference planes for your deployment coordinates

**Run**

```bash
uv run main.py
```

### Environment Variables

Settings can be overridden via environment variables using the `SENSOR_DATA_CONVERSION_` prefix with `__` as the nested delimiter:

```bash
export SENSOR_DATA_CONVERSION_LOG_LEVEL="DEBUG"
export SENSOR_DATA_CONVERSION_SENDER__URL="mqtt://broker:1883"
export SENSOR_DATA_CONVERSION_CONSUMER__BACKEND="mqtt"
export SENSOR_DATA_CONVERSION_CONSUMER__URL="mqtt://sensor-broker:1883"
export SENSOR_DATA_CONVERSION_ATB_REALTIME_TOPIC="vehicle/realtime"
```

The priority order is: environment variables -> `config.toml` values.
