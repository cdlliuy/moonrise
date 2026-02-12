# -*- coding: utf-8 -*-
"""
Flask应用工厂
"""

from flask import Flask
from flask_caching import Cache
import os

cache = Cache()


def create_app(config_name=None):
    """
    创建并配置Flask应用

    参数:
        config_name: 配置名称（暂未使用，预留扩展）

    返回:
        Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    from config import Config
    app.config.from_object(Config)

    # 初始化缓存
    cache.init_app(app)

    # 创建星历表目录
    os.makedirs(app.config['EPHEMERIS_DIR'], exist_ok=True)

    # 注册蓝图（路由）
    from app import main
    app.register_blueprint(main.bp)

    return app
