# ====================================================
# Project: mcp2mqtt
# Description: A protocol conversion tool that enables 
#              hardware devices to communicate with 
#              large language models (LLM) through serial ports.
# Repository: https://github.com/mcp2everything/mcp2mqtt.git
# License: MIT License
# Author: mcp2everything
# Copyright (c) 2024 mcp2everything
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
# ====================================================
from machine import Pin, Timer
import uos
import machine
import gc
import sys

# 初始化 LED 引脚
led = Pin("LED", Pin.OUT)

# 当前占空比（0-100）
duty = 50

# 使用全局变量来模拟计数器
toggle_led_counter = 0

# 定义一个回调函数来模拟 PWM 控制
def toggle_led(timer):
    global led, duty, toggle_led_counter

    if toggle_led_counter < duty:
        led.value(1)  # 开灯
    else:
        led.value(0)  # 关灯

    toggle_led_counter += 1

    if toggle_led_counter >= 100:
        toggle_led_counter = 0

# 启动定时器，每隔 10 毫秒回调一次
timer = Timer()
timer.init(period=10, mode=Timer.PERIODIC, callback=toggle_led)

print("Program started. Send commands in format 'PWM <duty>' or 'PICO_INFO'.")

# 定义一个函数来获取开发板信息
def get_pico_info():
    d = uos.uname()
    board_name = d[4]
    micropython_version = d[2]

    system_freq = machine.freq() // 1000000  # 系统频率 (MHz)

    memory_info = gc.mem_free() + gc.mem_alloc()  # 内存信息

    disk_info = uos.statvfs('/')
    total_disk_size = disk_info[0] * disk_info[2]
    free_disk_size = disk_info[0] * disk_info[3]

    # 拼接信息字符串
    info = (
        f"Board: {board_name}, "
        f"MicroPython: {micropython_version}, "
        f"Freq: {system_freq} MHz, "
        f"Memory: {memory_info} bytes, "
        f"Disk: Total {total_disk_size} bytes, Free {free_disk_size} bytes"
    )
    return info

# 主循环接收用户输入命令
while True:
    try:
        user_input = input()  # 从串口接收用户输入

        if user_input.startswith("PWM"):
            try:
                duty_value = float(user_input.split(" ")[1])

                # 检查占空比是否在 0 到 100 范围内
                if 0 <= duty_value <= 100:
                    duty = int(duty_value)  # 更新占空比例值
                    print("OK")
                else:
                    print("NG")
            except (IndexError, ValueError):
                print("NG")

        elif user_input.strip() == "PICO_INFO":
            info = get_pico_info()
            print(f"OK {info}")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        break



