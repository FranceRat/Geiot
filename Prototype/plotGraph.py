# - * - coding: utf8 - *

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random # 今回は乱数を使用するのでimportします。
import numpy as np
import datetime

############################
##
## ウィンドウ用のクラスです。
##
############################
class plotGraph(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'ストレスレベル'
        self.setFixedSize(500,300)
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(0, 0, self.width, self.height)

        self.setWindowLayout()
        #self.statusBar()
    def Plot(self,data):
        self.m.plot(data)

    def setWindowLayout(self):

        ### メニューバーアクションの定義 ###
        exitAction = QAction('&終了', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('ウィンドウを閉じるよ')
        exitAction.triggered.connect(qApp.quit)

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('ファイル') 
        #fileMenu.addAction(exitAction)

        #self.w = QWidget()

        ### 実際にグラフを打つPlotCanvasクラスのインスタンスを生成します。 ###
        self.m = PlotCanvas(self, width=5, height=4)


        ### GridLayoutを使用します。 ###
        main_layout = QGridLayout()

        ### GridLayoutのどこに何を配置するのか指定します。 ###
        main_layout.addWidget(self.m, 0, 0, 5, 4)

        self.setLayout(main_layout)
        #self.setCentralWidget(self.w)
        #self.show()



##################################
##
## 実際にグラフを描画するクラスです。
##
##################################
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111,ylim=(0,100),yticks=[0,50,80,100])
        super().__init__(self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
                self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding
                )
        FigureCanvas.updateGeometry(self)
        #self.plot(data=[0,0,0,0,0])

    def plot(self,data):
        self.axes.cla()
        color_arg="r-" if np.mean(data)>70 else "b-"
        self.axes.set_ylim(0, 100)
        self.axes.plot(data, color_arg)
        #self.axes.set_title('ストレスレベル')
        self.draw()

    def clear(self):
        self.axes.cla()
        self.draw()
