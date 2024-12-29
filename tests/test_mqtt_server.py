#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MQTT测试服务器
用于测试mcp2mqtt的MQTT功能
"""

import paho.mqtt.client as mqtt
import time
import json
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

class MQTTTestServer:
    """MQTT测试服务器类"""
    
    def __init__(self, config_path: str = "../config.yaml"):
        """初始化MQTT测试服务器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)
        self.client = mqtt.Client(client_id=f"{self.config['mqtt']['client_id']}_server")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
        # 存储最后收到的消息
        self.last_message = {
            'topic': None,
            'payload': None,
            'timestamp': None
        }
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def connect(self) -> bool:
        """连接到MQTT服务器
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 如果配置了用户名和密码，则设置认证
            if self.config['mqtt']['username']:
                self.client.username_pw_set(
                    self.config['mqtt']['username'],
                    self.config['mqtt']['password']
                )
            
            # 连接到服务器
            self.client.connect(
                self.config['mqtt']['broker'],
                self.config['mqtt']['port'],
                self.config['mqtt']['keepalive']
            )
            
            # 启动循环
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
            
            # 订阅所有命令的响应主题
            topics = []
            for cmd_name, cmd in self.config['commands'].items():
                if 'mqtt_topic' in cmd:
                    topics.append(cmd['mqtt_topic'])
                if 'response_topic' in cmd:
                    topics.append(cmd['response_topic'])
            
            for topic in topics:
                self.client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")
    
    def on_message(self, client, userdata, msg):
        """消息回调函数"""
        try:
            payload = msg.payload.decode()
            logger.info(f"Received message on topic {msg.topic}: {payload}")
            
            # 存储接收到的消息
            self.last_message = {
                'topic': msg.topic,
                'payload': payload,
                'timestamp': time.time()
            }
            
            # 发送响应消息
            response_topic = None
            if msg.topic.endswith('/command'):
                response_topic = msg.topic.replace('/command', '/response')
            elif msg.topic.endswith('/status'):
                response_topic = msg.topic.replace('/status', '/control')
            
            if response_topic:
                response = {
                    'original_topic': msg.topic,
                    'original_message': payload,
                    'status': 'received',
                    'timestamp': time.time()
                }
                self.client.publish(response_topic, json.dumps(response))
                logger.info(f"Sent response to topic {response_topic}")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """断开连接回调函数"""
        self.connected = False
        logger.warning(f"Disconnected from MQTT broker with result code: {rc}")
    
    def publish_test_message(self, topic: str, message: str):
        """发布测试消息
        
        Args:
            topic: 主题
            message: 消息内容
        """
        if not self.connected:
            logger.error("Not connected to MQTT broker")
            return False
        
        try:
            result = self.client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published test message to {topic}: {message}")
                return True
            else:
                logger.error(f"Failed to publish message: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")

def main():
    """主函数"""
    # 获取配置文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "..", "config.yaml")
    
    # 创建测试服务器实例
    server = MQTTTestServer(config_path)
    
    try:
        # 连接到MQTT服务器
        if not server.connect():
            logger.error("Failed to connect to MQTT broker")
            return
        
        # 发送测试消息到每个命令的主题
        test_messages = [
            {
                'topic': 'mcp2mqtt/pwm',
                'message': 'PWM 100'  # 设置PWM到最大
            },
            {
                'topic': 'mcp2mqtt/pwm',
                'message': 'PWM 0'    # 关闭PWM
            },
            {
                'topic': 'mcp2mqtt/info',
                'message': 'INFO'     # 查询信息
            },
            {
                'topic': 'mcp2mqtt/led',
                'message': 'LED on'   # 打开LED
            },
            {
                'topic': 'mcp2mqtt/led',
                'message': 'LED off'  # 关闭LED
            }
        ]
        
        # 每隔5秒发送一条测试消息
        for msg in test_messages:
            server.publish_test_message(msg['topic'], msg['message'])
            logger.info(f"Published test message: {msg['message']} to topic: {msg['topic']}")
            time.sleep(5)
        
        # 保持运行一段时间以接收响应
        logger.info("Waiting for responses...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        server.close()

if __name__ == "__main__":
    main()
