# Raspberry Pi Pico Firmware

这个目录包含用于树莓派 Pico 的固件程序，用于处理串口通信和 PWM 控制。

## 目录结构
```
firmware/
├── src/                    # Pico 源代码
│   ├── main.py            # 主程序
└── README.md              # 说明文档
```

## 安装说明
1. 将 Pico 连接到电脑
2. 使用Thonny连接Pico，保存main.py文件到 Pico中
3. 重启 Pico
4. 关闭Thonny（用于释放串口）
5. 安装mcp2tcp服务 配置串口参数和claude mcp协议，启动Claude客户端

## 开发说明
- 修改 `main.py` 来更新串口通信逻辑
