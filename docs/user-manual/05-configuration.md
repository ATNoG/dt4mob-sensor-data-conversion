## Configuration

Configuration is managed through `config.toml`. Environment variables can override any setting using the `SENSOR_DATA_CONVERSION_` prefix with `__` as the nested delimiter (e.g., `SENSOR_DATA_CONVERSION_SENDER__URL=mqtt://broker:1883`).

**Priority:** Environment variables override `config.toml` values.

### Global Settings

| Field                | Type   | Default  | Description                                                                                             |
| -------------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------- |
| `log_level`          | string | `"INFO"` | Logging verbosity. Options: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`                             |
| `atb_realtime_topic` | string | `""`     | MQTT topic to publish converted real-time ORT Tracking messages to                                      |
| `atb_history_topic`  | string | `""`     | MQTT topic to publish converted history ORT Tracking messages to                                        |

### `[consumer]` -- Inbound Consumer

The consumer defines how the service ingests OutSight messages. Only one backend can be active at a time.

| Field     | Type   | Default      | Description                                                          |
| --------- | ------ | ------------ | -------------------------------------------------------------------- |
| `backend` | string | `"disabled"` | Consumer backend. Options: `"disabled"`, `"mqtt"`, `"webhook"`       |

#### MQTT Consumer (`[consumer].backend = "mqtt"`)

| Field    | Type | Default            | Description                          |
| -------- | ---- | ------------------ | ------------------------------------ |
| `url`    | URL  | `"mqtt://localhost"` | MQTT broker connection URL         |
| `topics` | list | `[]`               | MQTT topics to subscribe to          |

#### Webhook Consumer (`[consumer].backend = "webhook"`)

| Field       | Type   | Default       | Description                                  |
| ----------- | ------ | ------------- | -------------------------------------------- |
| `host`      | string | `"localhost"` | Webhook listen hostname                      |
| `port`      | int    | `8000`        | Webhook listen port                          |
| `base_path` | string | `"/"`         | HTTP path to receive POST requests on        |

### `[sender]` -- Outbound Sender

The sender defines where converted messages are published.

| Field | Type | Default            | Description                      |
| ----- | ---- | ------------------ | -------------------------------- |
| `url` | URL  | `"mqtt://localhost"` | MQTT broker connection URL     |

### `[converter]` -- Converter Settings

The converter defines the reference planes used for coordinate transformations between OutSight and ORT Tracking coordinate systems.

#### `[converter.outsight_reference_plane]` -- OutSight Reference Plane

Defines the geographic coordinate system of the incoming OutSight data.

| Field                            | Type            | Default     | Description                                                                 |
| -------------------------------- | --------------- | ----------- | --------------------------------------------------------------------------- |
| `origin`                         | [lat, lon]      | `[0.0, 0.0]` | Geographic coordinates `[latitude, longitude]` of the reference plane origin |
| `point_on_positive_horizontal_axis` | [lat, lon]   | `[0.0, 1.0]` | Geographic coordinates `[latitude, longitude]` defining the positive horizontal axis direction |

#### `[converter.atobe_reference_plane]` -- AToBe Reference Plane

Defines the target geographic coordinate system for the converted ORT Tracking output.

| Field                            | Type            | Default     | Description                                                                 |
| -------------------------------- | --------------- | ----------- | --------------------------------------------------------------------------- |
| `origin`                         | [lat, lon]      | `[0.0, 0.0]` | Geographic coordinates `[latitude, longitude]` of the reference plane origin |
| `point_on_positive_horizontal_axis` | [lat, lon]   | `[0.0, 1.0]` | Geographic coordinates `[latitude, longitude]` defining the positive horizontal axis direction |

### Environment Variable Overrides

All settings can be overridden via environment variables with the prefix `SENSOR_DATA_CONVERSION_` and `__` as the nested delimiter:

```bash
export SENSOR_DATA_CONVERSION_LOG_LEVEL="DEBUG"
export SENSOR_DATA_CONVERSION_SENDER__URL="mqtt://broker:1883"
export SENSOR_DATA_CONVERSION_CONSUMER__BACKEND="mqtt"
export SENSOR_DATA_CONVERSION_CONSUMER__URL="mqtt://sensor-broker:1883"
export SENSOR_DATA_CONVERSION_CONSUMER__TOPICS='["detections"]'
export SENSOR_DATA_CONVERSION_ATB_REALTIME_TOPIC="vehicle/realtime"
export SENSOR_DATA_CONVERSION_ATB_HISTORY_TOPIC="vehicle/history"
```

### Example Configuration

```toml
log_level = "INFO"

atb_realtime_topic = "vehicle/realtime"
atb_history_topic = "vehicle/history"

[consumer]
backend = "mqtt"
url = "mqtt://sensor-broker:1883"
topics = ["outsight/detections"]

[sender]
url = "mqtt://hono-broker:1883"

[converter.outsight_reference_plane]
origin = [38.711289, -9.309308]
point_on_positive_horizontal_axis = [38.711341, -9.309187]

[converter.atobe_reference_plane]
origin = [38.711308, -9.309153]
point_on_positive_horizontal_axis = [38.711164, -9.309436]
```
