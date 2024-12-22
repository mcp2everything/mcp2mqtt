# MCP2Serial: 连接物理世界与AI大模型的桥梁 

[English](README_EN.md) | 简体中文

<div align="center">
    <img src="docs/images/logo.png" alt="MCP2Serial Logo" width="200"/>
    <p>通过自然语言控制硬件，开启物联网新纪元</p>
</div>

## 系统架构

<div align="center">
    <img src="docs/images/stru_chs.png" alt="系统架构图" width="800"/>
    <p>MCP2Serial 系统架构图</p>
</div>

## 工作流程

<div align="center">
    <img src="docs/images/workflow_chs.png" alt="工作流程图" width="800"/>
    <p>MCP2Serial 工作流程图</p>
</div>

## 项目愿景

MCP2Serial 将串口设备接入AI大模型的项目，它通过 Model Context Protocol (MCP) 将物理世界与 AI 大模型无缝连接。最终实现：
- 用自然语言控制你的硬件设备
- AI 实时响应并调整物理参数
- 让你的设备具备理解和执行复杂指令的能力

## 主要特性

- **智能串口通信**
  - 自动检测和配置串口设备 用户也可指定串口号
  - 支持多种波特率（默认 115200）
  - 实时状态监控和错误处理

- **MCP 协议集成**
  - 完整支持 Model Context Protocol
  - 支持资源管理和工具调用
  - 灵活的提示词系统

## 支持的客户端

MCP2Serial 支持所有实现了 MCP 协议的客户端，包括：

| 客户端 | 特性支持 | 说明 |
|--------|----------|------|
| Claude Desktop | 完整支持 | 推荐使用，支持所有 MCP 功能 |
| Continue | 完整支持 | 优秀的开发工具集成 |
| Cline | 资源+工具 | 支持多种 AI 提供商 |
| Zed | 基础支持 | 支持提示词命令 |
| Sourcegraph Cody | 资源支持 | 通过 OpenCTX 集成 |
| Firebase Genkit | 部分支持 | 支持资源列表和工具 |

## 支持的 AI 模型

得益于灵活的客户端支持，MCP2Serial 可以与多种 AI 模型协同工作：

### 云端模型
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- Google Cloud Vertex AI

### 本地模型
- LM Studio 支持的所有模型
- Ollama 支持的所有模型
- 任何兼容 OpenAI API 的模型

### 准备
Python3.11 或更高版本
Claude Desktop 或 Cline


## 快速开始

### 1. 安装

#### Windows用户
下载 [install.py](https://raw.githubusercontent.com/mcp2everything/mcp2tcp/main/install.py) 
```bash
python install.py
```
#### macOS用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2tcp/main/install_macos.py

# 运行安装脚本
python3 install_macos.py
```

#### Ubuntu/Raspberry Pi用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2tcp/main/install_ubuntu.py

# 运行安装脚本
python3 install_ubuntu.py
```

安装脚本会自动完成以下操作：
- ✅ 检查系统环境
- ✅ 安装必要的依赖
- ✅ 创建默认配置文件
- ✅ 配置Claude桌面版（如果已安装）
- ✅ 检查串口设备

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
        "mcp2tcp": {
            "command": "uvx",
            "args": [
                "mcp2tcp"
            ]
        }
    }
}
```
> 注意：修改配置后需要重启Cline或者Claude客户端软件

配置串口和命令：
注意下面的配置默认为COM11 需要根据实际进行修改
```yaml
# config.yaml
serial:
  port: COM11  # 或自动检测
  baud_rate: 115200  # 可选，默认 115200
  timeout: 1.0  # 可选，默认 1.0
  read_timeout: 1.0  # 读取超时时间，1秒内不应答则报错
  response_start_string: OK  # 可选，串口应答的开始字符串，默认为OK

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
```
## 配置说明
### 配置文件位置

配置文件（`config.yaml`）可以放在位置：
用户主目录（推荐个人使用）
```bash
# Windows系统
C:\Users\用户名\.mcp2tcp\config.yaml

# macOS系统
/Users/用户名/.mcp2tcp/config.yaml

# Linux系统
/home/用户名/.mcp2tcp/config.yaml
```
- 适用场景：个人配置
- 需要创建 `.mcp2tcp` 目录：
  ```bash
  # Windows系统（在命令提示符中）
  mkdir "%USERPROFILE%\.mcp2tcp"
  
  # macOS/Linux系统
  mkdir -p ~/.mcp2tcp
  ```

### 串口配置 命令配置进阶
在 `config.yaml` 中添加自定义命令：


使用真实串口
```yaml
# config.yaml
serial:
  port: COM11  # 或自动检测
  baud_rate: 115200  # 可选，默认 115200
  timeout: 1.0  # 可选，默认 1.0
  read_timeout: 1.0  # 读取超时时间，1秒内不应答则报错
  response_start_string: OK  # 可选，串口应答的开始字符串，默认为OK

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
```

使用模拟串口
```yaml
serial:
  # 串口配置
  port: LOOP_BACK  # 可选，如果不指定则自动查找。设置为LOOP_BACK时启用回环模式，发送什么就接收什么
  baud_rate: 115200  # 可选，默认 115200
  timeout: 1.0  # 可选，默认 1.0
  read_timeout: 1.0  # 读取超时时间，1秒内不应答则报错
  response_start_string: CMD  # 可选，串口应答的开始字符串，默认为OK

