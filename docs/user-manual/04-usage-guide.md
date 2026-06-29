## Usage Guide

### Starting the Service

Once started, the service will:

1. Connect to the configured consumer (MQTT broker or webhook endpoint)
2. Begin listening for OutSight messages
3. Convert each incoming message into ORT Tracking format (real-time and optionally history)
4. Publish the converted messages to the configured MQTT broker

### Processing Pipeline

The service processes messages through three stages:

1. **Consumer** receives raw OutSight JSON messages via MQTT subscription or HTTP webhook POST
2. **Converter** transforms OutSight data into ORT Tracking format:
   - Derives object **dimensions** (length, width, height) from bounding box corners
   - Converts **local coordinates** via ENU (East-North-Up) intermediate using the configured reference planes
   - Computes **absolute coordinates** (latitude/longitude) from the ENU position
   - Extracts **object ID**, **timestamp**, and **speed** directly
3. **Sender** publishes the converted messages to the configured MQTT topics

### OutSight Input Format

OutSight messages contain vehicle detections with bounding box coordinates:

```json
{
  "start_timestamp": "2024-01-15T10:30:00Z",
  "end_timestamp": "2024-01-15T10:30:01Z",
  "data": {
    "in_alert": {
      "object_id": 42,
      "speed": 85.5,
      "coordinate": [[x0, y0], [x1, y1], [x2, y2], [x3, y3]],
      "height": 2.1
    },
    "out_alert": {
      "object_id": 42,
      "speed": 82.3,
      "coordinate": [[x0, y0], [x1, y1], [x2, y2], [x3, y3]],
      "height": 2.1
    }
  }
}
```

### ORT Tracking Output Format

Converted real-time messages are published to the `atb_realtime_topic`:

```json
{
  "objectID": 42,
  "timeOfMeasurement": "2024-01-15T10:30:01Z",
  "speedKmh": 82.3,
  "absoluteCoordinates": { "latitude": 38.7113, "longitude": -9.3092 },
  "dimensions": { "width": 1.85, "length": 4.52, "height": 2.1 },
  "localCoordinates": { "x": 1.23, "y": 4.56 }
}
```

If an `out_alert` is present (indicating the vehicle has left the detection zone), a history message is also published to the `atb_history_topic` containing a path with both in and out detection points:

```json
{
  "objectID": 42,
  "path": [
    { "timeOfMeasurement": "...", "speedKmh": 85.5, "localCoordinates": {...}, "absoluteCoordinates": {...}, "dimensions": {...} },
    { "timeOfMeasurement": "...", "speedKmh": 82.3, "localCoordinates": {...}, "absoluteCoordinates": {...}, "dimensions": {...} }
  ]
}
```

### Stopping the Service

Press `Ctrl+C` or send a `SIGINT`/`SIGTERM` signal. The service will log a termination message and disconnect cleanly.
