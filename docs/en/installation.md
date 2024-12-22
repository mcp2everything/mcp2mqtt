# MCP2Serial Installation Guide

## Requirements

- Python 3.11 or higher
- uv package manager
- Serial device (e.g., Arduino, Raspberry Pi Pico)

### Installation

#### For Windows Users
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2tcp/main/install.py

# Run the installation script
python install.py
```

#### For MacOS Users
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2tcp/main/install_macos.py

# Run the installation script
python3 install_macos.py
```

The installation script will automatically:
- ✅ Check system environment
- ✅ Install required dependencies
- ✅ Create default configuration file
- ✅ Configure Claude Desktop (if installed)
- ✅ Check serial devices

2. Configure serial port and commands:
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
        "mcp2tcp": {
            "command": "uvx",
            "args": ["mcp2tcp"]
        }
    }
}


## Configuration

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
C:\Users\YourName\.mcp2tcp\config.yaml

# macOS
/Users/YourName/.mcp2tcp/config.yaml

# Linux
/home/username/.mcp2tcp/config.yaml
```
- Best for: Personal configuration
- Create the `.mcp2tcp` directory if it doesn't exist:
  ```bash
  # Windows (in Command Prompt)
  mkdir "%USERPROFILE%\.mcp2tcp"
  
  # macOS/Linux
  mkdir -p ~/.mcp2tcp
  ```

#### 3. System-wide Configuration (For Multi-user Setup)
```bash
# Windows (requires admin rights)
C:\ProgramData\mcp2tcp\config.yaml

# macOS/Linux (requires sudo/root)
/etc/mcp2tcp/config.yaml
```
- Best for: Shared configuration in multi-user environments
- Create the directory with appropriate permissions:
  ```bash
  # Windows (as administrator)
  mkdir "C:\ProgramData\mcp2tcp"
  
  # macOS/Linux (as root)
  sudo mkdir -p /etc/mcp2tcp
  sudo chown root:root /etc/mcp2tcp
  sudo chmod 755 /etc/mcp2tcp
  ```

The program searches for the configuration file in this order and uses the first valid file it finds. Choose the location based on your needs:
- For testing: use current directory
- For personal use: use home directory (recommended)
- For system-wide settings: use ProgramData or /etc

### Serial Port Configuration

Configure serial port parameters in `config.yaml`:

```yaml
serial:
  port: COM11  # Example for Windows, might be /dev/ttyUSB0 on Linux
  baud_rate: 115200  # Baud rate
  timeout: 1.0  # Serial timeout in seconds
  read_timeout: 0.5  # Read timeout in seconds
```

### MCP Client Configuration

When using MCP protocol-compatible clients (like Claude Desktop or Cline), add the following to your client's configuration file:

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
if you want to develop locally, you can use the following configuration:
```json
{
    "mcpServers": {
        "mcp2tcp": {
            "command": "uv",
            "args": [
                "--directory",
                "your project path/mcp2tcp",  // ex: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2tcp"
                "run",
                "mcp2tcp"
            ]
        }
    }
}
```
<div align="center">
    <img src="../images/client_config.png" alt="Client Configuration Example" width="600"/>
    <p>Configuration Example in Claude Desktop</p>
</div>

<div align="center">
    <img src="../images/cline_config.png" alt="Cline Configuration Example" width="600"/>
    <p>Configuration Example in Cline</p>
</div>

> **Important Notes:**
> 1. Use absolute paths only
> 2. Use forward slashes (/) or double backslashes (\\) as path separators
> 3. Ensure the path points to your actual project installation directory

## Development Steps

1. Clone the repository:

```bash
# Clone the repository
git clone https://github.com/mcp2everything/mcp2tcp.git
```

2. Create and activate virtual environment:

```bash
# Navigate to project directory
cd mcp2tcp

# Create virtual environment using uv
uv venv .venv
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

> **Note:** The project will be available on PyPI soon, enabling direct installation via pip.

## Running the Server

```bash
# Ensure you're in the project root
cd mcp2tcp

# Activate virtual environment (if not already activated)
.venv\Scripts\activate

# Run the server
uv run src/mcp2tcp/server.py
```

## Troubleshooting

1. Serial Port Issues:
   - Ensure the device is properly connected
   - Verify the correct COM port in Device Manager
   - Check baud rate settings match your device

2. MCP Client Issues:
   - Verify the path in configuration is absolute and correct
   - Ensure uv is installed and in system PATH
   - Check if virtual environment is activated

3. Communication Issues:
   - Monitor the serial output for debugging
   - Check device response format
   - Verify command syntax in config.yaml
