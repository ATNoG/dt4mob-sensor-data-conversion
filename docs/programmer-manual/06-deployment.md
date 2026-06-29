## Deployment

### Docker Build

The `Dockerfile` uses a single-stage build:

1. **Base image**: `python:3.13-slim`
2. **Package manager**: Copies `uv` from the official Astral image (`ghcr.io/astral-sh/uv:latest`)
3. **Dependencies**: Copies `pyproject.toml`, `uv.lock`, `.python-version` first for layer caching, then runs `uv sync --frozen --no-cache`
4. **Application**: Copies source code
5. **Entry command**: `uv run main.py`

### Production Deployment

```bash
# Build the image
docker compose build

# Deploy (with detached mode)
docker compose up -d

# View logs
docker compose logs -f conversion-service

# Stop
docker compose down
```

### Docker Compose Configuration

The `compose.yml` mounts `config.toml` as a read-only volume and exposes port `8000` for the webhook consumer. The `host.docker.internal` hostname is mapped to the host gateway, allowing the service to reach an MQTT broker running on the host machine.

For production deployments, ensure:

- `config.toml` is configured with the correct broker URLs and reference plane coordinates
- The MQTT broker is network-reachable from the container
- Port `8000` is only exposed if the webhook consumer is in use
