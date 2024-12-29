# Testing Guide

This guide explains how to test the MCP2MQTT service with a simulated device.

## Prerequisites

- Python >= 3.11
- UV package manager
- MQTT broker (default: broker.emqx.io)
- MCP client (e.g., Claude)

## Setup

1. Install dependencies:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. Configure MQTT settings in `config.yaml`:
   ```yaml
   mqtt:
     broker: "broker.emqx.io"  # Use default or your own broker
     port: 1883
     client_id: "mcp2mqtt_client"
   ```

## Running Tests

### 1. Start Device Simulator

The project includes a device simulator in the `tests` directory. This simulates a hardware device that can:
- Respond to PWM control commands
- Provide device information
- Control LED state

Start the simulator:
```bash
python tests/responder.py
```

You should see output indicating that the simulator is running and connected to the MQTT broker.

### 2. Start MCP2MQTT Service

In a new terminal:
```bash
uv run mcp2mqtt
```

The service will:
- Load configuration
- Connect to MQTT broker
- Register available tools
- Wait for MCP commands

### 3. Configure MCP Client

Add the MCP2MQTT service to your MCP client (e.g., Claude):
- Server name: mcp2mqtt
- Version: 0.1.0
- Tools:
  - set_pwm
  - get_pico_info
  - led_control

### 4. Test Commands

Try these example commands:

1. Set PWM frequency:
   ```
   set_pwm frequency=50
   ```
   Expected response: `CMD PWM 50 OK`

2. Get device information:
   ```
   get_pico_info
   ```
   Expected response: `CMD INFO Device:Pico Status:Running OK`

3. Control LED:
   ```
   led_control state=on
   ```
   Expected response: `CMD LED on OK`

## Troubleshooting

1. Connection Issues:
   - Check MQTT broker address and port
   - Verify network connectivity
   - Check firewall settings

2. Command Failures:
   - Verify simulator is running
   - Check MQTT topics match in config
   - Review service logs for errors

3. Response Timeouts:
   - Increase timeout value in configuration
   - Check network latency
   - Verify broker QoS settings

## Next Steps

After testing with the simulator, you can:
1. Connect real hardware devices
2. Customize MQTT topics and message formats
3. Add new tools and commands
4. Implement additional device features
