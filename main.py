#기본 위젯 사용하여 기본창 생성
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import pandas as pd
import webbrowser
import glob

form_class = uic.loadUiType('ui/form.ui')[0]

class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tablelist = [self.tableWidget_1,self.tableWidget_3,self.tableWidget_4,self.tableWidget_5,self.tableWidget_6]
        self.file_list = glob.glob('./data/추천키워드/카테고리별top5/*')
        self.file_list_top5 = [file for file in self.file_list if file.endswith(".csv")]
        self.webviewerlist = [self.webEngineView_1,self.webEngineView_2,self.webEngineView_3,self.webEngineView_4,self.webEngineView_5,self.webEngineView_6,self.webEngineView_7,
                              self.webEngineView_8,self.webEngineView_9,self.webEngineView_10,self.webEngineView_11,self.webEngineView_12,self.webEngineView_13,self.webEngineView_14,
                              self.webEngineView_15,self.webEngineView_16,self.webEngineView_17,self.webEngineView_18,self.webEngineView_19,self.webEngineView_20,self.webEngineView_21,
                              self.webEngineView_22,self.webEngineView_23,self.webEngineView_24,self.webEngineView_25,self.webEngineView_26,self.webEngineView_27,self.webEngineView_28,
                              self.webEngineView_29,self.webEngineView_30]
        self.label_list = [self.lbl_picture_3,self.lbl_picture_4,self.lbl_picture_5,self.lbl_picture_6,self.lbl_picture_7]
        self.pic_list= glob.glob('./data/추천키워드/Word2Vec 자료/*')
        self.pic_list_png = [file for file in self.pic_list if file.endswith(".png")]
        self.btn_loadFromFile.clicked.connect(self.loadImageFromFile)
        self.btn_loadFromFile.clicked.connect(self.loadImageFromFile2)
        for i in range(5):
            self.setTableWidgetData(tablelist=self.tablelist[i],csvlist=self.file_list_top5[i],value=i)
            self.loadImageFromFile3(label_list=self.label_list[i],pic_list=self.pic_list_png[i])

    def loadImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("data/감정분석/감정분석코로나_pie_chart.png")
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(500)
        self.lbl_picture.setPixmap(self.qPixmapFileVar)

    def loadImageFromFile2(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("data/감정분석/감정분석코로나_test_set워드클라우드.png")
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(500)
        self.lbl_picture_2.setPixmap(self.qPixmapFileVar)

    def loadImageFromFile3(self,label_list,pic_list) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap(pic_list)
        self.qPixmapFileVar.load(pic_list)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(650)
        label_list.setPixmap(self.qPixmapFileVar)

    def setTableWidgetData(self,tablelist,csvlist,value):
        df=pd.read_csv(csvlist)
        df=df[['keyword','values']]
        tablelist.setColumnCount(2)
        tablelist.setRowCount(len(df))
        tablelist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tablelist.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tablelist.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tablelist.resizeColumnsToContents()
        tablelist.resizeRowsToContents()
        tablelist.setHorizontalHeaderLabels(['키워드','빈도수'])
        tablelist.setVerticalHeaderLabels([str(i) for i in range(0,len(df))])
        for i in range(len(df)):
            for j in range(0,2):
                words = str(df.iloc[i,j])
                item = QTableWidgetItem(words)
                tablelist.setItem(i,j,item)
                if words.isalpha():
                    self.webviewerlist[value*6+i].load(QUrl('https://www.youtube.com/results?search_query='+words))
        tablelist.itemDoubleClicked.connect(self.openUrl)

    def openUrl(self,item):
        if item.text().isalpha():
            webbrowser.open('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+item.text())


if __name__ == "__main__" :
    sys.setrecursionlimit(5000)
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
