## Installation

**Option A: Run Directly with uv**

```bash
# Clone the repository
git clone https://github.com/ATNoG/dt4mob-sensor-data-conversion.git
cd dt4mob-sensor-data-conversion

# Install dependencies
uv sync

# Copy and edit the example configuration
cp config.example.toml config.toml
# Edit config.toml with your settings (see Configuration section)

# Run the service
uv run main.py
```

**Option B: Run with Docker Compose**

```bash
# Clone the repository
git clone https://github.com/ATNoG/dt4mob-sensor-data-conversion.git
cd dt4mob-sensor-data-conversion

# Copy and edit the example configuration
cp config.example.toml config.toml
# Edit config.toml with your settings (see Configuration section)

# Build and start
docker compose up --build
```

The Docker Compose setup automatically:

- Mounts `config.toml` as a read-only volume at `/app/config.toml`
- Exposes port `8000` (used by the webhook consumer)
- Maps `host.docker.internal` to the host gateway for local broker access
