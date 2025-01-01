# mcp2mqtt: 连接物理世界与AI大模型的桥梁 

[![smithery badge](https://smithery.ai/badge/mcp2mqtt)](https://smithery.ai/server/mcp2mqtt)

[English](README_EN.md) | 简体中文

<div align="center">
    <img src="docs/images/logo.png" alt="mcp2mqtt Logo" width="200"/>
    <p>通过自然语言控制硬件，开启物联网新纪元</p>
</div>

## 系统架构

<div align="center">
    <img src="docs/images/stru_chs.png" alt="系统架构图" width="800"/>
    <p>mcp2mqtt 系统架构图</p>
</div>

## 工作流程

<div align="center">
    <img src="docs/images/workflow_chs.png" alt="工作流程图" width="800"/>
    <p>mcp2mqtt 工作流程图</p>
</div>

## 项目愿景

mcp2mqtt 是一个将物联网设备接入AI大模型的项目，它通过 Model Context Protocol (MCP) 和 MQTT 协议将物理世界与 AI 大模型无缝连接。最终实现：
- 用自然语言控制你的硬件设备
- AI 实时响应并调整物理参数
- 让你的设备具备理解和执行复杂指令的能力
- 通过MQTT协议实现设备间的互联互通

## 主要特性

- **智能MQTT通信**
  - 支持MQTT协议的发布/订阅模式
  - 支持多种MQTT服务器（如Mosquitto、EMQ X等）
  - 支持QoS服务质量保证
  - 支持主题过滤和消息路由
  - 实时状态监控和错误处理

- **MCP 协议集成**
  - 完整支持 Model Context Protocol
  - 支持资源管理和工具调用
  - 灵活的提示词系统
  - 通过MQTT实现命令的发布与响应

## 配置说明

### MQTT配置
```yaml
mqtt:
  broker: "localhost"  # MQTT服务器地址
  port: 1883  # MQTT服务器端口
  client_id: "mcp2mqtt_client"  # MQTT客户端ID
  username: "mqtt_user"  # MQTT用户名
  password: "mqtt_password"  # MQTT密码
  keepalive: 60  # 保持连接时间
  topics:
    command:
      publish: "mcp/command"  # 发送命令的主题
      subscribe: "mcp/response"  # 接收响应的主题
    status:
      publish: "mcp/status"  # 发送状态的主题
      subscribe: "mcp/control"  # 接收控制命令的主题
```

### 命令配置
```yaml
commands:
  set_pwm:
    command: "CMD_PWM {frequency}"
    need_parse: false
    data_type: "ascii"
    prompts:
      - "把PWM调到最大"
      - "把PWM调到最小"
    mqtt_topic: "mcp/pwm"  # MQTT发布主题
    response_topic: "mcp/pwm/response"  # MQTT响应主题
```

## MQTT 命令和响应

### 命令格式

命令使用简单的文本格式：

1. PWM 控制：
   - 命令：`PWM {值}`
   - 示例：
     - `PWM 100`（最大值）
     - `PWM 0`（关闭）
     - `PWM 50`（50%）
   - 响应：`CMD PWM {值} OK`

2. LED 控制：
   - 命令：`LED {状态}`
   - 示例：
     - `LED on`（打开）
     - `LED off`（关闭）
   - 响应：`CMD LED {状态} OK`

3. 设备信息：
   - 命令：`INFO`
   - 响应：`CMD INFO {设备信息}`

### 错误响应

如果发生错误，响应格式将为：
`ERROR: {错误信息}`

## 支持的客户端

mcp2mqtt 支持所有实现了 MCP 协议的客户端，以及支持MQTT协议的物联网设备：

| 客户端类型 | 特性支持 | 说明 |
|--------|----------|------|
| Claude Desktop | 完整支持 | 推荐使用，支持所有 MCP 功能 |
| Continue | 完整支持 | 优秀的开发工具集成 |
| Cline | 资源+工具 | 支持多种 AI 提供商 |
| MQTT设备 | 发布/订阅 | 支持所有MQTT协议的物联网设备 |

## 快速开始

### 1. 安装

### Installing via Smithery

To install mcp2mqtt for Claude Desktop automatically via [Smithery](https://smithery.ai/server/mcp2mqtt):

```bash
npx -y @smithery/cli install mcp2mqtt --client claude
```

#### Windows用户
下载 [install.py](https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install.py) 
```bash
python install.py
```
#### macOS用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install_macos.py

# 运行安装脚本
python3 install_macos.py
```

#### Ubuntu/Raspberry Pi用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install_ubuntu.py

# 运行安装脚本
python3 install_ubuntu.py
```

安装脚本会自动完成以下操作：
- 检查系统环境
- 安装必要的依赖
- 创建默认配置文件
- 配置Claude桌面版（如果已安装）

### 手动分步安装依赖
```bash
windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
MacOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```
主要依赖uv工具，所以当python和uv以及Claude或Cline安装好后就可以了。

### 基本配置
在你的 MCP 客户端（如 Claude Desktop 或 Cline）配置文件中添加以下内容：
注意：如果使用的自动安装那么会自动配置Calude Desktop无需此步。
使用默认配置文件：
```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uvx",
            "args": [
                "mcp2mqtt"
            ]
        }
    }
}
```
> 注意：修改配置后需要重启Cline或者Claude客户端软件
## 配置说明
### 配置文件位置
复制配置文件（`config.yaml`）可以放在位置：
用户主目录（推荐个人使用）
```bash
# Windows系统
C:\Users\用户名\.mcp2mqtt\config.yaml

# macOS系统
/Users/用户名/.mcp2mqtt/config.yaml

# Linux系统
/home/用户名/.mcp2mqtt/config.yaml
```
- 适用场景：个人配置
- 需要创建 `.mcp2mqtt` 目录：
  ```bash
  # Windows系统（在命令提示符中）
  mkdir "%USERPROFILE%\.mcp2mqtt"
  
  # macOS/Linux系统
  mkdir -p ~/.mcp2mqtt
  ```
 
指定配置文件：
比如指定加载Pico配置文件：Pico_config.yaml
```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uvx",
            "args": [
                "mcp2mqtt",
                "--config",
                "Pico"  //指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```
为了能使用多个mqtt，我们可以新增多个mcp2mqtt的服务 指定不同的配置文件名即可。
如果要接入多个设备，如有要连接第二个设备：
指定加载Pico2配置文件：Pico2_config.yaml
```json
{
    "mcpServers": {
        "mcp2mqtt2": {
            "command": "uvx",
            "args": [
                "mcp2mqtt",
                "--config",
                "Pico2"  //指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```

### 硬件连接
1. 将你的设备通过网络连接到mqtt服务器
2. 也可以用tests目录下的responder.py来模拟设备

## 运行测试

### 启动设备模拟器

项目在 `tests` 目录中包含了一个设备模拟器。它可以模拟一个硬件设备，能够：
- 响应 PWM 控制命令
- 提供设备信息
- 控制 LED 状态

启动模拟器：
```bash
python tests/responder.py
```

你应该能看到模拟器正在运行并已连接到 MQTT 服务器的输出信息。

### 启动客户端Claude 桌面版或Cline
<div align="center">
    <img src="docs/images/test_output.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>

### 从源码快速开始
1. 从源码安装
```bash
# 通过源码安装：
git clone https://github.com/mcp2everything/mcp2mqtt.git
cd mcp2mqtt

# 创建虚拟环境
uv venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 安装开发依赖
uv pip install --editable .
```

### MCP客户端配置
在使用支持MCP协议的客户端（如Claude Desktop或Cline）时，需要在客户端的配置文件中添加以下内容：
直接自动安装的配置方式
源码开发的配置方式
#### 使用默认演示参数：
```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uv",
            "args": [
                "--directory",
                "你的实际路径/mcp2mqtt",  // 例如: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2mqtt"
                "run",
                "mcp2mqtt"
            ]
        }
    }
}
```
#### 指定参数文件名
```json
{
    "mcpServers": {
        "mcp2mqtt": {
            "command": "uv",
            "args": [
                "--directory",
                "你的实际路径/mcp2mqtt",  // 例如: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2mqtt"
                "run",
                "mcp2mqtt",
                "--config", // 可选参数，指定配置文件名
                "Pico"  // 可选参数，指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```
<div align="center">
    <img src="docs/images/config.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>
### 配置文件位置
配置文件（`config.yaml`）可以放在不同位置，程序会按以下顺序查找：
#### 1. 当前工作目录（适合开发测试）
- 路径：`./config.yaml`
- 示例：如果你在 `C:\Projects` 运行程序，它会查找 `C:\Projects\config.yaml`
- 适用场景：开发和测试
- 不需要特殊权限

#### 2. 用户主目录（推荐个人使用）
```bash
# Windows系统
C:\Users\用户名\.mcp2mqtt\config.yaml

# macOS系统
/Users/用户名/.mcp2mqtt/config.yaml

# Linux系统
/home/用户名/.mcp2mqtt/config.yaml
```
- 适用场景：个人配置
- 需要创建 `.mcp2mqtt` 目录：
  ```bash
  # Windows系统（在命令提示符中）
  mkdir "%USERPROFILE%\.mcp2mqtt"
  
  # macOS/Linux系统
  mkdir -p ~/.mcp2mqtt
  ```

#### 3. 系统级配置（适合多用户环境）
```bash
# Windows系统（需要管理员权限）
C:\ProgramData\mcp2mqtt\config.yaml

# macOS/Linux系统（需要root权限）
/etc/mcp2mqtt/config.yaml
```
- 适用场景：多用户共享配置
- 创建目录并设置权限：
  ```bash
  # Windows系统（以管理员身份运行）
  mkdir "C:\ProgramData\mcp2mqtt"
  
  # macOS/Linux系统（以root身份运行）
  sudo mkdir -p /etc/mcp2mqtt
  sudo chown root:root /etc/mcp2mqtt
  sudo chmod 755 /etc/mcp2mqtt
  ```

程序会按照上述顺序查找配置文件，使用找到的第一个有效配置文件。根据你的需求选择合适的位置：
- 开发测试：使用当前目录
- 个人使用：建议使用用户主目录（推荐）
- 多用户环境：使用系统级配置（ProgramData或/etc）

3. 运行服务器：
```bash
# 确保已激活虚拟环境
.venv\Scripts\activate

# 运行服务器（使用默认配置config.yaml 案例中用的LOOP_BACK 模拟串口，无需真实串口和串口设备）
uv run src/mcp2mqtt/server.py
或
uv run mcp2mqtt
# 运行服务器（使用指定配置Pico_config.yaml）
uv run src/mcp2mqtt/server.py --config Pico
或
uv run mcp2mqtt --config Pico
```


## 文档

- [安装指南](./docs/zh/installation.md)
- [API文档](./docs/zh/api.md)
- [配置说明](./docs/zh/configuration.md)