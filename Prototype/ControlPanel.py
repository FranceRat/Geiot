#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 00:52:50 2021

@author: shota-nak
"""

import sys
import numpy as np
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                             QTextEdit, QGridLayout, QApplication, QPushButton,  QDesktopWidget)
from PyQt5.QtGui import (QIcon,QColor,QFont)
from PyQt5.QtCore import QUrl,QTimer,Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence
import datetime
import OFFer_window

class ControlWindow(QWidget):
    def __init__(self):
        self.Trigers={"On":"水を飲む","Off":"腕をまくる"}
        self.startTime=datetime.datetime.now()
        
        self.GREEN=np.array([0,180,23])
        self.BLUE=np.array([69,115,197])
        self.Windows={"On":OFFer_window.PersephoneWindow("On",self,self.BLUE),
                      "Off":OFFer_window.PersephoneWindow("Off",self,self.GREEN)}
        self.NowState="On"
        #self.Windows[self.NowState].show()
        super().__init__(None)
        """
        self.setGeometry(int x, int y, int w, int h)
        :::windowサイズをここで規定する。
        """
        self.setGeometry(300, 50, 800, 500)
        self.setFixedSize(800,500)
        self.colorChange(self.BLUE)
        self.setWindowTitle('ControlPanel')
        self.TimeLabel=QLabel("               ",self)
        self.TimeLabel.setFont(QFont("Times",30, QFont.Bold))
        self.TimeLabel.setAlignment(Qt.AlignCenter)
        #ボタンを設定
        self.change_button = QPushButton("Off",parent=self)
        self.cansel_button=QPushButton("戻る",parent=self)
        self.ConsoleTextLog=QLineEdit(parent=self)
        self.ConsoleTextLog.setFont(QFont("Times",30, QFont.Bold))
        self.ConsoleTextLog.setText(self.Trigers[self.NowState])
        self.ConsoleTextLog.setAlignment(Qt.AlignCenter)
        self.ConsoleTextLog.setReadOnly(True)
        
        self.ConsoleTextLog.resize(500, 450)
        self.change_button.resize(100, 50)
        self.cansel_button.resize(50, 25)
        self.change_button.setStyleSheet("""
                                         QPushButton {
                                             color: #fff;
                                             border-top: 4px solid #48ecc4;
                                             border-right: 4px solid #0a5f4a;
                                             border-bottom: 4px solid #0f745b;
                                             border-left: 4px solid #8cf9de;
                                             border-radius: 0;
                                             background: """+self.RGB_2_HTMLColorCode(self.BLUE-80)+""";
                                             }
                                         QPushButton:hover {
                                             color: #fff;
                                             border-top: 4px solid #0f745b;
                                             border-right: 4px solid #8cf9de;
                                             border-bottom: 4px solid #48ecc4;
                                             border-left: 4px solid #0a5f4a;
                                             }""")
        self.change_button.clicked.connect(self.ChangeWin)
        self.cansel_button.clicked.connect(lambda:self.hide())
        #このオブジェクトを親としてタイマーのオブジェクトを作成
        timer = QTimer(self)
        #taimeoutした際の処理を設定する
        timer.timeout.connect(self.getDateTime)
        timer.start(1000) # 1000ミリ秒ごとにタイムアウト
        self.TimeLabel.move(30, 120)
        self.change_button.move(80, 210)
        #self.change_button.move(80, 235)
        self.ConsoleTextLog.move(260,25)
    
    
    def ChangeWin(self):
        """
        windowのオンオフを切り替える

        Returns
        -------
        None.

        """
        print(self.NowState)
        if(self.NowState=="On"):
            self.Windows[self.NowState].WinDeactive()
            self.change_button.setStyleSheet("""
                                         QPushButton {
                                             color: #fff;
                                             border-top: 4px solid #48ecc4;
                                             border-right: 4px solid #0a5f4a;
                                             border-bottom: 4px solid #0f745b;
                                             border-left: 4px solid #8cf9de;
                                             border-radius: 0;
                                             background: """+self.RGB_2_HTMLColorCode(self.GREEN-80)+""";
                                             }
                                         QPushButton:hover {
                                             color: #fff;
                                             border-top: 4px solid #0f745b;
                                             border-right: 4px solid #8cf9de;
                                             border-bottom: 4px solid #48ecc4;
                                             border-left: 4px solid #0a5f4a;
                                             }""")
            self.colorChange(self.GREEN)
            self.change_button.setText("On")
            self.NowState="Off"
            self.ConsoleTextLog.setText(self.Trigers[self.NowState])
            self.Windows[self.NowState].WinActive()
        elif (self.NowState=="Off"):
            self.Windows[self.NowState].WinDeactive()
            self.change_button.setStyleSheet("""
                                         QPushButton {
                                             color: #fff;
                                             border-top: 4px solid #48ecc4;
                                             border-right: 4px solid #0a5f4a;
                                             border-bottom: 4px solid #0f745b;
                                             border-left: 4px solid #8cf9de;
                                             border-radius: 0;
                                             background: """+self.RGB_2_HTMLColorCode(self.BLUE-80)+""";
                                             }
                                         QPushButton:hover {
                                             color: #fff;
                                             border-top: 4px solid #0f745b;
                                             border-right: 4px solid #8cf9de;
                                             border-bottom: 4px solid #48ecc4;
                                             border-left: 4px solid #0a5f4a;
                                             }""")
            self.colorChange(self.BLUE)
            self.change_button.setText("Off")
            self.NowState="On"
            self.ConsoleTextLog.setText(self.Trigers[self.NowState])
            self.Windows[self.NowState].WinActive()
        self.hide()
        self.startTime=datetime.datetime.now()
            
            
        
    def colorChange(self,ColorCode):
        """
        windowの色を変更する

        Parameters
        ----------
        ColorCode : list
            （red,green,blue）

        """
        p= self.palette()
        p.setColor(self.backgroundRole(),QColor(*ColorCode,alpha=255))
        self.setPalette(p)
        
    def getDateTime(self):
        """
        timeoutした際の処理
        
        Returns
        -------
        None.

        """
        dt = datetime.datetime.now()-self.startTime
        h,m=self.get_h_m_s(dt)
        dt_str = '現在の'+self.NowState+'時間\n{}時間{}分'.format(h,m)
        #print(dt_str)
        self.TimeLabel.setText(dt_str)
        
        
    def get_h_m_s(self,td):
        m, s = divmod(td.seconds, 60)
        h, m = divmod(m, 60)
        return h, m
        
    def RGB_2_HTMLColorCode(self,RGB):
        """
        RGB配列からHTMLColorCodeに変換

        Parameters
        ----------
        RGB : np.array
            RGBで可能されている配列

        Returns
        -------
        color_code : str
            HTMLColorCodeを出力

        """
        color_code = '{}{}{}'.format(hex(RGB[0]), hex(RGB[1]), hex(RGB[2]))
        color_code = color_code.replace('0x', '')
        color_code="#"+color_code.zfill(6)
        return color_code
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ControlWindow()
    #main_window.show()
    sys.exit(app.exec_())
    
