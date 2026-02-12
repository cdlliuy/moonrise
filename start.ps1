# PowerShell启动脚本 - 月升月落程序

# 设置输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌙 月升月落 - 月相演示程序" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境是否存在
if (-not (Test-Path "venv")) {
    Write-Host "[1/3] 创建虚拟环境..." -ForegroundColor Green
    python -m venv venv
    Write-Host "✓ 虚拟环境创建完成" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✓ 虚拟环境已存在" -ForegroundColor Green
    Write-Host ""
}

# 激活虚拟环境
Write-Host "[2/3] 激活虚拟环境..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ 虚拟环境已激活" -ForegroundColor Green
Write-Host ""

# 检查是否需要安装依赖
$flaskInstalled = python -m pip show flask 2>$null
if (-not $flaskInstalled) {
    Write-Host "[3/3] 安装依赖包..." -ForegroundColor Green
    pip install -r requirements.txt
    Write-Host "✓ 依赖安装完成" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✓ 依赖已安装" -ForegroundColor Green
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "启动应用程序..." -ForegroundColor Yellow
Write-Host "首次运行时会下载星历表文件（约17MB）" -ForegroundColor Gray
Write-Host "请稍候..." -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 运行应用
python run.py
