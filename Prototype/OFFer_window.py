#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 15:04:15 2021

@author: shota-nak
"""
import sys
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QDialog,QGraphicsView,
                             QTextEdit, QGridLayout, QApplication, QPushButton,QDesktopWidget,
                             QGraphicsScene,QGraphicsPixmapItem,QMessageBox)
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtCore import QUrl,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
#from image import Ui_Form
import cv2
#import threading
from PyQt5.QtGui import (QIcon,QColor,QFont)
#import queue
import time
import plotGraph
import numpy as np
import torch
import torch.nn as nn
import torchvision
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from torchvision import models,transforms
import threading
import datetime

class PersephoneWindow(QWidget):

    def __init__(self,name,control_win,ColorCode):
        super().__init__()
        self.win_name=name
        #self.Triger=Triger
        #self.CameraShowQue=q = queue.Queue()
        self.initUI(name,control_win,ColorCode)


    def initUI(self,name,control_win,ColorCode):
        #表示するwebサイトのurl
        initurl = 'https://www.google.co.jp'
        self.GraphWin=plotGraph.plotGraph()
        self.Camera=Movie(Graph=self.GraphWin,parent=self)
        
        # setting browser
        #Webドキュメントを表示および編集するために使用されているウィジェットを提供します。
        self.browser = QWebEngineView()
        #self.timer = QTimer(self)
        self.Is_CameraAwake=False
        #self.timer.timeout.connect(self.CameraShow)
        #self.timer.start(1000)
        
        #url読み込んでブラウザとして表示
        self.browser.load(QUrl(initurl))
        #サイズ変更中にウィジェットが表示されている場合、ウィジェットはすぐにサイズ変更イベント（resizeEvent（））を受け取ります。
        #ウィジェットが現在表示されていない場合は、表示される前にイベントを受信することが保証されています。
        self.browser.resize(1000,600)
        #wigetの位置を変更する
        self.browser.move(200,200)
        
        self.browser.setWindowTitle(name+"ブラウザ")

        # setting button
        self.back_button = QPushButton('←')
        self.back_button.clicked.connect(self.browser.back)        
        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.browser.forward)
        self.reload_button = QPushButton('reload')
        self.reload_button.clicked.connect(self.browser.reload)
        self.camera_button = QPushButton("カメラ起動")
        self.camera_button.clicked.connect(self.CameraButton)
        self.change_button=QPushButton("On" if name=="Off" else "Off")
        self.change_button.clicked.connect(lambda: control_win.show())
        #1行のテキストライン
        self.url_edit = QLineEdit()
        self.move_button = QPushButton('move')
        self.move_button.clicked.connect(self.loadPage)

        # signal catch from moving web pages.
        #urlが変更された際に呼び出される
        self.browser.urlChanged.connect(self.updateCurrentUrl)

        # setting layout
        grid = QGridLayout()
        #この関数は、垂直方向と水平方向の両方の間隔を間隔に設定します.グリッド間が１０ピクセル空けられる
        grid.setSpacing(5)
        """
        grid.addWidget(wigget,row,col,rowspan=1,colspan=1)
        グリッド内にウィゲットを配置する為のメソッド
        
        -----------------------------------------------
        wigget:wigget
        追加したいwiggetをここに入力
        row:int
        配置する行の場所
        col:int
        配置する列の場所
        rowspan:int
        配置する幅
        colspan:int
        配置する高さ
        """
        grid.addWidget(self.back_button, 1, 0)
        grid.addWidget(self.forward_button, 1, 1)
        grid.addWidget(self.reload_button, 1, 2)
        grid.addWidget(self.url_edit, 1, 3, 1, 10)
        grid.addWidget(self.change_button, 1, 13)
        grid.addWidget(self.move_button, 1, 14)
        grid.addWidget(self.camera_button, 1, 15)
        grid.addWidget(self.browser,2, 0, 1, 16)
        #ここで画面上に配置する
        self.setLayout(grid) 
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle(name+"Window")
        self.colorChange(ColorCode)
        if name=="On":
            self.show()
######ここから緊急ボタン#####    
        else:
            self.emargene_change_button=QPushButton("緊急") 
            self.emargene_change_button.clicked.connect(lambda:self.emargene_change(control_win))
            self.emargene_change_button.setStyleSheet("""
                                         QPushButton {
                                             color: white;
                                             background: red;
                                             }
                                         QPushButton:hover {
                                             color: white;
                                             background: darkred;
                                             }
                                         """)
            grid.addWidget(self.emargene_change_button, 3, 8)
        
            
    """
    def CameraShow(self):
        if self.Is_CameraAwake:
            print("AAAA")
            cv2.imshow(self.win_name+"Camera",self.CameraShowQue.get())
    """
    def emargene_change(self,control_win):
        control_win.Windows["On"].show() 
        control_win.startTime=datetime.datetime.now()
        print(control_win.NowState)
        control_win.NowState="On"
        print(control_win.NowState)
        self.hide()
#####2022/8/8 22:00#####
        
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
    
    def CameraButton(self):
        """
        カメラとグラフのアクティブとでアクティブ

        Returns
        -------
        None.

        """
        if self.Is_CameraAwake:
            self.Camera.close()
            self.Is_CameraAwake=False
            self.GraphWin.close()
        else:
            self.Camera.show()
            self.Is_CameraAwake=True
            self.GraphWin.show()
            
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            QMessageBox.information(None, "通知", "18時になりました.\n疲れていませんか?", QMessageBox.Yes)
            
    def WinDeactive(self):
        self.hide()
    def WinActive(self):
        self.show()
        
    def center(self):
        ''' centering widget
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadPage(self):
        ''' move web page which is set at url_edit
        '''
        #テキストラインからurlを取得する
        move_url = QUrl(self.url_edit.text())
        self.browser.load(move_url)
        self.updateCurrentUrl

    def updateCurrentUrl(self):
        ''' rewriting url_edit when you move different web page.
        '''
        # current_url = self.browser.url().toString()
        #テキストラインを白紙にする
        self.url_edit.clear()
        #現在のひょうじしているurlを表示させる
        self.url_edit.insert(self.browser.url().toString())
        


class Movie(QDialog):
    """
    QDialogはwindowを作成することができる。
    Qwigetの違い
    ========================================
    QWidgetは、Qtのすべての描画可能クラスの基本クラスです。 
    QWidgetベースのクラスは、親がないときに表示することにより、ウィンドウとして表示できます。
    """
    msec = 100 # ms
    
    def __init__(self,Graph,parent=None):
        super().__init__(parent)
        #グラフを描く為のウィンドウ
        self.Graph_win=Graph
        #自身のウィンドウサイズの固定
        self.setFixedSize(234,234)
        #画像表示の準備
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #x軸の表示ピン数
        inputPin_num=20
        self.data=np.zeros(inputPin_num)
        
        #何回目の実行したか
        self.count=0
        
        #AIのモデルを設計する
        self.net=models.vgg16_bn(pretrained=False)
        save_path='weight_fine_tuning_VGG_2Way_extenddata.pth'
        self.net.classifier.add_module("7",nn.Linear(in_features=1000,out_features=2))
        self.net.load_state_dict(torch.load(save_path))
        self.net.eval()
        self.transforms_func=transforms.Compose([transforms.ToPILImage(),transforms.Resize([224,224]),transforms.ToTensor(),
                                            transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])])
    def show(self):
        """
        windowの表示を改良する。
        １.webカメラを設定
        2.描画シーンの設置
        3.描画するタイムイベントの設定
        ４.ウィンドウを表示

        Returns
        -------
        None.

        """
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened() is False:
            raise("IO Error")
            
        self.scene =QGraphicsScene()
        self.set()

       
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set)
        timer.start(self.msec)
        super().show()

    def set(self):
        """
        画像表示を行う
        1.ウェブカメラの画像を取得
        2.中心から(672,672)のサイズでクロップ
        3.(224,224)にリサイズ
        4.10フレームごとにAIのストレスチェック
        5.画像をシーン上に表示

        Returns
        -------
        None.

        """

        ret, cv_img = self.capture.read()
        if ret == False:
            return
        cv_img = cv2.flip(cv_img, 1)
        c_height=int(cv_img.shape[0]/2)
        c_width=int(cv_img.shape[1]/2)
        cut_size=112*3
        cv_img=cv_img[c_height-cut_size:c_height+cut_size,c_width-cut_size:c_width+cut_size,:]
        cv_img=cv2.resize(cv_img, dsize=(224,224))
        
        cv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
        height, width, dim = cv_img.shape
        
        if self.count%10==0:
            threading.Thread(target=self.ThredAction,args=(cv_img,),daemon=True).start()
            

        self.image = QImage(cv_img.data, width, height, QImage.Format_RGB888)
        self.item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.clear()
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)
        self.count+=1
        
        
    def ThredAction(self,cv_img):
         input_img=self.transforms_func(cv_img)
         input_img=torch.unsqueeze(input_img,0)
         pred=torch.mul(self.net(input_img),1/20)
         #一番古いデータを削除
         self.data=np.delete(self.data, 0)
         #最新データの追加
         self.data=np.append(self.data,nn.functional.softmax(pred,1).detach().numpy()[0,0]*100)
         #グラフへのプロット
         self.Graph_win.Plot(self.data)
         #print(nn.functional.softmax(pred,1).detach().numpy()[0])
        
    def close(self):
        """
        閉じる時はカメラキャプチャもリリース

        Returns
        -------
        None.

        """
        self.capture.release()
        super().close()

class Ui_Form(object):
    def setupUi(self, Form):
        """
        UIを設定する

        Parameters
        ----------
        Form : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        Form.setObjectName("Form")
        Form.resize(234, 234)
        self.graphicsView = QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(5, 5, 224, 224))
        self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))