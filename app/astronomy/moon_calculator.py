# -*- coding: utf-8 -*-
"""
月球计算器模块
使用Skyfield库计算月相、月升月落时间和月球位置
"""

from datetime import datetime, timedelta
from skyfield.api import load, Topos
from skyfield import almanac
import pytz
import math


class MoonCalculator:
    """基于Skyfield的月球计算引擎"""

    def __init__(self, latitude, longitude, timezone_str='Asia/Shanghai'):
        """
        初始化月球计算器

        参数:
            latitude: 纬度（度）
            longitude: 经度（度）
            timezone_str: 时区字符串，默认为'Asia/Shanghai'
        """
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = pytz.timezone(timezone_str)

        # 加载Skyfield星历表
        self.ts = load.timescale()
        self.eph = load('de421.bsp')  # JPL DE421星历表

        # 创建观测者位置
        self.location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

        # 获取地球和月球对象
        self.earth = self.eph['earth']
        self.moon = self.eph['moon']
        self.sun = self.eph['sun']

    def get_moon_phase(self, date):
        """
        计算指定日期的月相信息

        参数:
            date: datetime对象

        返回:
            dict包含:
                - phase_angle: 月相角度（0-360度，0=新月，180=满月）
                - illumination: 光照百分比（0-100）
                - phase_name: 月相名称（中文）
                - phase_emoji: 月相表情符号
                - phase_type: 月相类型（英文key）
        """
        # 转换为Skyfield时间
        if date.tzinfo is None:
            date = self.timezone.localize(date)

        t = self.ts.from_datetime(date)

        # 计算月相角度
        phase_angle = almanac.moon_phase(self.eph, t)
        phase_degrees = phase_angle.degrees

        # 计算光照百分比
        # 相位角: 0° = 新月, 180° = 满月
        # 光照比例 = (1 + cos(相位角)) / 2
        illumination = 50 * (1 + math.cos(math.radians(phase_degrees)))

        # 确定月相名称
        phase_type, phase_name, phase_emoji = self._get_phase_name(phase_degrees)

        return {
            'phase_angle': phase_degrees,
            'illumination': illumination,
            'phase_name': phase_name,
            'phase_emoji': phase_emoji,
            'phase_type': phase_type
        }

    def _get_phase_name(self, phase_degrees):
        """
        根据相位角确定月相名称

        参数:
            phase_degrees: 相位角（度）

        返回:
            (phase_type, phase_name, phase_emoji)
        """
        # 标准化角度到0-360
        phase_degrees = phase_degrees % 360

        # 月相划分（每个相位约45度）
        if phase_degrees < 22.5 or phase_degrees >= 337.5:
            return ('new', '新月', '🌑')
        elif 22.5 <= phase_degrees < 67.5:
            return ('waxing_crescent', '峨眉月', '🌒')
        elif 67.5 <= phase_degrees < 112.5:
            return ('first_quarter', '上弦月', '🌓')
        elif 112.5 <= phase_degrees < 157.5:
            return ('waxing_gibbous', '盈凸月', '🌔')
        elif 157.5 <= phase_degrees < 202.5:
            return ('full', '满月', '🌕')
        elif 202.5 <= phase_degrees < 247.5:
            return ('waning_gibbous', '亏凸月', '🌖')
        elif 247.5 <= phase_degrees < 292.5:
            return ('last_quarter', '下弦月', '🌗')
        else:  # 292.5 <= phase_degrees < 337.5
            return ('waning_crescent', '残月', '🌘')

    def get_rise_set_times(self, date):
        """
        计算指定日期的月升月落时间

        参数:
            date: datetime对象（日期部分）

        返回:
            dict包含:
                - moonrise: 月升时间（datetime或None）
                - moonset: 月落时间（datetime或None）
                - is_always_up: 月亮全天可见
                - is_always_down: 月亮全天不可见
        """
        # 确保date是当地时间
        if date.tzinfo is None:
            date = self.timezone.localize(date)

        # 设置搜索时间范围（当天00:00到次日00:00）
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)

        # 转换为Skyfield时间
        t0 = self.ts.from_datetime(start_date)
        t1 = self.ts.from_datetime(end_date)

        # 创建观测者
        observer = self.earth + self.location

        # 查找月升月落事件
        f = almanac.risings_and_settings(self.eph, self.moon, self.location)
        times, events = almanac.find_discrete(t0, t1, f)

        moonrise = None
        moonset = None

        # 解析事件
        # events: True表示升起，False表示落下
        for t, event in zip(times, events):
            event_time = t.astimezone(self.timezone)
            if event:  # 升起
                if moonrise is None:
                    moonrise = event_time
            else:  # 落下
                if moonset is None:
                    moonset = event_time

        # 检查是否全天可见或全天不可见
        is_always_up = False
        is_always_down = False

        if moonrise is None and moonset is None:
            # 检查当天中午月亮的高度角
            noon = start_date.replace(hour=12)
            t_noon = self.ts.from_datetime(noon)
            apparent = observer.at(t_noon).observe(self.moon).apparent()
            alt, az, distance = apparent.altaz()

            if alt.degrees > 0:
                is_always_up = True
            else:
                is_always_down = True

        return {
            'moonrise': moonrise,
            'moonset': moonset,
            'is_always_up': is_always_up,
            'is_always_down': is_always_down
        }

    def get_moon_position(self, dt):
        """
        计算指定时刻的月球位置

        参数:
            dt: datetime对象

        返回:
            dict包含:
                - altitude: 地平高度（度）
                - azimuth: 方位角（度，0=北，90=东）
                - distance: 距离地球的距离（公里）
        """
        if dt.tzinfo is None:
            dt = self.timezone.localize(dt)

        t = self.ts.from_datetime(dt)
        observer = self.earth + self.location

        apparent = observer.at(t).observe(self.moon).apparent()
        alt, az, distance = apparent.altaz()

        return {
            'altitude': alt.degrees,
            'azimuth': az.degrees,
            'distance': distance.km
        }

    def get_month_data(self, year, month):
        """
        获取整月的月相和月升月落数据

        参数:
            year: 年份
            month: 月份（1-12）

        返回:
            list of dict，每个dict包含一天的数据
        """
        # 计算该月的天数
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)

        first_day = datetime(year, month, 1)
        days_in_month = (next_month - first_day).days

        month_data = []

        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day, 12, 0)  # 使用中午时间计算月相

            # 获取月相信息
            phase_info = self.get_moon_phase(date)

            # 获取月升月落时间
            rise_set_info = self.get_rise_set_times(date)

            # 格式化月升月落时间
            moonrise_str = None
            moonset_str = None

            if rise_set_info['moonrise']:
                moonrise_str = rise_set_info['moonrise'].strftime('%H:%M')
            elif rise_set_info['is_always_up']:
                moonrise_str = '全天可见'
            elif rise_set_info['is_always_down']:
                moonrise_str = '月不出'

            if rise_set_info['moonset']:
                moonset_str = rise_set_info['moonset'].strftime('%H:%M')
            elif rise_set_info['is_always_up']:
                moonset_str = '全天可见'
            elif rise_set_info['is_always_down']:
                moonset_str = '月不落'

            day_data = {
                'date': date,
                'day': day,
                'phase_angle': phase_info['phase_angle'],
                'illumination': phase_info['illumination'],
                'phase_name': phase_info['phase_name'],
                'phase_emoji': phase_info['phase_emoji'],
                'phase_type': phase_info['phase_type'],
                'moonrise': moonrise_str,
                'moonset': moonset_str,
                'moonrise_time': rise_set_info['moonrise'],
                'moonset_time': rise_set_info['moonset']
            }

            month_data.append(day_data)

        return month_data
