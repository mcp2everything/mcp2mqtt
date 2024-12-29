# 测试指南

本指南说明如何使用模拟设备测试 MCP2MQTT 服务。

## 前提条件

- Python >= 3.11
- UV 包管理器
- MQTT 服务器（默认：broker.emqx.io）
- MCP 客户端（如 Claude）

## 设置

1. 安装依赖：
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. 在 `config.yaml` 中配置 MQTT 设置：
   ```yaml
   mqtt:
     broker: "broker.emqx.io"  # 使用默认或你自己的服务器
     port: 1883
     client_id: "mcp2mqtt_client"
   ```

## 运行测试

### 1. 启动设备模拟器

项目在 `tests` 目录中包含了一个设备模拟器。它可以模拟一个硬件设备，能够：
- 响应 PWM 控制命令
- 提供设备信息
- 控制 LED 状态

启动模拟器：
```bash
python tests/responder.py
```

你应该能看到模拟器正在运行并已连接到 MQTT 服务器的输出信息。

### 2. 启动 MCP2MQTT 服务

在新的终端中：
```bash
uv run mcp2mqtt
```

服务将：
- 加载配置
- 连接到 MQTT 服务器
- 注册可用工具
- 等待 MCP 命令

### 3. 配置 MCP 客户端

将 MCP2MQTT 服务添加到你的 MCP 客户端（如 Claude）：
- 服务器名称：mcp2mqtt
- 版本：0.1.0
- 工具：
  - set_pwm
  - get_pico_info
  - led_control

### 4. 测试命令

尝试这些示例命令：

1. 设置 PWM 频率：
   ```
   set_pwm frequency=50
   ```
   预期响应：`CMD PWM 50 OK`

2. 获取设备信息：
   ```
   get_pico_info
   ```
   预期响应：`CMD INFO Device:Pico Status:Running OK`

3. 控制 LED：
   ```
   led_control state=on
   ```
   预期响应：`CMD LED on OK`

## 故障排除

1. 连接问题：
   - 检查 MQTT 服务器地址和端口
   - 验证网络连接
   - 检查防火墙设置

2. 命令失败：
   - 确认模拟器正在运行
   - 检查配置中的 MQTT 主题是否匹配
   - 查看服务日志中的错误

3. 响应超时：
   - 在配置中增加超时值
   - 检查网络延迟
   - 验证服务器 QoS 设置

## 下一步

在使用模拟器测试后，你可以：
1. 连接真实的硬件设备
2. 自定义 MQTT 主题和消息格式
3. 添加新的工具和命令
4. 实现额外的设备功能
