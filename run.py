# -*- coding: utf-8 -*-
"""
应用入口点
运行Flask开发服务器或生产服务器
"""

import sys
import io
import os

# 设置UTF-8编码输出（解决Windows终端编码问题）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from app import create_app

app = create_app()

if __name__ == '__main__':
    # 检查是否在生产环境（Railway会设置PORT环境变量）
    port = int(os.environ.get('PORT', 5000))
    is_production = 'PORT' in os.environ

    print("\n" + "="*60)
    print("🌙 月升月落 - 月相演示程序")
    print("="*60)
    print(f"环境: {'生产环境' if is_production else '开发环境'}")
    print("正在启动服务器...")
    if not is_production:
        print("首次运行时，Skyfield会自动下载星历表文件（~17MB）")
        print(f"请在浏览器中访问: http://localhost:{port}")
    print("="*60 + "\n")

    # 生产环境由Gunicorn启动，这里只用于开发
    app.run(debug=not is_production, host='0.0.0.0', port=port)
