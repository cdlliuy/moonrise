#!/bin/bash

echo "========================================"
echo "🌙 月升月落 - 快速启动脚本"
echo "========================================"
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "[1/3] 创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
    echo ""
else
    echo "✓ 虚拟环境已存在"
    echo ""
fi

# 激活虚拟环境
echo "[2/3] 激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 检查是否需要安装依赖
if ! pip show flask > /dev/null 2>&1; then
    echo "[3/3] 安装依赖包..."
    pip install -r requirements.txt
    echo "✓ 依赖安装完成"
    echo ""
else
    echo "✓ 依赖已安装"
    echo ""
fi

echo "========================================"
echo "启动应用程序..."
echo "首次运行时会下载星历表文件（约17MB）"
echo "请稍候..."
echo "========================================"
echo ""

# 运行应用
python run.py
