import os

class Config:
    """应用程序配置类"""

    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-moonraise-2024'

    # 时区配置
    DEFAULT_TIMEZONE = 'Asia/Shanghai'

    # 缓存配置
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 3600  # 1小时

    # Skyfield星历表配置
    EPHEMERIS_DIR = os.path.join(os.path.dirname(__file__), 'app/data/ephemeris')
    EPHEMERIS_FILE = 'de421.bsp'  # JPL DE421星历表

    # 月相中文名称映射
    MOON_PHASES_ZH = {
        'new': '新月',
        'waxing_crescent': '峨眉月',
        'first_quarter': '上弦月',
        'waxing_gibbous': '盈凸月',
        'full': '满月',
        'waning_gibbous': '亏凸月',
        'last_quarter': '下弦月',
        'waning_crescent': '残月'
    }

    # 月相表情符号映射
    MOON_PHASES_EMOJI = {
        'new': '🌑',
        'waxing_crescent': '🌒',
        'first_quarter': '🌓',
        'waxing_gibbous': '🌔',
        'full': '🌕',
        'waning_gibbous': '🌖',
        'last_quarter': '🌗',
        'waning_crescent': '🌘'
    }