commands:
  # PWM控制命令
  set_pwm:
    command: "CMD_PWM {frequency}"  # 实际发送的命令格式，server会自动添加\r\n
    need_parse: false  # 不需要解析响应内容
    prompts:
      - "把PWM调到最大"
      - "把PWM调到最小"
      - "请将PWM设置为{value}"
      - "关闭PWM"
      - "把PWM调到一半"
```

指定配置文件：
比如指定加载Pico配置文件：Pico_config.yaml
```json
{
    "mcpServers": {
        "mcp2tcp": {
            "command": "uvx",
            "args": [
                "mcp2tcp",
                "--config",
                "Pico"  //指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```
为了能使用多个串口，我们可以新增多个mcp2serial的服务 指定不同的配置文件名即可。
如果要接入多个设备，如有要连接第二个设备：
指定加载Pico2配置文件：Pico2_config.yaml
```json
{
    "mcpServers": {
        "mcp2serial2": {
            "command": "uvx",
            "args": [
                "mcp2tcp",
                "--config",
                "Pico2"  //指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```

### 硬件连接

1. 将你的设备通过USB连接到电脑
2. 打开设备管理器，记下设备的COM端口号
3. 在`config.yaml`中配置正确的端口号和波特率

<div align="center">
    <img src="docs/images/conn
ect.jpg" alt="硬件连接示例" width="600"/>
    <p>硬件连接和COM端口配置</p>
</div>

### 启动客户端Claude 桌面版或Cline

<div align="center">
    <img src="docs/images/pwm.png" alt="Cline Configuration Example" width="600"/>
    <p> Example in Claude</p>
</div>
<div align="center">
    <img src="docs/images/test_output.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>

### 硬件编程
firmware可以在项目仓库中下载，目前演示的是Pico的micropython代码案例。另存到Pico开发板运行即可。

### 从源码快速开始
1. 从源码安装
```bash
# 通过源码安装：
git clone https://github.com/mcp2everything/mcp2tcp.git
cd mcp2tcp

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

2. 配置串口和命令：
默认不使用真实串口 用模拟串口来演示
如果你的电脑没有串口或者目前没有串口可用
可以将port参数设置为LOOP_BACK，这样就可以在命令行直接发送命令了
但同时请修改应答OK的命令的起始符需要和发送的命令一样。
比如发送LED_ON
那么应答起始符也是LED_ON
```yaml
serial:
  # 串口配置
  port: LOOP_BACK  # 可选，如果不指定则自动查找。设置为LOOP_BACK时启用回环模式，发送什么就接收什么
  baud_rate: 115200  # 可选，默认 115200
  timeout: 1.0  # 可选，默认 1.0
  read_timeout: 1.0  # 读取超时时间，1秒内不应答则报错
  response_start_string: CMD  # 可选，串口应答的开始字符串，默认为OK

commands:
  # PWM控制命令
  set_pwm:
    command: "CMD_PWM {frequency}"  # 实际发送的命令格式，server会自动添加\r\n
    need_parse: false  # 不需要解析响应内容
    prompts:
      - "把PWM调到最大"
      - "把PWM调到最小"
      - "请将PWM设置为{value}"
      - "关闭PWM"
      - "把PWM调到一半"
```

如果使用真实串口
```yaml
# config.yaml
serial:
  port: COM11  # 或自动检测
  baud_rate: 115200  # 可选，默认 115200
  timeout: 1.0  # 可选，默认 1.0
  read_timeout: 1.0  # 读取超时时间，1秒内不应答则报错
  response_start_string: OK  # 可选，串口应答的开始字符串，默认为OK

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
```



### MCP客户端配置

在使用支持MCP协议的客户端（如Claude Desktop或Cline）时，需要在客户端的配置文件中添加以下内容：
直接自动安装的配置方式
源码开发的配置方式
#### 使用默认演示参数：
```json
{
    "mcpServers": {
        "mcp2tcp": {
            "command": "uv",
            "args": [
                "--directory",
                "你的实际路径/mcp2tcp",  // 例如: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2tcp"
                "run",
                "mcp2tcp"
            ]
        }
    }
}
```
#### 指定参数文件名
```json
{
    "mcpServers": {
        "mcp2tcp": {
            "command": "uv",
            "args": [
                "--directory",
                "你的实际路径/mcp2tcp",  // 例如: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2tcp"
                "run",
                "mcp2tcp",
                "--config", // 可选参数，指定配置文件名
                "Pico"  // 可选参数，指定配置文件名，不需要添加_config.yaml后缀
            ]
        }
    }
}
```
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
C:\Users\用户名\.mcp2tcp\config.yaml

# macOS系统
/Users/用户名/.mcp2tcp/config.yaml

# Linux系统
/home/用户名/.mcp2tcp/config.yaml
```
- 适用场景：个人配置
- 需要创建 `.mcp2tcp` 目录：
  ```bash
  # Windows系统（在命令提示符中）
  mkdir "%USERPROFILE%\.mcp2tcp"
  
  # macOS/Linux系统
  mkdir -p ~/.mcp2tcp
  ```

#### 3. 系统级配置（适合多用户环境）
```bash
# Windows系统（需要管理员权限）
C:\ProgramData\mcp2tcp\config.yaml

# macOS/Linux系统（需要root权限）
/etc/mcp2tcp/config.yaml
```
- 适用场景：多用户共享配置
- 创建目录并设置权限：
  ```bash
  # Windows系统（以管理员身份运行）
  mkdir "C:\ProgramData\mcp2tcp"
  
  # macOS/Linux系统（以root身份运行）
  sudo mkdir -p /etc/mcp2tcp
  sudo chown root:root /etc/mcp2tcp
  sudo chmod 755 /etc/mcp2tcp
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
uv run src/mcp2tcp/server.py
或
uv run mcp2tcp
# 运行服务器（使用指定配置Pico_config.yaml）
uv run src/mcp2tcp/server.py --config Pico
或
uv run mcp2tcp --config Pico
```


## 文档

- [安装指南](./docs/zh/installation.md)
- [API文档](./docs/zh/api.md)
- [配置说明](./docs/zh/configuration.md)


## 应用场景

1. **智能家居自动化**
   - 通过自然语言控制灯光、风扇等设备
   - AI 根据环境自动调节设备参数

2. **工业自动化**
   - 智能控制生产线设备
   - 实时监控和调整工艺参数

3. **教育和研究**
   - 物联网教学演示
   - 硬件控制实验平台

4. **原型开发**
   - 快速验证硬件控制方案
   - 简化开发流程

## 🚀 项目发展规划

### 第一阶段：协议扩展
- **工业协议支持**
  - MODBUS RTU/TCP
  - OPC UA
  - MQTT
  - CoAP
  - TCP/IP Socket
  
- **硬件接口扩展**
  - I2C
  - SPI
  - CAN
  - 1-Wire
  - GPIO

### 第二阶段：MCP2Anything 平台
- **统一集成平台**
  - 可视化配置界面
  - 一键启用各类协议
  - 实时监控仪表盘
  - 设备管理系统

- **智能功能**
  - 协议自动检测
  - 设备自动发现
  - 参数智能优化
  - 异常预警系统

### 第三阶段：生态系统建设
- **插件市场**
  - 协议插件
  - 设备驱动
  - 自定义功能模块
  - 社区贡献集成

- **云服务集成**
  - 设备云管理
  - 远程控制
  - 数据分析
  - AI 训练平台

### 第四阶段：行业解决方案
- **垂直领域适配**
  - 工业自动化
  - 智能建筑
  - 农业物联网
  - 智慧城市

- **定制化服务**
  - 行业协议适配
  - 专业技术支持
  - 解决方案咨询
  - 培训服务

## 🔮 愿景展望

MCP2Serial 正在开启物联网的新篇章：

- **协议统一**: 通过 MCP2Anything 平台实现全协议支持
- **即插即用**: 一键配置，自动发现，零门槛使用
- **AI 赋能**: 深度集成 AI 能力，实现智能决策
- **开放生态**: 建立活跃的开发者社区和插件市场

## 未来展望

MCP2Serial 正在开启物联网的新篇章：

- **多协议支持**: 计划支持更多通信协议（I2C、SPI等）
- **设备生态**: 建立开放的设备支持生态系统
- **AI 增强**: 集成更多 AI 能力，提供更智能的控制逻辑
- **可视化**: 开发直观的监控和配置界面

## 相关资源

- [MCP 协议规范](https://modelcontextprotocol.io/)
- [项目文档](docs/)
- [示例代码](examples/)
- [常见问题](docs/FAQ.md)

## 参与贡献

我们欢迎各种形式的贡献，无论是新功能、文档改进还是问题报告。查看 [贡献指南](CONTRIBUTING.md) 了解更多信息。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
