#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if len(p_list) != 2:
        return []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1 and y0 == y1:
            result.append((x0,y0))
        else:
            if abs(y0 - y1) < abs(x0 - x1):
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                k = (y1 - y0) / (x1 - x0)
                y = y0
                for x in range(x0, x1 + 1):
                    result.append((x, int(y + k)))
                    y = y + k
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                k = (x1 - x0) / (y1 - y0)
                x = x0
                for y in range(y0, y1 + 1):
                    result.append((int(x + k), y))
                    x = x + k
    elif algorithm == 'Bresenham':
        if x0 == x1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for y in range(y0, y1+1):
                result.append((x0, y))
        elif y0 == y1:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for x in range(x0, x1 + 1):
                result.append((x, y0))
        elif x0 - x1 == y0 - y1:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for i in range(0, x1 - x0 + 1):
                result.append((x0 + i, y0 + i))
        elif x0 - x1 == y1 - y0:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for i in range(0, x1 - x0 + 1):
                result.append((x0 + i, y0 - i))
        elif abs(y0 - y1) < abs(x0 - x1):
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            d = 2 * (dy - dx)
            t = int((y1 - y0) / dy)
            p = dy + dy - dx
            result.append((x0, y0))
            y = y0
            for x in range(x0, x1):
                if p < 0:
                    result.append((x + 1, y))
                    p = p + dy + dy
                else:
                    result.append((x + 1, y + t))
                    y = y + t
                    p = p + d
        elif abs(y0 - y1) > abs(x0 - x1):
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            d = 2 * (dx - dy)
            t = int((x1 - x0) / dx)
            p = dx + dx - dy
            x = x0
            for y in range(y0, y1):
                if p < 0:
                    result.append((x, y + 1))
                    p = p + dx + dx
                else:
                    result.append((x + t, y + 1))
                    x = x + t
                    p = p + d
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    rx = abs(x0 - x1) / 2
    ry = abs(y0 - y1) / 2
    ry2 = ry * ry
    rx2 = rx * rx
    p1 = ry2 - rx2 * ry + ry2 / 4
    x = 0
    y = ry
    result.append((int(xc), int(yc + ry)))
    result.append((int(xc), int(yc - ry)))
    while 2 * ry2 * x < 2 * rx2 * y:
        if p1 < 0:
            x += 1
            result.append((int(xc + x), int(yc + y)))
            result.append((int(xc + x), int(yc - y)))
            result.append((int(xc - x), int(yc + y)))
            result.append((int(xc - x), int(yc - y)))
            p1 = p1 + 2 * ry2 * x + ry2
        else:
            y -= 1
            x += 1
            result.append((int(xc + x), int(yc + y)))
            result.append((int(xc + x), int(yc - y)))
            result.append((int(xc - x), int(yc + y)))
            result.append((int(xc - x), int(yc - y)))
            p1 = p1 + 2 * ry2 * x - 2 * rx2 * y + ry2
    p2 = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2
    while y > 0:
        if p2 > 0:
            y -= 1
            result.append((int(xc + x), int(yc + y)))
            result.append((int(xc + x), int(yc - y)))
            result.append((int(xc - x), int(yc + y)))
            result.append((int(xc - x), int(yc - y)))
            p2 = p2 - 2 * rx2 * y + rx2
        else:
            x += 1
            y -= 1
            result.append((int(xc + x), int(yc + y)))
            result.append((int(xc + x), int(yc - y)))
            result.append((int(xc - x), int(yc + y)))
            result.append((int(xc - x), int(yc - y)))
            p2 = p2 + 2 * ry2 * x - 2 * rx2 * y + rx2
    return result

