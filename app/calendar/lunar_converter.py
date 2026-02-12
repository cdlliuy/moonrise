# -*- coding: utf-8 -*-
"""
农历转换器模块
实现公历与农历的双向转换
"""

from datetime import datetime
from lunarcalendar import Converter, Lunar, Solar


class LunarCalendarConverter:
    """公历-农历双向转换"""

    # 天干
    HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

    # 地支
    EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

    # 生肖
    ZODIAC_ANIMALS = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

    # 农历月份名称
    LUNAR_MONTHS = ['正月', '二月', '三月', '四月', '五月', '六月',
                    '七月', '八月', '九月', '十月', '冬月', '腊月']

    # 农历日期名称
    LUNAR_DAYS = [
        '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
        '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
    ]

    @staticmethod
    def solar_to_lunar(date):
        """
        公历转农历

        参数:
            date: datetime对象

        返回:
            dict包含:
                - year: 农历年份
                - month: 农历月份（1-12，闰月可能13）
                - day: 农历日期（1-30）
                - is_leap_month: 是否闰月
                - zodiac: 生肖
                - heavenly_stem: 天干
                - earthly_branch: 地支
                - year_name: 干支年名（如"甲辰"）
                - month_name: 农历月份名（如"正月"）
                - day_name: 农历日期名（如"十五"）
                - formatted: 格式化字符串（如"甲辰年正月十五"）
        """
        # 转换为Solar对象
        solar = Solar(date.year, date.month, date.day)

        # 转换为Lunar对象
        lunar = Converter.Solar2Lunar(solar)

        # 计算干支
        year_index = (lunar.year - 4) % 60
        stem = LunarCalendarConverter.HEAVENLY_STEMS[year_index % 10]
        branch = LunarCalendarConverter.EARTHLY_BRANCHES[year_index % 12]
        year_name = stem + branch

        # 计算生肖
        zodiac = LunarCalendarConverter.ZODIAC_ANIMALS[(lunar.year - 4) % 12]

        # 获取月份名称
        month_name = LunarCalendarConverter.LUNAR_MONTHS[lunar.month - 1]
        if lunar.isleap:
            month_name = '闰' + month_name

        # 获取日期名称
        day_name = LunarCalendarConverter.LUNAR_DAYS[lunar.day - 1]

        # 格式化完整字符串
        formatted = f"{year_name}年{month_name}{day_name}"

        return {
            'year': lunar.year,
            'month': lunar.month,
            'day': lunar.day,
            'is_leap_month': lunar.isleap,
            'zodiac': zodiac,
            'heavenly_stem': stem,
            'earthly_branch': branch,
            'year_name': year_name,
            'month_name': month_name,
            'day_name': day_name,
            'formatted': formatted
        }

    @staticmethod
    def lunar_to_solar(year, month, day, is_leap_month=False):
        """
        农历转公历

        参数:
            year: 农历年份
            month: 农历月份（1-12）
            day: 农历日期（1-30）
            is_leap_month: 是否闰月，默认False

        返回:
            datetime对象
        """
        # 创建Lunar对象
        lunar = Lunar(year, month, day, is_leap_month)

        # 转换为Solar对象
        solar = Converter.Lunar2Solar(lunar)

        # 返回datetime对象
        return datetime(solar.year, solar.month, solar.day)

    @staticmethod
    def get_lunar_month_name(month, is_leap=False):
        """
        获取农历月份名称

        参数:
            month: 月份（1-12）
            is_leap: 是否闰月

        返回:
            月份名称字符串
        """
        month_name = LunarCalendarConverter.LUNAR_MONTHS[month - 1]
        if is_leap:
            month_name = '闰' + month_name
        return month_name

    @staticmethod
    def get_lunar_day_name(day):
        """
        获取农历日期名称

        参数:
            day: 日期（1-30）

        返回:
            日期名称字符串
        """
        return LunarCalendarConverter.LUNAR_DAYS[day - 1]

    @staticmethod
    def get_zodiac(year):
        """
        根据农历年份获取生肖

        参数:
            year: 农历年份

        返回:
            生肖字符串
        """
        return LunarCalendarConverter.ZODIAC_ANIMALS[(year - 4) % 12]
