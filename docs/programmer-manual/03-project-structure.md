## Project Structure

### Key Files

| Path                  | Description                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| `main.py`             | Application entry point -- creates and runs the `Service`                                     |
| `app/service.py`      | Core orchestration -- wires consumer, converter, and sender into an async processing pipeline |
| `app/sender.py`       | MQTT sender -- publishes converted messages via `amqtt`                                       |
| `app/interfaces/`     | Abstract base classes defining the programming interface for pluggable components             |
| `app/drivers/`        | Concrete driver implementations for each interface                                            |
| `app/lib/`            | Core conversion logic                                                                         |
| `app/lib/convert.py`  | `OutSightToAToBe` class -- coordinate transforms, dimension calculations, message conversion  |
| `app/models/`         | Pydantic data models for input/output messages and shared types                               |
| `app/settings/`       | Pydantic-settings configuration models                                                        |
| `config.example.toml` | Documented example configuration with all available options                                   |
| `docs/`               | Documentation sources (user manual, programmer manual)                                        |
