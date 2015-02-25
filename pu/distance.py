# -*- coding: utf-8 -*-
from math import pi, sin, cos, acos

EARTH_RADIUS = 6378137

PI_180 = pi / 180

def distance(lo1, la1, lo2, la2):
    """计算两点之间的距离，单位: 米

    :param lo1, la1: 第一个点的经度、纬度
    :param lo2, la2: 第二个点的经度、纬度

    参考:
    * http://www.geodatasource.com/developers/c
    * http://boulter.com/gps/distance/
    """
    if abs(lo2 - lo1) + abs(la2 - la1) < 0.000001:
        return 0

    la1 = la1 * PI_180
    la2 = la2 * PI_180

    theta = (lo1 - lo2) * PI_180
    dist = sin(la1) * sin(la2) + cos(la1) * cos(la2) * cos(theta)
    dist = acos(dist)

    return dist * EARTH_RADIUS
