# ====================================================
# Project: mcp2tcp
# Description: A protocol conversion tool that enables 
#              hardware devices to communicate with 
#              large language models (LLM) through serial ports.
# Repository: https://github.com/mcp2everything/mcp2tcp.git
# License: MIT License
# Author: mcp2everything
# Copyright (c) 2024 mcp2everything
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
# ====================================================
from typing import Any, Optional, Tuple, Dict, List
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import logging
import yaml
import os
from dataclasses import dataclass, field
import time
import socket

# 设置日志级别为 DEBUG
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以显示更多信息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加版本号常量
VERSION = "0.1.0"  # 添加了自动\r\n和更详细的错误信息

server = Server("mcp2tcp")

@dataclass
class Command:
    """Configuration for a serial command."""
    command: str
    need_parse: bool
    data_type: str  # 新增：数据类型
    prompts: List[str]

@dataclass
class Config:
    """Configuration for mcp2tcp service."""
    remote_ip: Optional[str] = None
    port: int = 12345
    connect_timeout: float = 3.0
    receive_timeout: float = 3.0
    timeout: float = 1.0
    read_timeout: float = 1.0
    response_start_string: str = "OK"  # 新增：可配置的应答开始字符串
    communication_type: str = "client"  # 新增：通信类型
    commands: Dict[str, Command] = field(default_factory=dict)

    @staticmethod
    def load(config_path: str = "config.yaml") -> 'Config':
        """Load configuration from YAML file."""
        # 获取配置文件名
        config_name = os.path.basename(config_path)
        # 定义可能的配置文件位置
        config_paths = [
            config_path,  # 首先检查指定的路径
            os.path.join(os.getcwd(), config_name),  # 当前工作目录
            os.path.expanduser(f"~/.mcp2tcp/{config_name}"),  # 用户主目录
        ]
        
        # 添加系统级目录
        if os.name == 'nt':  # Windows
            config_paths.append(os.path.join(os.environ.get("ProgramData", "C:\\ProgramData"),
                                           "mcp2tcp", config_name))
        else:  # Linux/Mac
            config_paths.append(f"/etc/mcp2tcp/{config_name}")

        # 尝试从每个位置加载配置
        for path in config_paths:
            if (os.path.exists(path)):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                    logger.info(f"Loading configuration from {path}")
                    
                    # Load TCP configuration
                    tcp_config = config_data.get('tcp', {})
                    config = Config(
                        remote_ip=tcp_config.get('remote_ip'),
                        port=tcp_config.get('port', 12345),
                        connect_timeout=tcp_config.get('connect_timeout', 3.0),
                        receive_timeout=tcp_config.get('receive_timeout', 3.0),
                        response_start_string=tcp_config.get('response_start_string', 'OK'),  # 新增：加载应答开始字符串
                        communication_type=tcp_config.get('communication_type', 'client')  # 新增：加载通信类型
                    )

                    # Load commands
                    commands_data = config_data.get('commands', {})
                    for cmd_id, cmd_data in commands_data.items():
                        raw_command = cmd_data.get('command', '')
                        logger.debug(f"Loading command {cmd_id}: {repr(raw_command)}")
                        config.commands[cmd_id] = Command(
                            command=raw_command,
                            need_parse=cmd_data.get('need_parse', False),
                            data_type=cmd_data.get('data_type', 'ascii'),  # 新增：加载数据类型
                            prompts=cmd_data.get('prompts', [])
                        )
                        logger.debug(f"Loaded command {cmd_id}: {repr(config.commands[cmd_id].command)}")

                    return config
                except Exception as e:
                    logger.warning(f"Error loading config from {path}: {e}")
                    continue

        logger.info("No valid config file found, using defaults")
        return Config()

config = Config.load()