def cal_n(i, k, u):
    if k == 1:
        if u >= i * 1000 and u < (i + 1) * 1000:
            return 1
        else:
            return 0
    else:
        return ((u - i * 1000) / ((k - 1) * 1000)) * cal_n(i, k - 1, u) + (((i + k) * 1000 - u) / ((k - 1) * 1000)) * cal_n(i + 1, k - 1, u)

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    ret = []
    if len(p_list) < 3:
        return ret
    if algorithm == "Bezier":
        # if len(p_list) == 2:
        #     return draw_line(p_list, "Bresenham")
        n = len(p_list)
        for tu in range(0, 10000):
            u = tu * 0.0001
            p_bef = p_list.copy()
            p_aft = []
            for r in range(1, n):
                p_aft = []
                for i in range(0, n - r):
                    p_aft.append([(1 - u) * p_bef[i][0] + u * p_bef[i + 1][0], (1 - u) * p_bef[i][1] + u * p_bef[i + 1][1]])
                p_bef = p_aft.copy()
            ret.append([int(p_aft[0][0]), int(p_aft[0][1])])
    else:
        if len(p_list) < 4:
            return ret
        n = len(p_list)
        for u in range(3000, n * 1000 + 1):
            x, y = 0, 0
            for i in range(0, n):
                b = cal_n(i, 4, u)
                x += b * p_list[i][0]
                y += b * p_list[i][1]
            ret.append([int(x), int(y)])
    return ret


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        result.append([p_list[i][0] + dx, p_list[i][1] + dy])
    return result 


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x0 = p_list[i][0]
        y0 = p_list[i][1]
        if x0 == x and y0 == y:
            result.append([x0, y0])
            continue
        r0 = ((x0 - x) * (x0 - x) + (y0 - y) * (y0 - y)) ** 0.5
        w = cal_r(x0 - x, y0 - y)
        w -= (math.pi * r / 180)
        x1 = x + r0 * math.cos(w)
        y1 = y + r0 * math.sin(w)
        result.append([int(x1), int(y1)])
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x1 = x + (x0 - x) * s
        y1 = y + (y0 - y) * s
        result.append([int(x1), int(y1)])
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    if len(p_list) == 0:
        return []
    if algorithm == 'Cohen-Sutherland':
        a = 0
        b = 0
        p1 = p_list[0]
        p2 = p_list[1]
        if p1[0] < x_min:
            a += 1
        if p1[0] > x_max:
            a += (1 << 1)
        if p1[1] < y_min:
            a += (1 << 2)
        if p1[1] > y_max:
            a += (1 << 3)
        if p2[0] < x_min:
            b += 1
        if p2[0] > x_max:
            b += (1 << 1)
        if p2[1] < y_min:
            b += (1 << 2)
        if p2[1] > y_max:
            b += (1 << 3)
        if a == 0 and b == 0:   # 线段完全在窗口边界内
            return p_list
        if a & b != 0:          # 线段完全在窗口外
            return []
        if p2[0] != p1[0]:
            ty = (p2[0] - x_min) * (p1[1] - p2[1]) / (p2[0] - p1[0]) + p2[1] # 与左边的交点
            if ty >= min(p1[1], p2[1]) and ty <= max(p1[1], p2[1]):
                if p1[0] <= x_min:
                    p1 = [x_min, int(ty)]
                else:
                    p2 = [x_min, int(ty)]
        if p2[0] != p1[0]:
            ty = (p2[0] - x_max) * (p1[1] - p2[1]) / (p2[0] - p1[0]) + p2[1] # 与右边的交点
            if ty >= min(p1[1], p2[1]) and ty <= max(p1[1], p2[1]):
                if p1[0] >= x_max:
                    p1 = [x_max, int(ty)]
                else:
                    p2 = [x_max, int(ty)]
        if max(p1[1], p2[1]) < y_min or min(p1[1], p2[1]) > y_max:
            return []
        if p1[1] != p2[1]:
            tx = (y_max - p2[1]) * (p1[0] - p2[0]) / (p1[1] - p2[1]) + p2[0] # 与上边的交点
            if tx >= min(p1[0], p2[0]) and tx <= max(p1[0], p2[0]):
                if p1[1] >= y_max:
                    p1 = [int(tx), y_max]
                else:
                    p2 = [int(tx), y_max]
        if p1[1] != p2[1]:
            tx = (y_min - p2[1]) * (p1[0] - p2[0]) / (p1[1] - p2[1]) + p2[0] # 与下边的交点
            if tx >= min(p1[0], p2[0]) and tx <= max(p1[0], p2[0]):
                if p1[1] <= y_min:
                    p1 = [int(tx), y_min]
                else:
                    p2 = [int(tx), y_min]
        return [p1, p2]
    else:
        p = []
        dx = p_list[1][0] - p_list[0][0]
        dy = p_list[1][1] - p_list[0][1]
        p.append(- dx)
        p.append(dx)
        p.append(- dy)
        p.append(dy)
        q = []
        q.append(p_list[0][0] - x_min)
        q.append(x_max - p_list[0][0])
        q.append(p_list[0][1] - y_min)
        q.append(y_max - p_list[0][1])
        if p[0] == 0:
            if q[0] < 0:
                return []
            p_max = max(p_list[0][1], p_list[1][1])
            p_min = min(p_list[0][1], p_list[1][1])
            if p_max < y_min or p_min > y_max:
                return []
            else:
                return [[p_list[0][0], max(p_min, y_min)], [p_list[0][0], min(p_max, y_max)]]
        if p[2] == 0:
            if q[2] < 0:
                return []
            p_max = max(p_list[0][0], p_list[1][0])
            p_min = min(p_list[0][0], p_list[1][0])
            if p_max < x_min or p_min > x_max:
                return []
            else:
                return [[max(p_min, x_min), p_list[0][1]], [min(p_max, x_max), p_list[0][1]]]
        u1, u2 = 0, 1
        for i in range(0, 4):
            if p[i] < 0: #入边交点
                u1 = max(u1, q[i] / p[i])
            else: #出边交点
                u2 = min(u2, q[i] / p[i])
        if u1 > u2:
            return []
        else:
            return [[int(p_list[0][0] + u1 * dx), int(p_list[0][1] + u1 * dy)], [int(p_list[0][0] + u2 * dx), int(p_list[0][1] + u2 * dy)]] 


def cal_r(x, y):
    """计算角度

    :param x: x坐标
    :param y: y坐标
    :return r: (x, y)在极坐标下对应的弧度theta
    """
    if x == 0:
        if y > 0:
            return math.pi / 2
        else:
            return 3 * math.pi / 2
    elif y == 0:
        if x > 0:
            return 0
        else:
            return math.pi
    else:
        if x < 0:
            return math.atan(y / x) + math.pi
        else:
            return math.atan(y / x)