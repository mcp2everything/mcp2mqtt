import os
import sys
import platform
import subprocess
import json
from pathlib import Path

def check_os():
    """检查操作系统"""
    system = platform.system()
    if system != "Darwin":
        print(f"❌ 错误: 此脚本仅支持 MacOS 系统，当前系统为 {system}")
        sys.exit(1)
    print(f"✅ 操作系统: MacOS {platform.mac_ver()[0]}")
    return system

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ 错误: Python版本必须大于等于3.11，当前版本为 {sys.version.split()[0]}")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version.split()[0]}")

def check_homebrew():
    """检查是否安装了Homebrew"""
    try:
        subprocess.run(["brew", "--version"], capture_output=True)
        print("✅ Homebrew 已安装")
    except FileNotFoundError:
        print("❌ 请先安装 Homebrew")
        print("💡 安装命令: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        sys.exit(1)

def check_and_install_uv():
    """检查和安装uv"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True)
        print("✅ uv 已安装")
        # 检查uvx是否可用
        try:
            subprocess.run(["uvx", "--version"], capture_output=True)
            print("✅ uvx 已安装")
        except FileNotFoundError:
            print("⚙️ 正在配置 uvx...")
            subprocess.run([sys.executable, "-m", "uv", "pip", "install", "--system", "uv"], check=True)
            print("✅ uvx 配置成功")
    except FileNotFoundError:
        print("⚙️ 正在安装 uv...")
        try:
            # 使用 Homebrew 安装 uv
            subprocess.run(["brew", "install", "astral-sh/tap/uv"], check=True)
            print("✅ uv 安装成功")
            # 安装完uv后配置uvx
            print("⚙️ 正在配置 uvx...")
            subprocess.run([sys.executable, "-m", "uv", "pip", "install", "--system", "uv"], check=True)
            print("✅ uvx 配置成功")
        except subprocess.CalledProcessError:
            print("❌ uv 安装失败")
            sys.exit(1)

def create_config():
    """创建默认配置文件"""
    config_dir = Path.home() / ".mcp2mqtt"
    config_file = config_dir / "config.yaml"
    
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
        print(f"✅ 创建配置目录: {config_dir}")

    if not config_file.exists():
        config_content = """serial:
  port: /dev/tty.usbserial-*  # 串口设备名，支持通配符
  baud_rate: 115200

commands:
  set_pwm:
    command: "PWM {frequency}\\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
      - "Set PWM to {value}%"
"""
        config_file.write_text(config_content, encoding='utf-8')
        print(f"✅ 创建配置文件: {config_file}")
        print("⚠️ 请修改配置文件中的串口设备名为实际值")
    else:
        print(f"ℹ️ 配置文件已存在: {config_file}")

def check_and_configure_claude():
    """检查和配置Claude桌面客户端"""
    claude_config_dir = Path.home() / "Library/Application Support/Claude"
    if not claude_config_dir.exists():
        print(f"ℹ️ 未检测到Claude桌面客户端目录: {claude_config_dir}")
        return

    config_file = claude_config_dir / "claude_desktop_config.json"
    if not config_file.exists():
        print(f"ℹ️ Claude配置文件不存在: {config_file}")
        return

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("❌ Claude配置文件格式错误")
        return

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    if "mcp2mqtt" not in config["mcpServers"]:
        config["mcpServers"]["mcp2mqtt"] = {
            "command": "uvx",
            "args": ["mcp2mqtt"]
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print("✅ 已添加mcp2mqtt配置到Claude")
    else:
        print("ℹ️ Claude已配置mcp2mqtt")

def check_vscode():
    """检查VSCode安装"""
    vscode_path = Path("/Applications/Visual Studio Code.app")
    if vscode_path.exists():
        print("""
ℹ️ 检测到VSCode安装
请在VSCode中添加以下MCP服务器配置：
{
    "mcp2mqtt": {
        "command": "uvx",
        "args": ["mcp2mqtt"]
    }
}
""")
    else:
        print("ℹ️ 未检测到VSCode安装")

def check_serial_devices():
    """检查串口设备"""
    devices = list(Path("/dev").glob("tty.usbserial-*"))
    if devices:
        print("\n检测到以下串口设备：")
        for device in devices:
            print(f"- {device}")
        print("💡 请在配置文件中使用正确的设备名")
    else:
        print("\n⚠️ 未检测到串口设备，请确保：")
        print("1. 设备已正确连接")
        print("2. 已安装串口驱动")
        print("💡 常用串口芯片驱动：")
        print("- CH340/CH341: https://www.wch.cn/downloads/CH341SER_MAC_ZIP.html")
        print("- CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers")
        print("- FTDI: https://ftdichip.com/drivers/vcp-drivers/")

def main():
    print("=== mcp2mqtt MacOS 安装程序 ===")
    
    # 1. 检查操作系统
    system = check_os()
    
    # 2. 检查Python版本
    check_python_version()
    
    # 3. 检查Homebrew
    check_homebrew()
    
    # 4. 检查和安装uv/uvx
    check_and_install_uv()
    
    # 5. 创建配置文件
    create_config()
    
    # 6. 检查和配置Claude
    check_and_configure_claude()
    
    # 7. 检查VSCode
    check_vscode()
    
    # 8. 检查串口设备
    check_serial_devices()
    
    print("\n✨ 安装完成！")
    print("📝 请确保：")
    print("1. 修改配置文件中的串口设备名")
    print("2. 检查Claude或VSCode的MCP服务器配置")
    print("3. 重启Claude或VSCode以使配置生效")
    print("\n💡 提示：")
    print("- mcp2mqtt 将在首次运行时自动下载")
    print("- 串口设备名通常为 /dev/tty.usbserial-* 格式")
    print("- 如遇到权限问题，请确保当前用户有串口设备的读写权限")

if __name__ == "__main__":
    main()
