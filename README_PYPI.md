# MCP2Serial: Bridge between AI Models and Physical World

Connect AI Large Language Models to hardware devices through the Model Context Protocol (MCP).

[GitHub Repository](https://github.com/mcp2everything/mcp2tcp) | [Documentation](https://github.com/mcp2everything/mcp2tcp/tree/main/docs)

## Features

- **Intelligent Serial Communication**
  - Automatic port detection and configuration
  - Multiple baud rate support (default 115200)
  - Real-time status monitoring and error handling

- **MCP Protocol Integration**
  - Full Model Context Protocol support
  - Resource management and tool invocation
  - Flexible prompt system

## Supported Clients

MCP2Serial supports all clients implementing the MCP protocol, including:

- Claude Desktop (Test ok)
- Continue (Should work)
- Cline (Test ok)

## Quick Start
make sure you have installed uv
```
```bash
windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
MacOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## Basic Configuration

Add the following to your MCP client configuration:

```json
{
    "mcpServers": {
        "mcp2tcp": {
            "command": "uvx",
            "args": ["mcp2tcp"]
        }
    }
}
```

## Serial Port Configuration

Create or modify `config.yaml` to configure serial port parameters:

```yaml
serial:
  port: COM11  # Windows example, on Linux might be /dev/ttyUSB0
  baud_rate: 115200  # Baud rate
  timeout: 1.0  # Serial timeout (seconds)
  read_timeout: 0.5  # Read timeout (seconds)
```

If `port` is not specified, the program will automatically search for available serial ports.

## Configuration File Location

The configuration file (`config.yaml`) can be placed in different locations depending on your needs. The program searches for the configuration file in the following order:

### 1. Current Working Directory (For Development)
- Path: `./config.yaml`
- Example: If you run the program from `C:\Projects`, it will look for `C:\Projects\config.yaml`
- Best for: Development and testing
- No special permissions required

### 2. User's Home Directory (Recommended for Personal Use)
- Windows: `C:\Users\YourName\.mcp2tcp\config.yaml`
- macOS: `/Users/YourName/.mcp2tcp/config.yaml`
- Linux: `/home/username/.mcp2tcp/config.yaml`
- Best for: Personal configuration
- Create the `.mcp2tcp` directory if it doesn't exist
- No special permissions required

### 3. System-wide Configuration (For Multi-user Setup)
- Windows: `C:\ProgramData\mcp2tcp\config.yaml` (requires admin rights)
- macOS/Linux: `/etc/mcp2tcp/config.yaml` (requires sudo/root)
- Best for: Shared configuration in multi-user environments
- Create the directory with appropriate permissions

The program will use the first valid configuration file it finds in this order. Choose the location based on your needs:
- For testing: use current directory
- For personal use: use home directory (recommended)
- For system-wide settings: use ProgramData or /etc

## Serial Port Configuration

Create your `config.yaml` in one of the above locations with the following structure:

```yaml
serial:
  port: COM11  # or /dev/ttyUSB0 for Linux
  baud_rate: 115200
  timeout: 1.0
  read_timeout: 0.5

commands:
  # Add your commands here
  # See the Command Configuration section for examples
```

## Command Configuration

Add or remove custom commands in `config.yaml`:

```yaml
commands:
  # PWM control command example
  set_pwm:
    command: "PWM {frequency}\n"  # Actual command format to send
    need_parse: false  # No need to parse response
    prompts:  # Prompt list
      - "Set PWM to {value}"
      - "Turn off PWM"

  # LED control command example
  led_control:
    command: "LED {state}\n"  # state can be on/off or other values
    need_parse: false
    prompts:
      - "Turn on LED"
      - "Turn off LED"
      - "Set LED state to {state}"

  # Command example with response parsing
  get_sensor:
    command: "GET_SENSOR\n"
    need_parse: true  # Need to parse response
    prompts:
      - "Read sensor data"
```

### Response Parsing

1. Simple Response (`need_parse: false`):
   - Device returns message starting with "OK" indicates success
   - Other responses will be treated as errors

2. Parsed Response (`need_parse: true`):
   - Complete response will be returned in the `result.raw` field

## Documentation

For detailed documentation, please visit our [GitHub repository](https://github.com/mcp2everything/mcp2tcp).

## Support

If you encounter any issues or have questions:
1. Check our [Issues](https://github.com/mcp2everything/mcp2tcp/issues) page
2. Read our [Wiki](https://github.com/mcp2everything/mcp2tcp/wiki)
3. Create a new issue if needed

## License

This project is licensed under the MIT License.
