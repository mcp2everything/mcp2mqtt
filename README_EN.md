# mcp2mqtt: Bridge Between Physical World and AI Large Models

English | [简体中文](README.md)

<div align="center">
    <img src="docs/images/logo.png" alt="mcp2mqtt Logo" width="200"/>
    <p>Control Hardware Through Natural Language, Opening a New Era of IoT</p>
</div>

mcp2mqtt is a serial communication server based on the MCP service interface protocol, designed for communication with serial devices. It provides a simple configuration approach for defining and managing serial commands.

## Features

- 🔌 Automatic serial port detection and connection management
- 📝 Simple YAML configuration
- 🛠️ Customizable commands and response parsing
- 🌐 Multi-language prompt support
- 🚀 Asynchronous communication support
- Auto-detect and connect to serial ports at 115200 baud rate
- Control PWM frequency (range: 0-100)
- Compliant with Claude MCP protocol
- Comprehensive error handling and status feedback
- Cross-platform support (Windows, Linux, macOS)
- **Smart MQTT Communication**
  - Support for MQTT protocol publish/subscribe model
  - Support for various MQTT servers (e.g., Mosquitto, EMQ X)
  - QoS (Quality of Service) guarantee
  - Topic filtering and message routing
  - Real-time status monitoring and error handling

## System Architecture

<div align="center">
    <img src="docs/images/stru_en.png" alt="System Architecture" width="800"/>
    <p>mcp2mqtt System Architecture</p>
</div>

## Workflow

<div align="center">
    <img src="docs/images/workflow_en.png" alt="Workflow" width="800"/>
    <p>mcp2mqtt Workflow</p>
</div>

## Project Vision

mcp2mqtt is a project that connects IoT devices with AI large models through Model Context Protocol (MCP) and MQTT protocol, achieving seamless integration between the physical world and AI models. The ultimate goals are:
- Control your hardware devices using natural language
- Real-time AI response and physical parameter adjustment
- Enable your devices to understand and execute complex instructions
- Enable device interconnection through MQTT protocol

## Key Features

- **MCP Protocol Integration**
  - Complete support for Model Context Protocol
  - Resource management and tool invocation support
  - Flexible prompt system
  - Command publishing and response through MQTT

## Configuration Guide

### MQTT Configuration
```yaml
mqtt:
  broker: "localhost"  # MQTT server address
  port: 1883  # MQTT server port
  client_id: "mcp2mqtt_client"  # MQTT client ID
  username: "mqtt_user"  # MQTT username
  password: "mqtt_password"  # MQTT password
  keepalive: 60  # Keep-alive time
  topics:
    command:
      publish: "mcp/command"  # Command publishing topic
      subscribe: "mcp/response"  # Response subscription topic
    status:
      publish: "mcp/status"  # Status publishing topic
      subscribe: "mcp/control"  # Control command subscription topic
```

### Command Configuration
```yaml
commands:
  set_pwm:
    command: "CMD_PWM {frequency}"
    need_parse: false
    data_type: "ascii"
    prompts:
      - "Set PWM to maximum"
      - "Set PWM to minimum"
    mqtt_topic: "mcp/pwm"  # MQTT publish topic
    response_topic: "mcp/pwm/response"  # MQTT response topic
```

## Supported Clients

mcp2mqtt supports all clients implementing the MCP protocol and IoT devices supporting the MQTT protocol:

| Client Type | Feature Support | Description |
|------------|----------------|-------------|
| Claude Desktop | Full Support | Recommended, supports all MCP features |
| Continue | Full Support | Excellent development tool integration |
| Cline | Resource + Tools | Supports multiple AI providers |
| MQTT Devices | Pub/Sub | Supports all MQTT-compatible IoT devices |

## Quick Start

### Prepare
Python>=3.11 
Claude Desktop or Cline+Vscode


### Installation

#### For Windows Users
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install.py

# Run the installation script
python install.py
```

#### For macOS Users
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install_macos.py

# Run the installation script
python3 install_macos.py
```

#### For Ubuntu/Raspberry Pi Users
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install_ubuntu.py

# Run the installation script
python3 install_ubuntu.py
```

The installation script will automatically:
- ✅ Check system environment
- ✅ Install required dependencies
- ✅ Create default configuration file
- ✅ Configure Claude Desktop (if installed)
- ✅ Check serial devices

### Configuration File Location

The configuration file (`config.yaml`) can be placed in different locations depending on your needs:

#### 1. Current Working Directory (For Development)
- Path: `./config.yaml`
- Example: If you run the program from `C:\Projects`, it will look for `C:\Projects\config.yaml`
- Best for: Development and testing
- No special permissions required

#### 2. User's Home Directory (Recommended for Personal Use)
```bash
# Windows
C:\Users\YourName\.mcp2mqtt\config.yaml

