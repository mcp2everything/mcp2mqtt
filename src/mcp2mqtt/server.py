import os
import logging
import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import paho.mqtt.client as mqtt
import yaml
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# 设置日志级别为 DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Tool:
    """Tool configuration."""
    name: str
    description: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    mqtt_topic: str = ""
    response_topic: str = ""
    response_format: str = ""

@dataclass
class Config:
    """Configuration for mcp2mqtt service."""
    mqtt_broker: str = "broker.emqx.io"
    mqtt_port: int = 1883
    mqtt_client_id: str = "mcp2mqtt_client"
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_keepalive: int = 60
    mqtt_response_start_string: str = "CMD"
    tools: Dict[str, Tool] = field(default_factory=dict)

    @staticmethod
    def load(config_path: str = "config.yaml") -> 'Config':
        """Load configuration from YAML file."""
        try:
            logger.info(f"Opening configuration file: {config_path}")
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                logger.info("Successfully parsed YAML configuration")
            
            # 加载 MQTT 配置
            mqtt_config = data.get('mqtt', {})
            logger.info("Loading MQTT configuration...")
            config = Config(
                mqtt_broker=mqtt_config.get('broker', "broker.emqx.io"),
                mqtt_port=mqtt_config.get('port', 1883),
                mqtt_client_id=mqtt_config.get('client_id', "mcp2mqtt_client"),
                mqtt_username=mqtt_config.get('username', ""),
                mqtt_password=mqtt_config.get('password', ""),
                mqtt_keepalive=mqtt_config.get('keepalive', 60),
                mqtt_response_start_string=mqtt_config.get('response_start_string', "CMD")
            )
            logger.info("MQTT configuration loaded")
            
            # 加载工具配置
            logger.info("Loading tools configuration...")
            tools_count = 0
            for tool_name, tool_data in data.get('tools', {}).items():
                logger.info(f"Loading tool: {tool_name}")
                config.tools[tool_name] = Tool(
                    name=tool_data.get('name', ''),
                    description=tool_data.get('description', ''),
                    parameters=tool_data.get('parameters', []),
                    mqtt_topic=tool_data.get('mqtt_topic', ''),
                    response_topic=tool_data.get('response_topic', ''),
                    response_format=tool_data.get('response_format', '')
                )
                tools_count += 1
            logger.info(f"Loaded {tools_count} tools")
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

