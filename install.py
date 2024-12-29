import os
import sys
import platform
import subprocess
import json
import shutil
from pathlib import Path

def check_os():
    """检查操作系统"""
    system = platform.system()
    if system != "Windows":
        print(f"⚠️ 警告: 当前操作系统为 {system}，本脚本主要针对 Windows 系统优化")
        if not input("是否继续安装? (y/n): ").lower().startswith('y'):
            sys.exit(1)
    return system

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ 错误: Python版本必须大于等于3.11，当前版本为 {sys.version.split()[0]}")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version.split()[0]}")

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
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
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
  port: COM1  # 请修改为实际的COM端口号
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
        print("⚠️ 请修改配置文件中的COM端口号为实际值")
    else:
        print(f"ℹ️ 配置文件已存在: {config_file}")

def check_and_configure_claude():
    """检查和配置Claude桌面客户端"""
    claude_config_dir = Path.home() / "AppData/Roaming/Claude"
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
    vscode_path = Path.home() / "AppData/Local/Programs/Microsoft VS Code"
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

def main():
    print("=== mcp2mqtt 安装程序 ===")
    
    # 1. 检查操作系统
    system = check_os()
    print(f"✅ 操作系统: {system}")
    
    # 2. 检查Python版本
    check_python_version()
    
    # 3. 检查和安装uv/uvx
    check_and_install_uv()
    
    # 4. 创建配置文件
    create_config()
    
    # 5. 检查和配置Claude
    check_and_configure_claude()
    
    # 6. 检查VSCode
    check_vscode()
    
    print("\n✨ 安装完成！")
    print("📝 请确保：")
    print("1. 修改配置文件中的COM端口号")
    print("2. 检查Claude或VSCode的MCP服务器配置")
    print("3. 重启Claude或VSCode以使配置生效")
    print("\n💡 提示：mcp2mqtt 将在首次运行时自动下载")

if __name__ == "__main__":
    main()