# macOS
/Users/YourName/.mcp2mqtt/config.yaml

# Linux
/home/username/.mcp2mqtt/config.yaml
```
- Best for: Personal configuration
- Create the `.mcp2mqtt` directory if it doesn't exist:
  ```bash
  # Windows (in Command Prompt)
  mkdir "%USERPROFILE%\.mcp2mqtt"
  
  # macOS/Linux
  mkdir -p ~/.mcp2mqtt
  ```

#### 3. System-wide Configuration (For Multi-user Setup)
```bash
# Windows (requires admin rights)
C:\ProgramData\mcp2mqtt\config.yaml

# macOS/Linux (requires sudo/root)
/etc/mcp2mqtt/config.yaml
```
- Best for: Shared configuration in multi-user environments
- Create the directory with appropriate permissions:
  ```bash
  # Windows (as administrator)
  mkdir "C:\ProgramData\mcp2mqtt"
  
  # macOS/Linux (as root)
  sudo mkdir -p /etc/mcp2mqtt
  sudo chown root:root /etc/mcp2mqtt
  sudo chmod 755 /etc/mcp2mqtt
  ```

The program searches for the configuration file in this order and uses the first valid file it finds. Choose the location based on your needs:
- For testing: use current directory
- For personal use: use home directory (recommended)
- For system-wide settings: use ProgramData or /etc

### Serial Port Configuration

Configure serial port and commands in `config.yaml`:
```yaml
# config.yaml
serial:
  port: COM11  # or auto-detect
  baud_rate: 115200

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "Set PWM to {value}%"
```

3.MCP json Configuration
Add the following to your MCP client (like Claude Desktop or Cline) configuration file, making sure to update the path to your actual installation path:

```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uvx",
            "args": ["mcp2mqtt"]
        }
    }
}
```
if you want to develop locally, you can use the following configuration:
```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uv",
            "args": [
                "--directory",
                "your project path/mcp2mqtt",  // ex: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2mqtt"
                "run",
                "mcp2mqtt"
            ]
        }
    }
}
```

> **Important Notes:**
> 1. Use absolute paths only
> 2. Use forward slashes (/) or double backslashes (\\) as path separators
> 3. Ensure the path points to your actual project installation directory



4. launch your client(claude desktop or cline):


## Interacting with Claude

Once the service is running, you can control PWM through natural language conversations with Claude. Here are some example prompts:

- "Set PWM to 50%"
- "Turn PWM to maximum"
- "Turn off PWM output"
- "Adjust PWM frequency to 75%"
- "Can you set PWM to 25%?"

Claude will understand your intent and automatically invoke the appropriate commands. No need to remember specific command formats - just express your needs in natural language.

<div align="center">
    <img src="docs/images/pwm.png" alt="Cline Configuration Example" width="600"/>
    <p> Example in Claude</p>
</div>
<div align="center">
    <img src="docs/images/test_output.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>

## Documentation

- [Installation Guide](./docs/en/installation.md)
- [API Documentation](./docs/en/api.md)
- [Configuration Guide](./docs/en/configuration.md)

## Examples

### 1. Simple Command Configuration
```yaml
commands:
  led_control:
    command: "LED {state}\n"
    need_parse: false
    prompts:
      - "Turn on LED"
      - "Turn off LED"
```

### 2. Command with Response Parsing
```yaml
commands:
  get_temperature:
    command: "GET_TEMP\n"
    need_parse: true
    prompts:
      - "Get temperature"
```

Response example:
```python
{
    "status": "success",
    "result": {
        "raw": "OK TEMP=25.5"
    }
}
```

## Requirements

- Python 3.11+
- pyserial
- mcp

## Installation from source code
 
#### Manual Installation
```bash
# Install from source:
git clone https://github.com/mcp2everything/mcp2mqtt.git
cd mcp2mqtt

# Create virtual environment
uv venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install development dependencies
uv pip install --editable .
```

## Running the Service

Use the `uv run` command to automatically build, install, and run the service:

```bash
uv run src/mcp2mqtt/server.py
```

This command will:
1. Build the mcp2mqtt package
2. Install it in the current environment
3. Start the server


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   uv venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Running Tests

```bash
uv pytest tests/
```

## License

[MIT](LICENSE)

## Acknowledgments

- Thanks to the [Claude](https://claude.ai) team for the MCP protocol
- [pySerial](https://github.com/pyserial/pyserial) for serial communication
- All contributors and users of this project

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/mcp2everything/mcp2mqtt/issues) page
2. Read our [Wiki](https://github.com/mcp2everything/mcp2mqtt/wiki)
3. Create a new issue if needed
