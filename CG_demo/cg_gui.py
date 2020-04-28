#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF
import math


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.temp_flag = 0
        self.temp_loc = [0, 0]
        self.clip_loc = [0, 0]
        self.temp_list = []
        self.temp_r = 0
        self.temp_dis = 0

    def start_draw_line(self, algorithm, item_id):
        #print('start_draw_line')
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def finish_draw(self):
        #print('finish_draw')
        self.temp_id = self.main_window.get_id()
    
    def start_draw_polygon(self, algorithm, item_id):
        #print('start_draw_polygon')
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_id = item_id
        self.temp_algorithm = None

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_translate(self):
        self.status = 'translate'

    def start_rotate(self):
        self.status = 'rotate'

    def start_scale(self):
        self.status = 'scale'
    
    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_algorithm = algorithm

    def clear_selection(self):
        #print('clear_selection')
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        #print('selection_changed')
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        #print('mousePressEvent')
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if self.temp_flag == 0:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.temp_flag = 1
            else:
                #点在开始点的领域，多边形绘制结束
                if abs(x - self.temp_item.p_list[0][0]) <= 10 and abs(y - self.temp_item.p_list[0][1]) <= 10:
                    self.temp_flag = 0
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                else:
                    self.temp_item.p_list.append([x,y])
                    self.temp_item.p_list[len(self.temp_item.p_list) - 1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'curve':
            if self.temp_flag == 0:
                if self.temp_algorithm == "Bezier":
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
                else:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.temp_flag = 1
            else:
                if self.temp_item.algorithm == "Bezier":
                    self.temp_item.p_list.append(self.temp_item.p_list[len(self.temp_item.p_list) - 1])
                    self.temp_item.p_list[len(self.temp_item.p_list) - 2] = [x, y]
                else:
                    self.temp_item.p_list.append([x, y])
                    self.temp_item.p_list[len(self.temp_item.p_list) - 1] = [x, y]
        elif self.status == 'translate':
            self.temp_loc = [x, y]
        elif self.status == 'rotate':
            self.temp_list = self.item_dict[self.selected_id].p_list
            self.temp_loc = self.item_dict[self.selected_id].center_loc
            self.temp_r = alg.cal_r(x - self.temp_loc[0], y - self.temp_loc[1])
        elif self.status == 'scale':
            self.temp_list = self.item_dict[self.selected_id].p_list
            self.temp_loc = self.item_dict[self.selected_id].center_loc
            self.temp_dis = ((x - self.temp_loc[0]) * (x - self.temp_loc[0]) + (y - self.temp_loc[1]) * (y - self.temp_loc[1])) ** 0.5
        elif self.status == 'clip':
            if self.selected_id == '':
                print("Please choose one line before clipping.")
            else:
                #self.temp_list = self.item_dict[self.selected_id].p_list
                self.temp_loc = [x, y]
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        #print('mouseMoveEvent')
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[len(self.temp_item.p_list) - 1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            self.temp_item.p_list[len(self.temp_item.p_list) - 1] = [x, y]
        elif self.status == 'translate':
            self.item_dict[self.selected_id].p_list = alg.translate(self.item_dict[self.selected_id].p_list, x - self.temp_loc[0], y - self.temp_loc[1])
            self.item_dict[self.selected_id].update()
            self.temp_loc = [x, y]
        elif self.status == 'rotate' :
            x0 = x - self.temp_loc[0]
            y0 = y - self.temp_loc[1]
            r = self.temp_r - alg.cal_r(x0, y0)
            self.item_dict[self.selected_id].p_list = alg.rotate(self.temp_list, self.temp_loc[0], self.temp_loc[1], int(r * 180 / math.pi))
            self.item_dict[self.selected_id].update()
        elif self.status == 'scale' :
            x0 = x - self.temp_loc[0]
            y0 = y - self.temp_loc[1]
            r = (x0 * x0 + y0 * y0) ** 0.5
            self.item_dict[self.selected_id].p_list = alg.scale(self.temp_list, self.temp_loc[0], self.temp_loc[1], r / self.temp_dis)
            self.item_dict[self.selected_id].update()
        elif self.status == 'clip':
            self.clip_loc = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        #print('mouseDoubleClick')
        if self.status == 'polygon':
            self.temp_flag = 0
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status == 'curve':
            self.temp_flag = 0
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        #print('mouseReleaseEvent')
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon': 
            pass #不需要有动作
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'curve':
            pass #不需要有动作
        elif self.status == 'translate':
            self.temp_loc = [0, 0]
        elif self.status == 'rotate':
            self.temp_loc = [0, 0]
        elif self.status == 'clip':
            if self.selected_id != '':
                x_min = min(self.temp_loc[0], self.clip_loc[0])
                x_max = max(self.temp_loc[0], self.clip_loc[0])
                y_min = min(self.temp_loc[1], self.clip_loc[1])
                y_max = max(self.temp_loc[1], self.clip_loc[1])
                self.item_dict[self.selected_id].p_list = alg.clip(self.item_dict[self.selected_id].p_list, x_min, y_min, x_max, y_max, self.temp_algorithm)
                self.item_dict[self.selected_id].update()
                self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        #print('myitem init id: '+item_id)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.center_loc = [0, 0]

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        #print('boundingRect')
        if self.item_type == 'line':
            if self.p_list != []:
                x0, y0 = self.p_list[0]
                x1, y1 = self.p_list[1]
                x = min(x0, x1)
                y = min(y0, y1)
                w = max(x0, x1) - x
                h = max(y0, y1) - y
                self.center_loc = (int(x + w / 2), int(y + h / 2))
                return QRectF(x - 1, y - 1, w + 2, h + 2)
            else:
                return QRectF(0, 0, 0, 0)
        elif self.item_type == 'polygon':
            x0 = self.p_list[0][0]
            y0 = self.p_list[0][1]
            x1 = self.p_list[0][0]
            y1 = self.p_list[0][1]
            for i in range(1, len(self.p_list)):
                x0 = min(x0, self.p_list[i][0])
                y0 = min(y0, self.p_list[i][1])
                x1 = max(x1, self.p_list[i][0])
                y1 = max(y1, self.p_list[i][1])
            self.center_loc = (int((x0 + x1) / 2), int((y0 + y1) / 2))
            return QRectF(x0 - 1, y0 - 1, x1 - x0 + 2, y1 - y0 + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            self.center_loc = (int(x + w / 2), int(y + h / 2))
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            x0 = self.p_list[0][0]
            y0 = self.p_list[0][1]
            x1 = self.p_list[0][0]
            y1 = self.p_list[0][1]
            for i in range(1, len(self.p_list)):
                x0 = min(x0, self.p_list[i][0])
                y0 = min(y0, self.p_list[i][1])
                x1 = max(x1, self.p_list[i][0])
                y1 = max(y1, self.p_list[i][1])
            self.center_loc = (int((x0 + x1) / 2), int((y0 + y1) / 2))
            return QRectF(x0 - 1, y0 - 1, x1 - x0 + 2, y1 - y0 + 2)

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        #print('init')
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        self.item_cnt += 1
        _id = str(self.item_cnt)
        #print('in get_id, id is ' + str(self.item_cnt))
        return _id

    def line_naive_action(self):
        #print('line_naive_action')
        self.canvas_widget.start_draw_line('Naive', str(self.item_cnt))
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        #print('line_dda_action')
        self.canvas_widget.start_draw_line('DDA', str(self.item_cnt))
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        #print('line_bresenham_action')
        self.canvas_widget.start_draw_line('Bresenham', str(self.item_cnt))
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        #print('polygon_dda_action')
        self.canvas_widget.start_draw_polygon('DDA', str(self.item_cnt))
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        #print('polygon_bresenham_action')
        self.canvas_widget.start_draw_polygon('Bresenham', str(self.item_cnt))
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(str(self.item_cnt))
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B_spline', str(self.item_cnt))
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', str(self.item_cnt))
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放')

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪')
    
    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky算法裁剪')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
