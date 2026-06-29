## Troubleshooting

### Common Issues

| Issue | Solution |
| ----- | -------- |
| Service exits immediately | Verify `config.toml` exists and is valid TOML. Change `log_level` to `DEBUG` for verbose output. |
| No messages being received | Check that the consumer backend matches your OutSight sensor output (MQTT or webhook). Verify connection details (host, port, URL, topics). |
| MQTT connection refused | Verify the broker URL in `[sender]` and `[consumer]` sections. Check that the broker is running and accessible. |
| Webhook not receiving data | Confirm the webhook port (default `8000`) is not blocked by a firewall. Verify the POST request path matches `base_path`. |
| Converted messages missing fields | Ensure `[converter.outsight_reference_plane]` and `[converter.atobe_reference_plane]` are configured with correct coordinates for your deployment. |
| Validation errors in logs | The incoming message does not match the expected OutSight format. Enable `DEBUG` logging to see the raw message and validation details. |

### Logging

Increase verbosity by setting `log_level = "DEBUG"` in `config.toml` or via environment variable:

```bash
export SENSOR_DATA_CONVERSION_LOG_LEVEL="DEBUG"
```

Available log levels: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`.

### Further Help

- Check `config.toml` against `config.example.toml` for field reference
- Enable `DEBUG` logging to see detailed processing output
