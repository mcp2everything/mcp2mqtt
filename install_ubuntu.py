#!/usr/bin/env python3
# ====================================================
# Project: MCP2Serial
# Description: Installation script for Ubuntu/Raspberry Pi
# Repository: https://github.com/mcp2everything/mcp2tcp.git
# License: MIT License
# Author: mcp2everything
# Copyright (c) 2024 mcp2everything
# ====================================================

import os
import sys
import json
import subprocess
from pathlib import Path
import shutil

def get_uv_path():
    """Get uv executable path."""
    # 检查是否已安装uv
    try:
        result = subprocess.run(['which', 'uv'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None

def install_uv():
    """Install uv package manager."""
    print("Installing uv package manager...")
    try:
        # 使用curl安装uv
        curl_command = 'curl -LsSf https://astral.sh/uv/install.sh | sh'
        subprocess.run(curl_command, shell=True, check=True)
        
        # 添加uv到PATH
        home = str(Path.home())
        bashrc_path = os.path.join(home, '.bashrc')
        with open(bashrc_path, 'a') as f:
            f.write('\n# uv package manager\nexport PATH="$HOME/.cargo/bin:$PATH"\n')
        
        print("uv installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing uv: {e}")
        return False

def install_mcp2serial():
    """Install mcp2tcp package."""
    try:
        # 创建虚拟环境并安装包
        subprocess.run(['uv', 'venv', '.venv'], check=True)
        subprocess.run(['.venv/bin/uv', 'pip', 'install', 'mcp2tcp'], check=True)
        return True
    except Exception as e:
        print(f"Error installing mcp2tcp: {e}")
        return False

def configure_claude_desktop():
    """Configure Claude Desktop with mcp2tcp."""
    try:
        home = str(Path.home())
        config_dir = os.path.join(home, '.config', 'claude-desktop')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, 'config.json')
        config = {
            "mcpServers": {
                "mcp2tcp": {
                    "command": "uvx",
                    "args": ["mcp2tcp"]
                }
            }
        }
        
        # 如果配置文件已存在，则更新而不是覆盖
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                existing_config = json.load(f)
            existing_config.setdefault('mcpServers', {})
            existing_config['mcpServers']['mcp2tcp'] = config['mcpServers']['mcp2tcp']
            config = existing_config
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
            
        print("Claude Desktop configured successfully!")
        return True
    except Exception as e:
        print(f"Error configuring Claude Desktop: {e}")
        return False

def setup_config():
    """Setup configuration files."""
    try:
        home = str(Path.home())
        config_dir = os.path.join(home, '.mcp2tcp')
        os.makedirs(config_dir, exist_ok=True)
        
        # 复制默认配置文件
        default_config = os.path.join(os.path.dirname(__file__), 'config.yaml')
        user_config = os.path.join(config_dir, 'config.yaml')
        
        if os.path.exists(default_config):
            shutil.copy2(default_config, user_config)
            print(f"Configuration file copied to: {user_config}")
        return True
    except Exception as e:
        print(f"Error setting up configuration: {e}")
        return False

def main():
    """Main installation process."""
    print("Starting MCP2Serial installation for Ubuntu/Raspberry Pi...")
    
    # 检查Python版本
    if sys.version_info < (3, 11):
        print("Error: Python 3.11 or higher is required")
        sys.exit(1)
    
    # 安装uv（如果需要）
    if not get_uv_path():
        if not install_uv():
            print("Failed to install uv package manager")
            sys.exit(1)
    
    # 安装mcp2serial
    if not install_mcp2serial():
        print("Failed to install mcp2tcp")
        sys.exit(1)
    
    # 配置Claude Desktop
    if not configure_claude_desktop():
        print("Warning: Failed to configure Claude Desktop")
    
    # 设置配置文件
    if not setup_config():
        print("Warning: Failed to setup configuration files")
    
    print("\nInstallation completed!")
    print("\nTo use mcp2tcp:")
    print("1. Activate the virtual environment:")
    print("   source .venv/bin/activate")
    print("2. Run the server:")
    print("   uv run mcp2tcp")
    print("\nFor more information, visit: https://github.com/mcp2everything/mcp2tcp")

if __name__ == "__main__":
    main()
