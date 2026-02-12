@echo off
chcp 65001 >nul
echo ========================================
echo 🌙 月升月落 - 快速启动脚本
echo ========================================
echo.

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo [1/3] 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境创建完成
    echo.
) else (
    echo ✓ 虚拟环境已存在
    echo.
)

REM 激活虚拟环境
echo [2/3] 激活虚拟环境...
call venv\Scripts\activate
echo ✓ 虚拟环境已激活
echo.

REM 检查是否需要安装依赖
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [3/3] 安装依赖包...
    pip install -r requirements.txt
    echo ✓ 依赖安装完成
    echo.
) else (
    echo ✓ 依赖已安装
    echo.
)

echo ========================================
echo 启动应用程序...
echo 首次运行时会下载星历表文件（约17MB）
echo 请稍候...
echo ========================================
echo.

REM 运行应用
python run.py

pause
