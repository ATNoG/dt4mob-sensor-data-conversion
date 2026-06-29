## Key Implementation Details

### Consumer Drivers

- **MQTT Consumer** (`app/drivers/consumer/mqtt/consumer.py`): Uses `amqtt.client.MQTTClient` with `ClientConfig` and `ConnectionConfig`. Subscribes to all configured topics at QOS 0. Exposes an async iterator that yields raw message bytes.

- **Webhook Consumer** (`app/drivers/consumer/webhook/consumer.py`): Creates a `FastAPI` app with a catch-all POST endpoint at the configured `base_path`. Runs via `uvicorn.Server` as an asyncio task. Incoming request bodies are placed into an `asyncio.Queue[bytes]`.

- **Factory** (`app/drivers/consumer/__init__.py`): Uses a `match` statement on `settings.consumer.backend` to conditionally import and instantiate the correct driver. Raises `RuntimeError` if no valid backend is configured.

### Converter (`app/lib/convert.py`)

The `OutSightToAToBe` class performs all coordinate transformations and message conversion.

**Initialization** (runs once at startup):

1. Converts the OutSight reference plane origin and horizontal axis point from geodetic to ENU coordinates relative to the AToBe reference plane origin using `pymap3d.geodetic2enu`
2. Computes the OutSight-to-ENU transformation matrix from the OutSight horizontal and vertical unit vectors
3. Computes the ENU-to-AToBe transformation matrix from the AToBe horizontal and vertical unit vectors

**Per-message conversion**:

- `calculate_coords(data: Alert)` -- Transforms OutSight bounding box corner `[3]` (the reference point) through the OutSight-to-ENU matrix, then computes absolute coordinates via `pymap3d.enu2geodetic`, then transforms through the ENU-to-AToBe matrix for local coordinates. Note: x and y are intentionally flipped in the final output due to the ORT Tracking specification.

- `calculate_dimensions(data: Alert)` -- Computes length and width by averaging distances between opposite pairs of the four bounding box corners using `numpy.linalg.norm`. Height is taken directly from the OutSight message.

- `convert_outsight_to_ort_tracking_realtime_message()` -- Produces a single `ORTTrackingRealtimeMessage` from either the `out_alert` (preferred) or `in_alert` data.

- `convert_outsight_to_ort_tracking_history_message()` -- Produces an `ORTTrackingHistoryMessage` containing both in and out detection points as path items. Returns `None` if no `out_alert` or `end_timestamp` is present.

### Sender (`app/sender.py`)

- Uses `amqtt.client.MQTTClient` with `reconnect_retries=-1` for infinite reconnection
- Exposes an async context manager `client` that connects on enter and disconnects on exit
- `send(topic, payload)` publishes raw bytes to the specified MQTT topic

### Service Orchestration (`app/service.py`)

The `Service` class ties everything together:

1. Creates consumer, sender, and converter from settings
2. Opens both consumer and sender connections via async context managers
3. Iterates over consumer messages, converts each one, and publishes the results
4. Handles `ValidationError` from pydantic (logs warning and skips invalid messages)
5. Handles graceful shutdown on `KeyboardInterrupt` / `CancelledError`
