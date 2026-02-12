# -*- coding: utf-8 -*-
"""
Flask路由和视图
"""

from flask import Blueprint, render_template, jsonify, request
from datetime import datetime
from app.astronomy.moon_calculator import MoonCalculator
from app.calendar.lunar_converter import LunarCalendarConverter
from app.data.cities import get_city_by_id, get_all_cities
from app import cache

bp = Blueprint('main', __name__)


@bp.route('/health')
def health():
    """健康检查端点，用于Railway监控和保活"""
    return jsonify({
        'status': 'ok',
        'app': 'moonrise',
        'version': '1.0.0'
    })


@bp.route('/')
def index():
    """主页"""
    cities = get_all_cities()
    return render_template('index.html', cities=cities)


@bp.route('/api/moon/<city_id>/<date_str>')
@cache.cached(timeout=3600)
def get_moon_data(city_id, date_str):
    """
    获取指定城市和日期的月相和月升月落信息

    参数:
        city_id: 城市ID
        date_str: 日期字符串（格式：YYYY-MM-DD）

    返回:
        JSON格式的月相和月升月落数据
    """
    try:
        # 获取城市信息
        city = get_city_by_id(city_id)
        if not city:
            return jsonify({'error': '城市不存在'}), 404

        # 解析日期
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # 创建月球计算器
        calc = MoonCalculator(
            city['latitude'],
            city['longitude'],
            city['timezone']
        )

        # 获取月相信息
        phase_info = calc.get_moon_phase(date)

        # 获取月升月落信息
        rise_set_info = calc.get_rise_set_times(date)

        # 获取农历信息
        lunar_info = LunarCalendarConverter.solar_to_lunar(date)

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

        # 组装返回数据
        result = {
            'city': city,
            'date': date_str,
            'phase': {
                'angle': round(phase_info['phase_angle'], 2),
                'illumination': round(phase_info['illumination'], 2),
                'name': phase_info['phase_name'],
                'emoji': phase_info['phase_emoji'],
                'type': phase_info['phase_type']
            },
            'rise_set': {
                'moonrise': moonrise_str,
                'moonset': moonset_str,
                'is_always_up': rise_set_info['is_always_up'],
                'is_always_down': rise_set_info['is_always_down']
            },
            'lunar': lunar_info
        }

        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': '日期格式错误，应为YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/calendar/<city_id>/<int:year>/<int:month>')
@cache.cached(timeout=3600)
def get_month_calendar(city_id, year, month):
    """
    获取指定城市、年份和月份的整月月相日历

    参数:
        city_id: 城市ID
        year: 年份
        month: 月份（1-12）

    返回:
        JSON格式的整月数据
    """
    try:
        # 获取城市信息
        city = get_city_by_id(city_id)
        if not city:
            return jsonify({'error': '城市不存在'}), 404

        # 验证月份
        if month < 1 or month > 12:
            return jsonify({'error': '月份必须在1-12之间'}), 400

        # 创建月球计算器
        calc = MoonCalculator(
            city['latitude'],
            city['longitude'],
            city['timezone']
        )

        # 获取整月数据
        month_data = calc.get_month_data(year, month)

        # 为每一天添加农历信息
        for day_data in month_data:
            lunar_info = LunarCalendarConverter.solar_to_lunar(day_data['date'])
            day_data['lunar'] = {
                'month_name': lunar_info['month_name'],
                'day_name': lunar_info['day_name'],
                'formatted': lunar_info['formatted']
            }
            # 转换日期为字符串
            day_data['date'] = day_data['date'].strftime('%Y-%m-%d')
            # 删除datetime对象（不能JSON序列化）
            if 'moonrise_time' in day_data:
                del day_data['moonrise_time']
            if 'moonset_time' in day_data:
                del day_data['moonset_time']

        result = {
            'city': city,
            'year': year,
            'month': month,
            'days': month_data
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/cities')
def get_cities():
    """获取所有城市列表"""
    cities = get_all_cities()
    return jsonify(cities)
