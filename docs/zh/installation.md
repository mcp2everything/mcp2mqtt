# mcp2mqtt 安装指南

## 环境要求

- Python 3.11 或更高版本
- uv 包管理器
- 串口设备（如Arduino、树莓派Pico等）

### 安装

#### Windows用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2mqtt/main/install.py

# 运行安装脚本
python install.py
```

#### MacOS用户
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
- ✅ 检查系统环境
- ✅ 安装必要的依赖
- ✅ 创建默认配置文件
- ✅ 配置Claude桌面版（如果已安装）
- ✅ 检查串口设备


## 手动安装

如果你不想使用安装脚本，也可以手动安装：

### 方式一：通过 pip 安装

1. 确保已安装 Python 3.11+
2. 安装 uv 包管理器：
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. 创建虚拟环境：
   ```bash
   uv venv .venv
   ```

4. 激活虚拟环境：
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

5. 安装 mcp2mqtt：
   ```bash
   uv pip install mcp2mqtt
   ```

### 方式二：通过源码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/mcp2everything/mcp2mqtt.git
   cd mcp2mqtt
   ```

2. 创建虚拟环境：
   ```bash
   uv venv .venv
   ```

3. 激活虚拟环境：
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. 安装开发依赖：
   ```bash
   uv pip install --editable .
   ```

## 配置说明

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

### 串口配置

在 `config.yaml` 文件中配置串口参数：

```yaml
serial:
  port: COM11  # Windows系统示例，Linux下可能是 /dev/ttyUSB0
  baud_rate: 115200  # 波特率
  timeout: 1.0  # 串口超时时间（秒）
  read_timeout: 0.5  # 读取超时时间（秒）
```

如果不指定 `port`，程序会自动搜索可用的串口设备。

### 命令配置

在 `config.yaml` 中添加自定义命令：

```yaml
commands:
  # PWM控制命令示例
  set_pwm:
    command: "PWM {frequency}\n"  # 实际发送的命令格式
    need_parse: false  # 不需要解析响应
    prompts:  # 提示语列表
      - "把PWM调到{value}"
      - "关闭PWM"

  # LED控制命令示例
  led_control:
    command: "LED {state}\n"  # state可以是on/off或其他值
    need_parse: false
    prompts:
      - "打开LED"
      - "关闭LED"
      - "设置LED状态为{state}"

  # 带响应解析的命令示例
  get_sensor:
    command: "GET_SENSOR\n"
    need_parse: true  # 需要解析响应
    prompts:
      - "读取传感器数据"
```

### 响应解析说明

1. 简单响应（`need_parse: false`）：
   - 设备返回 "OK" 开头的消息表示成功
   - 其他响应将被视为错误

2. 需要解析的响应（`need_parse: true`）：
   - 完整响应将在 `result.raw` 字段中返回
   - 可以在应用层进行进一步解析

响应示例：
```python
# 简单响应
{"status": "success"}

# 需要解析的响应
{"status": "success", "result": {"raw": "OK TEMP=25.5,HUMIDITY=60%"}}
```

### MCP客户端配置

在使用支持MCP协议的客户端（如Claude Desktop或Cline）时，需要在客户端的配置文件中添加以下内容：
直接自动安装的配置方式
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

源码开发的配置方式
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

<div align="center">
    <img src="../images/client_config.png" alt="客户端配置示例" width="600"/>
    <p>在 Claude Desktop 中的配置示例</p>
</div>

<div align="center">
    <img src="../images/cline_config.png" alt="Cline配置示例" width="600"/>
    <p>在 Cline 中的配置示例</p>
</div>

> **注意事项：**
> 1. 路径必须使用完整的绝对路径
> 2. 使用正斜杠（/）或双反斜杠（\\）作为路径分隔符
> 3. 确保路径指向实际的项目安装目录

## 源码开发步骤

1. 克隆项目代码：

```bash
# 克隆代码库
git clone https://github.com/mcp2everything/mcp2mqtt.git
```

2. 创建并激活虚拟环境：

```bash
# 进入项目目录
cd mcp2mqtt

# 使用 uv 创建虚拟环境并安装依赖
uv venv .venv
.venv\Scripts\activate

# 安装依赖
uv pip install -r requirements.txt
```

> **注意：** 项目即将发布到PyPI，届时可以直接通过pip安装。

## 运行服务器

```bash
# 确保在项目根目录下
cd mcp2mqtt

# 激活虚拟环境（如果尚未激活）
.venv\Scripts\activate

# 运行服务器
uv run src/mcp2mqtt/server.py
```


## 故障排除

1. 串口连接问题：
   - 确认设备已正确连接
   - 检查串口号是否正确
   - 验证波特率设置
   - 检查串口权限（Linux系统）

2. 命令超时：
   - 检查 `timeout` 和 `read_timeout` 设置
   - 确认设备响应时间

## 测试

运行测试用例：

```bash
# 激活虚拟环境（如果尚未激活）
.venv\Scripts\activate

# 运行测试
uv run pytest tests/