class TCPConnection:
    """TCP connection manager."""
    
    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.remote_ip: str = config.remote_ip
        self.port: int = config.port
        self.connect_timeout: float = config.connect_timeout
        self.receive_timeout: float = config.receive_timeout * 5  # 增加接收超时时间
        self.response_start_string: str = config.response_start_string

    def connect(self) -> bool:
        """Attempt to connect to the TCP server."""
        try:
            if self.socket:
                self.socket.close()
            self.socket = socket.create_connection(
                (self.remote_ip, self.port), 
                timeout=self.connect_timeout
            )
            logger.info(f"Connected to TCP server at {self.remote_ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to TCP server: {str(e)}")
            return False

    def send_command(self, command: Command, arguments: dict[str, Any] | None) -> list[types.TextContent]:
        """Send a command to the TCP server and return result according to MCP protocol."""
        try:
            if not self.socket:
                if not self.connect():
                    return [types.TextContent(
                        type="text",
                        text=f"Failed to connect to TCP server at {self.remote_ip}:{self.port}"
                    )]
            if command.data_type == "ascii":
                # 准备命令
                cmd_str = command.command.format(**arguments)
                # 确保命令以\r\n结尾
                cmd_str = cmd_str.rstrip() + '\r\n'  # 移除可能的空白字符，强制添加\r\n
                command_bytes = cmd_str.encode()
                logger.info(f"Sending command: {cmd_str.strip()}")
                logger.info(f"Sent command: {command_bytes.strip().decode('ascii')}")
                self.socket.sendall(command_bytes)

            elif command.data_type == "hex":
                command_bytes = bytes.fromhex(command.command.replace(" ", ""))
                logger.info(f"Sent command: {command.command}")
                self.socket.sendall(command_bytes)
            self.socket.settimeout(self.receive_timeout)
            responses = []
            while True:
                try:
                    response = self.socket.recv(4096)
                    if response:
                        logger.debug(f"Received data: {response}")
                        responses.append(response)
                        if command.data_type == "ascii" and response.endswith(b'\r\n'):
                            break
                        elif command.data_type == "hex":
                            break
                    else:
                        break
                except socket.timeout as e:
                    logger.error(f"TCP receive timeout: {str(e)}")
                    return [types.TextContent(
                        type="text",
                        text=f"TCP receive timeout: {str(e)}"
                    )]

            if not responses:
                return [types.TextContent(
                    type="text",
                    text=f"No response received from TCP server within {self.receive_timeout} seconds"
                )]

            first_response = responses[0].decode().strip()
            logger.info(f"Received response: {first_response}")

            if self.response_start_string in first_response:
                return [types.TextContent(
                    type="text",
                    text=first_response
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Invalid response: {first_response}"
                )]

        except socket.timeout as e:
            logger.error(f"TCP send timeout: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"TCP send timeout: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"TCP error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"TCP error: {str(e)}"
            )]

    def close(self) -> None:
        """Close the TCP connection if open."""
        if self.socket:
            self.socket.close()
            logger.info(f"Closed TCP connection to {self.remote_ip}:{self.port}")
            self.socket = None

tcp_connection = TCPConnection()

def send_command(command, arguments):
    response = tcp_connection.send_command(command,arguments)
    logger.info(f"Received response: {response}")
    print(f"Received response: {response}")
    return response

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the MCP service."""
    logger.info("Listing available tools")
    tools = []
    
    for cmd_id, command in config.commands.items():
        # 从命令字符串中提取参数名
        import re
        param_names = re.findall(r'\{(\w+)\}', command.command)
        properties = {name: {"type": "string"} for name in param_names}
        
        tools.append(types.Tool(
            name=cmd_id,
            description=f"Execute {cmd_id} command",
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": param_names
            },
            prompts=command.prompts
        ))
    
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle tool execution requests according to MCP protocol."""
    logger.info(f"Tool call received - Name: {name}, Arguments: {arguments}")
    
    try:
        if name not in config.commands:
            error_msg = f"[mcp2tcp v{VERSION}] Error: Unknown tool '{name}'\n"
            error_msg += "Please check:\n"
            error_msg += "1. Tool name is correct\n"
            error_msg += "2. Tool is configured in config.yaml"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]

        command = config.commands[name]
        if arguments is None:
            arguments = {}
        
        # 发送命令并返回 MCP 格式的响应
        return tcp_connection.send_command(command, arguments)

    except Exception as e:
        logger.error(f"Error handling tool call: {str(e)}")
        error_msg = f"[mcp2tcp v{VERSION}] Error: {str(e)}\n"
        error_msg += "Please check:\n"
        error_msg += "1. Configuration is correct\n"
        error_msg += "2. Device is functioning properly"
        return [types.TextContent(
            type="text",
            text=error_msg
        )]

async def main(config_name: str = None) -> None:
    """Run the MCP server.
    
    Args:
        config_name: Optional configuration name. If not provided, uses default config.yaml
    """
    logger.info("Starting mcp2tcp server")
    
    # 处理配置文件名
    if config_name and config_name != "default":
        if not config_name.endswith("_config.yaml"):
            config_name = f"{config_name}_config.yaml"
    else:
        config_name = "config.yaml"
        
    # 加载配置
    global config
    config = Config.load(config_name)
    # communication_type = config.communication_type
    # for command in config.commands.values():
    #     logger.info(f"Loaded command: {command.command}")
    #     if communication_type == "client":
    #         pass
    #     elif communication_type == "server":
    #         pass
    #     arguments = {}
    #     # 判断字符串是否以 "PWM" 开头
    #     if "PWM" in command.command:
    #         # 示例参数
    #         arguments = {"frequency": 1000}
    #     if "LED" in command.command:
    #         # 示例参数
    #         arguments = {"state": 1}
    #     # 发送命令
    #     response = send_command(command, arguments)
    #     print(response)
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp2tcp",
                    server_version=VERSION,
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        tcp_connection.close()

# 示例调用
if __name__ == "__main__":
    import sys
    config_name = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(config_name))