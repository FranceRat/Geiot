#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                             QTextEdit, QGridLayout, QApplication, QPushButton,  QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

__program__ = 'OFFer'

windows={}
class PersephoneWindow(QWidget):

    def __init__(self,name):
        super().__init__()

        self.initUI(name)


    def initUI(self,name="On"):
        #表示するwebサイトのurl
        initurl = 'https://www.google.co.jp'

        # setting browser
        #Webドキュメントを表示および編集するために使用されているウィジェットを提供します。
        self.browser = QWebEngineView()
        
        #url読み込んでブラウザとして表示
        self.browser.load(QUrl(initurl))
        #サイズ変更中にウィジェットが表示されている場合、ウィジェットはすぐにサイズ変更イベント（resizeEvent（））を受け取ります。
        #ウィジェットが現在表示されていない場合は、表示される前にイベントを受信することが保証されています。
        self.browser.resize(1000,600)
        #wigetの位置を変更する
        self.browser.move(200,200)
        
        self.browser.setWindowTitle(__program__)

        # setting button
        self.back_button = QPushButton('←')
        self.back_button.clicked.connect(self.browser.back)        
        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.browser.forward)
        self.reload_button = QPushButton('reload')
        self.reload_button.clicked.connect(self.browser.reload)
        self.change_button = QPushButton(name)
        self.change_button.clicked.connect(lambda: ChangeWin(name))
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
        grid.addWidget(self.move_button, 1, 14)
        grid.addWidget(self.change_button, 1, 15)
        grid.addWidget(self.browser,2, 0, 1, 15)
        #ここで画面上に配置する
        self.setLayout(grid) 
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle(__program__)
        if name=='On':
            self.show()
        
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
        
        
def ChangeWin(name):
    windows[name].WinDeactive()
    if name=="On":
        windows["Off"].WinActive()
    else:
        windows["On"].WinActive()
    

if __name__ == '__main__':
    # mainPyQt5()
    app = QApplication(sys.argv)

    # setWindowIcon is a method for QApplication, not for QWidget
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon_persephone.png')
    app.setWindowIcon(QIcon(path))
    windows ={"On":PersephoneWindow("On"),"Off":PersephoneWindow("Off")}
    sys.exit(app.exec_())
