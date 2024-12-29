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
from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='mcp2mqtt Server')
    parser.add_argument('--config', 
                       default="default",
                       help='Configuration name (without _config.yaml suffix)')
    
    args = parser.parse_args()
    asyncio.run(server.main(args.config))


# Expose important items at package level
__version__ = "0.1.0"
__all__ = ['main', 'server']
