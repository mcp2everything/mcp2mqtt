#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MQTT应答程序
用于接收MQTT消息并按照配置的格式进行应答
基于配置文件自动处理三种类型的命令：
PWM控制命令
PICO信息查询命令
LED控制命令
响应格式：
PWM命令：CMD PWM {value} OK
INFO命令：CMD INFO Device:Pico Status:Running OK
LED命令：CMD LED {state} OK
"""

import paho.mqtt.client as mqtt
import time
import logging
import yaml
import os
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MQTTResponder:
    """MQTT应答程序类"""
    
    def __init__(self, config_path: str = "../config.yaml"):
        """初始化MQTT应答程序
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)
        self.client = mqtt.Client(client_id=f"{self.config['mqtt']['client_id']}_responder")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def connect(self) -> bool:
        """连接到MQTT服务器"""
        try:
            if self.config['mqtt']['username']:
                self.client.username_pw_set(
                    self.config['mqtt']['username'],
                    self.config['mqtt']['password']
                )
            
            self.client.connect(
                self.config['mqtt']['broker'],
                self.config['mqtt']['port'],
                self.config['mqtt']['keepalive']
            )
            
            self.client.loop_start()
            logger.info(f"Connected to MQTT broker at {self.config['mqtt']['broker']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """连接回调函数"""
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker successfully")
            
            # 订阅所有命令主题
            for cmd_name, cmd in self.config['commands'].items():
                if 'mqtt_topic' in cmd:
                    self.client.subscribe(cmd['mqtt_topic'])
                    logger.info(f"Subscribed to topic: {cmd['mqtt_topic']}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")
    
    def on_message(self, client, userdata, msg):
        """消息回调函数"""
        try:
            payload = msg.payload.decode()
            logger.info(f"Received message on topic {msg.topic}: {payload}")
            
            # 查找对应的命令配置
            for cmd_name, cmd in self.config['commands'].items():
                if cmd['mqtt_topic'] == msg.topic:
                    # 生成响应
                    response = self.generate_response(cmd_name, payload)
                    # 发送响应
                    if response and 'response_topic' in cmd:
                        self.client.publish(cmd['response_topic'], response)
                        logger.info(f"Sent response to topic {cmd['response_topic']}: {response}")
                    break
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def generate_response(self, cmd_name: str, payload: str) -> str:
        """生成响应消息"""
        try:
            cmd_config = self.config['commands'][cmd_name]
            response_start = self.config['mqtt']['response_start_string']
            
            if cmd_name == 'set_pwm':
                # 解析PWM值
                try:
                    value = int(payload.split()[-1])
                    return f"{response_start} PWM {value} OK"
                except:
                    return f"{response_start} PWM ERROR"
                    
            elif cmd_name == 'get_pico_info':
                # 返回设备信息
                return f"{response_start} INFO Device:Pico Status:Running OK"
                
            elif cmd_name == 'led_control':
                # 解析LED状态
                state = payload.split()[-1].lower()
                if state in ['on', 'off']:
                    return f"{response_start} LED {state} OK"
                return f"{response_start} LED ERROR"
                
            return None
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    def on_disconnect(self, client, userdata, rc):
        """断开连接回调函数"""
        self.connected = False
        logger.warning(f"Disconnected from MQTT broker with result code: {rc}")
    
    def close(self):
        """关闭连接"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")

def main():
    """主函数"""
    import signal
    import sys
    
    def signal_handler(sig, frame):
        logger.info("Received signal to stop...")
        responder.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 获取配置文件路径
    config_path = '../config.yaml'
    if not os.path.isfile(config_path):
        config_path = os.path.join(os.path.dirname(__file__), '..', '/', 'config.yaml')
    
    # 创建并启动应答程序
    responder = MQTTResponder(config_path)
    if responder.connect():
        logger.info("MQTT Responder is running. Press CTRL+C to stop.")
        signal.pause()
    else:
        logger.error("Failed to start MQTT Responder")
        sys.exit(1)

if __name__ == "__main__":
    main()
