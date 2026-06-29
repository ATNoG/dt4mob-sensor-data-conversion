## Prerequisites

Before using Sensor Data Conversion, ensure you have:

| Requirement        | Version/Details                                                       |
| ------------------ | --------------------------------------------------------------------- |
| Python             | 3.13 or higher                                                        |
| uv package manager | [Install uv](https://docs.astral.sh/uv/getting-started/installation/) |
| MQTT broker        | Accessible instance (e.g., Mosquitto) for the sender and optionally the consumer |

**Optional requirements:**

- Docker and Docker Compose (if running via containers)
- A running OutSight sensor system publishing messages
- An ORT Tracking-compatible consumer subscribing to the converted output topics
