# coding = utf-8
# !/users/Jiao/venv1/bin/python
# Copyright 2018 Jiao. All right Reserved.
# Author: Jiao.1985@foxmail.com
# 5-3-QListView.py 2018/1/19 下午3:34

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView, QMessageBox
from PyQt5.QtCore import QStringListModel


# from PyQt5.QtGui import *

class ListViewDemo(QWidget):
    def __init__(self):
        super(ListViewDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QListView Demo')

        self.qList = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        self.listView = QListView()
        self.strModel = QStringListModel()
        self.strModel.setStringList(self.qList)
        self.listView.setModel(self.strModel)

        self.listView.clicked.connect(self.showSelectedItem)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.listView)

        self.setLayout(mainLayout)

    def showSelectedItem(self,qModelIndex):
        # 我靠这里好神奇!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # 信号槽中没有传递参数,这里哪里冒出来一个位置参数
        # 这个参数还知道自己是个QModelIndex类对象,太神奇了!
        QMessageBox.information(self, '显示', '你选择了' + self.qList[qModelIndex.row()])
        #个人猜测可能是ListView的clicked信号发射时,内置了一个QModelIndex类型的参数
        #查询技术文档:证实了我的猜想:见下面
        #void QAbstractItemView :: clicked（const QModelIndex＆index）


if __name__ == '__main__':
    app = QApplication(sys.argv)
    listViewDemo = ListViewDemo()
    listViewDemo.show()
    sys.exit(app.exec_())