class MQTTConnection:
    """MQTT connection manager."""
    
    def __init__(self, config):
        """Initialize MQTT connection."""
        self.config = config
        self.client = None
        self.connected = False
        self.response_start_string = config.mqtt_response_start_string
        self.response = None
        self.response_received = asyncio.Event()
        logger.info(f"Initialized MQTT connection manager")
    
    def setup_client(self):
        """Setup MQTT client"""
        if self.client is not None:
            return
            
        self.client = mqtt.Client(client_id=f"{self.config.mqtt_client_id}_{int(time.time())}")
        if self.config.mqtt_username:
            self.client.username_pw_set(self.config.mqtt_username, self.config.mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server."""
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker successfully")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")
            self.connected = False
    
    def on_message(self, client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server."""
        try:
            payload = msg.payload.decode()
            logger.info(f"Received message on topic {msg.topic}: {payload}")
            self.response = payload
            self.response_received.set()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the server."""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker with result code: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")
    
    async def connect_and_send(self, topic: str, message: str, response_topic: str = None, timeout: int = 5) -> Optional[str]:
        """Connect to broker, send message, wait for response, and disconnect."""
        try:
            # 设置客户端
            self.setup_client()
            self.response = None
            self.response_received.clear()
            
            # 连接到服务器
            logger.info(f"Connecting to MQTT broker at {self.config.mqtt_broker}")
            self.client.connect(
                self.config.mqtt_broker,
                self.config.mqtt_port,
                keepalive=10  # 使用较短的 keepalive
            )
            
            # 如果需要等待响应，订阅响应主题
            if response_topic:
                self.client.subscribe(response_topic)
                logger.info(f"Subscribed to response topic: {response_topic}")
            
            # 启动循环
            self.client.loop_start()
            
            # 等待连接成功
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                await asyncio.sleep(0.1)
            
            if not self.connected:
                raise Exception("Failed to connect to MQTT broker")
            
            # 发送消息
            logger.info(f"Publishing message to {topic}: {message}")
            self.client.publish(topic, message)
            
            # 如果需要等待响应
            response = None
            if response_topic:
                try:
                    # 等待响应
                    await asyncio.wait_for(self.response_received.wait(), timeout)
                    response = self.response
                except asyncio.TimeoutError:
                    logger.error("Timeout waiting for response")
                    raise Exception("Timeout waiting for response")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in connect_and_send: {e}")
            raise
        finally:
            # 清理连接
            self.cleanup()
    
    def cleanup(self):
        """Clean up MQTT connection."""
        try:
            if self.client:
                self.client.loop_stop()
                if self.connected:
                    self.client.disconnect()
                self.client = None
            self.connected = False
            logger.info("Cleaned up MQTT connection")
        except Exception as e:
            logger.error(f"Error cleaning up connection: {e}")

# 创建 MCP 服务器
server = Server("mcp2mqtt")
config = None

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools."""
    tools = []
    for tool_name, tool_config in config.tools.items():
        tools.append(
            types.Tool(
                name=tool_config.name,
                description=tool_config.description,
                inputSchema={
                    "type": "object",
                    "properties": {
                        param["name"]: {
                            "type": param["type"],
                            "description": param["description"],
                            **({"enum": param["enum"]} if "enum" in param else {})
                        }
                        for param in tool_config.parameters
                    },
                    "required": [
                        param["name"]
                        for param in tool_config.parameters
                        if param.get("required", False)
                    ]
                }
            )
        )
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> List[types.TextContent | types.ImageContent]:
    """Handle tool execution requests."""
    try:
        logger.info(f"Tool call received - Name: {name}, Arguments: {arguments}")
        
        # 检查工具是否存在
        if name not in config.tools:
            return [types.TextContent(
                type="text",
                text=f"Error: Tool {name} not found"
            )]
            
        tool_config = config.tools[name]
        
        # 验证参数
        if arguments is None:
            arguments = {}
            
        # 检查必需参数
        for param in tool_config.parameters:
            if param.get('required', False) and param['name'] not in arguments:
                return [types.TextContent(
                    type="text",
                    text=f"Error: Missing required parameter {param['name']}"
                )]
                
            # 验证枚举值
            if 'enum' in param and param['name'] in arguments:
                if arguments[param['name']] not in param['enum']:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: Invalid value for {param['name']}"
                    )]
        
        # 准备消息
        message = None
        if name == "set_pwm":
            frequency = arguments.get("frequency", 0)
            if not (0 <= frequency <= 100):
                return [types.TextContent(
                    type="text",
                    text="Error: Frequency must be between 0 and 100"
                )]
            message = f"PWM {frequency}"
            
        elif name == "get_pico_info":
            message = "INFO"
            
        elif name == "led_control":
            state = arguments.get("state", "").lower()
            if state not in ["on", "off"]:
                return [types.TextContent(
                    type="text",
                    text="Error: State must be 'on' or 'off'"
                )]
            message = f"LED {state}"
            
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown tool {name}"
            )]
        
        # 发送消息并等待响应
        mqtt_connection = MQTTConnection(config)
        response = await mqtt_connection.connect_and_send(
            topic=tool_config.mqtt_topic,
            message=message,
            response_topic=tool_config.response_topic
        )
        
        return [types.TextContent(
            type="text",
            text=response if response else f"{config.mqtt_response_start_string} {message} OK"
        )]
        
    except Exception as e:
        logger.error(f"Error handling tool call: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main(config_name: str = None) -> None:
    """Run the MCP server."""
    try:
        # 加载配置
        config_path = config_name if config_name else "config.yaml"
        if not os.path.isfile(config_path):
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
        
        logger.info(f"Loading configuration from {config_path}")
        if not os.path.isfile(config_path):
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        global config
        config = Config.load(config_path)
        logger.info("Configuration loaded successfully")
        logger.info(f"MQTT Broker: {config.mqtt_broker}")
        logger.info(f"MQTT Port: {config.mqtt_port}")
        logger.info(f"Available tools: {list(config.tools.keys())}")
        
        # 运行 MCP 服务器
        logger.info("Starting MCP server...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp2mqtt",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    import sys
    config_name = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(config_name))