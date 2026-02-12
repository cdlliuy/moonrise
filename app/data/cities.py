# -*- coding: utf-8 -*-
"""
中国主要城市地理坐标数据
包含50个主要城市的经纬度信息，用于精确计算月升月落时间
"""

CHINESE_CITIES = [
    # 第一梯队：直辖市和特大城市
    {
        'id': 'beijing',
        'name': '北京',
        'name_en': 'Beijing',
        'latitude': 39.9042,
        'longitude': 116.4074,
        'timezone': 'Asia/Shanghai',
        'province': '直辖市'
    },
    {
        'id': 'shanghai',
        'name': '上海',
        'name_en': 'Shanghai',
        'latitude': 31.2304,
        'longitude': 121.4737,
        'timezone': 'Asia/Shanghai',
        'province': '直辖市'
    },
    {
        'id': 'guangzhou',
        'name': '广州',
        'name_en': 'Guangzhou',
        'latitude': 23.1291,
        'longitude': 113.2644,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'shenzhen',
        'name': '深圳',
        'name_en': 'Shenzhen',
        'latitude': 22.5431,
        'longitude': 114.0579,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'chengdu',
        'name': '成都',
        'name_en': 'Chengdu',
        'latitude': 30.5728,
        'longitude': 104.0668,
        'timezone': 'Asia/Shanghai',
        'province': '四川省'
    },
    {
        'id': 'chongqing',
        'name': '重庆',
        'name_en': 'Chongqing',
        'latitude': 29.5630,
        'longitude': 106.5516,
        'timezone': 'Asia/Shanghai',
        'province': '直辖市'
    },
    {
        'id': 'wuhan',
        'name': '武汉',
        'name_en': 'Wuhan',
        'latitude': 30.5928,
        'longitude': 114.3055,
        'timezone': 'Asia/Shanghai',
        'province': '湖北省'
    },
    {
        'id': 'xian',
        'name': '西安',
        'name_en': "Xi'an",
        'latitude': 34.2658,
        'longitude': 108.9541,
        'timezone': 'Asia/Shanghai',
        'province': '陕西省'
    },
    {
        'id': 'hangzhou',
        'name': '杭州',
        'name_en': 'Hangzhou',
        'latitude': 30.2741,
        'longitude': 120.1551,
        'timezone': 'Asia/Shanghai',
        'province': '浙江省'
    },
    {
        'id': 'nanjing',
        'name': '南京',
        'name_en': 'Nanjing',
        'latitude': 32.0603,
        'longitude': 118.7969,
        'timezone': 'Asia/Shanghai',
        'province': '江苏省'
    },

    # 第二梯队：省会城市
    {
        'id': 'tianjin',
        'name': '天津',
        'name_en': 'Tianjin',
        'latitude': 39.3434,
        'longitude': 117.3616,
        'timezone': 'Asia/Shanghai',
        'province': '直辖市'
    },
    {
        'id': 'harbin',
        'name': '哈尔滨',
        'name_en': 'Harbin',
        'latitude': 45.8038,
        'longitude': 126.5340,
        'timezone': 'Asia/Shanghai',
        'province': '黑龙江省'
    },
    {
        'id': 'changchun',
        'name': '长春',
        'name_en': 'Changchun',
        'latitude': 43.8171,
        'longitude': 125.3235,
        'timezone': 'Asia/Shanghai',
        'province': '吉林省'
    },
    {
        'id': 'shenyang',
        'name': '沈阳',
        'name_en': 'Shenyang',
        'latitude': 41.8057,
        'longitude': 123.4328,
        'timezone': 'Asia/Shanghai',
        'province': '辽宁省'
    },
    {
        'id': 'jinan',
        'name': '济南',
        'name_en': 'Jinan',
        'latitude': 36.6512,
        'longitude': 117.1205,
        'timezone': 'Asia/Shanghai',
        'province': '山东省'
    },
    {
        'id': 'zhengzhou',
        'name': '郑州',
        'name_en': 'Zhengzhou',
        'latitude': 34.7466,
        'longitude': 113.6253,
        'timezone': 'Asia/Shanghai',
        'province': '河南省'
    },
    {
        'id': 'hefei',
        'name': '合肥',
        'name_en': 'Hefei',
        'latitude': 31.8206,
        'longitude': 117.2272,
        'timezone': 'Asia/Shanghai',
        'province': '安徽省'
    },
    {
        'id': 'nanchang',
        'name': '南昌',
        'name_en': 'Nanchang',
        'latitude': 28.6820,
        'longitude': 115.8579,
        'timezone': 'Asia/Shanghai',
        'province': '江西省'
    },
    {
        'id': 'changsha',
        'name': '长沙',
        'name_en': 'Changsha',
        'latitude': 28.2282,
        'longitude': 112.9388,
        'timezone': 'Asia/Shanghai',
        'province': '湖南省'
    },
    {
        'id': 'fuzhou',
        'name': '福州',
        'name_en': 'Fuzhou',
        'latitude': 26.0745,
        'longitude': 119.2965,
        'timezone': 'Asia/Shanghai',
        'province': '福建省'
    },
    {
        'id': 'xiamen',
        'name': '厦门',
        'name_en': 'Xiamen',
        'latitude': 24.4798,
        'longitude': 118.0894,
        'timezone': 'Asia/Shanghai',
        'province': '福建省'
    },
    {
        'id': 'nanning',
        'name': '南宁',
        'name_en': 'Nanning',
        'latitude': 22.8170,
        'longitude': 108.3665,
        'timezone': 'Asia/Shanghai',
        'province': '广西壮族自治区'
    },
    {
        'id': 'kunming',
        'name': '昆明',
        'name_en': 'Kunming',
        'latitude': 25.0406,
        'longitude': 102.7123,
        'timezone': 'Asia/Shanghai',
        'province': '云南省'
    },
    {
        'id': 'guiyang',
        'name': '贵阳',
        'name_en': 'Guiyang',
        'latitude': 26.6470,
        'longitude': 106.6302,
        'timezone': 'Asia/Shanghai',
        'province': '贵州省'
    },
    {
        'id': 'lhasa',
        'name': '拉萨',
        'name_en': 'Lhasa',
        'latitude': 29.6500,
        'longitude': 91.1000,
        'timezone': 'Asia/Shanghai',
        'province': '西藏自治区'
    },
    {
        'id': 'lanzhou',
        'name': '兰州',
        'name_en': 'Lanzhou',
        'latitude': 36.0611,
        'longitude': 103.8343,
        'timezone': 'Asia/Shanghai',
        'province': '甘肃省'
    },
    {
        'id': 'xining',
        'name': '西宁',
        'name_en': 'Xining',
        'latitude': 36.6171,
        'longitude': 101.7782,
        'timezone': 'Asia/Shanghai',
        'province': '青海省'
    },
    {
        'id': 'yinchuan',
        'name': '银川',
        'name_en': 'Yinchuan',
        'latitude': 38.4872,
        'longitude': 106.2309,
        'timezone': 'Asia/Shanghai',
        'province': '宁夏回族自治区'
    },
    {
        'id': 'urumqi',
        'name': '乌鲁木齐',
        'name_en': 'Urumqi',
        'latitude': 43.8256,
        'longitude': 87.6168,
        'timezone': 'Asia/Shanghai',
        'province': '新疆维吾尔自治区'
    },
    {
        'id': 'hohhot',
        'name': '呼和浩特',
        'name_en': 'Hohhot',
        'latitude': 40.8415,
        'longitude': 111.7519,
        'timezone': 'Asia/Shanghai',
        'province': '内蒙古自治区'
    },

    # 第三梯队：重要城市
    {
        'id': 'suzhou',
        'name': '苏州',
        'name_en': 'Suzhou',
        'latitude': 31.2989,
        'longitude': 120.5853,
        'timezone': 'Asia/Shanghai',
        'province': '江苏省'
    },
    {
        'id': 'wuxi',
        'name': '无锡',
        'name_en': 'Wuxi',
        'latitude': 31.4912,
        'longitude': 120.3119,
        'timezone': 'Asia/Shanghai',
        'province': '江苏省'
    },
    {
        'id': 'ningbo',
        'name': '宁波',
        'name_en': 'Ningbo',
        'latitude': 29.8683,
        'longitude': 121.5440,
        'timezone': 'Asia/Shanghai',
        'province': '浙江省'
    },
    {
        'id': 'wenzhou',
        'name': '温州',
        'name_en': 'Wenzhou',
        'latitude': 28.0006,
        'longitude': 120.6994,
        'timezone': 'Asia/Shanghai',
        'province': '浙江省'
    },
    {
        'id': 'qingdao',
        'name': '青岛',
        'name_en': 'Qingdao',
        'latitude': 36.0671,
        'longitude': 120.3826,
        'timezone': 'Asia/Shanghai',
        'province': '山东省'
    },
    {
        'id': 'dalian',
        'name': '大连',
        'name_en': 'Dalian',
        'latitude': 38.9140,
        'longitude': 121.6147,
        'timezone': 'Asia/Shanghai',
        'province': '辽宁省'
    },
    {
        'id': 'shijiazhuang',
        'name': '石家庄',
        'name_en': 'Shijiazhuang',
        'latitude': 38.0428,
        'longitude': 114.5149,
        'timezone': 'Asia/Shanghai',
        'province': '河北省'
    },
    {
        'id': 'taiyuan',
        'name': '太原',
        'name_en': 'Taiyuan',
        'latitude': 37.8706,
        'longitude': 112.5489,
        'timezone': 'Asia/Shanghai',
        'province': '山西省'
    },
    {
        'id': 'haikou',
        'name': '海口',
        'name_en': 'Haikou',
        'latitude': 20.0444,
        'longitude': 110.1999,
        'timezone': 'Asia/Shanghai',
        'province': '海南省'
    },
    {
        'id': 'sanya',
        'name': '三亚',
        'name_en': 'Sanya',
        'latitude': 18.2528,
        'longitude': 109.5117,
        'timezone': 'Asia/Shanghai',
        'province': '海南省'
    },
    {
        'id': 'zhuhai',
        'name': '珠海',
        'name_en': 'Zhuhai',
        'latitude': 22.2711,
        'longitude': 113.5767,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'dongguan',
        'name': '东莞',
        'name_en': 'Dongguan',
        'latitude': 23.0205,
        'longitude': 113.7518,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'foshan',
        'name': '佛山',
        'name_en': 'Foshan',
        'latitude': 23.0218,
        'longitude': 113.1219,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'zhongshan',
        'name': '中山',
        'name_en': 'Zhongshan',
        'latitude': 22.5171,
        'longitude': 113.3926,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'huizhou',
        'name': '惠州',
        'name_en': 'Huizhou',
        'latitude': 23.1115,
        'longitude': 114.4152,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'shantou',
        'name': '汕头',
        'name_en': 'Shantou',
        'latitude': 23.3540,
        'longitude': 116.6824,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'zhanjiang',
        'name': '湛江',
        'name_en': 'Zhanjiang',
        'latitude': 21.2707,
        'longitude': 110.3577,
        'timezone': 'Asia/Shanghai',
        'province': '广东省'
    },
    {
        'id': 'guilin',
        'name': '桂林',
        'name_en': 'Guilin',
        'latitude': 25.2736,
        'longitude': 110.2900,
        'timezone': 'Asia/Shanghai',
        'province': '广西壮族自治区'
    },
    {
        'id': 'luoyang',
        'name': '洛阳',
        'name_en': 'Luoyang',
        'latitude': 34.6197,
        'longitude': 112.4540,
        'timezone': 'Asia/Shanghai',
        'province': '河南省'
    },
    {
        'id': 'nantong',
        'name': '南通',
        'name_en': 'Nantong',
        'latitude': 32.0085,
        'longitude': 120.8943,
        'timezone': 'Asia/Shanghai',
        'province': '江苏省'
    }
]


def get_city_by_id(city_id):
    """根据城市ID获取城市信息"""
    for city in CHINESE_CITIES:
        if city['id'] == city_id:
            return city
    return None


def get_all_cities():
    """获取所有城市列表"""
    return CHINESE_CITIES


def get_cities_by_province(province):
    """根据省份获取城市列表"""
    return [city for city in CHINESE_CITIES if city['province'] == province]
