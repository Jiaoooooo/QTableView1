# coding = utf-8
# !/users/Jiao/venv1/bin/python
# Copyright 2018 Jiao. All right Reserved.
# Author: Jiao.1985@foxmail.com
# 5-2-TableView-Fuctions-Test.py 2018/1/18 下午4:04

import sys, random
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QApplication, QMenu
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableDemo(QWidget):
    def __init__(self):
        super(TableDemo, self).__init__()
        self.setWindowTitle('TableView Demo')
        self.resize(600, 500)

        modelVerticalTitleLabelList = ['A', 'B', 'C', 'D', 'E']
        modelHorizontialTitleLabelList = ['甲', '乙', '丙', '丁', '戊', '已']

        self.model = QStandardItemModel(5, 5)
        self.model.setHorizontalHeaderLabels(modelVerticalTitleLabelList)
        self.model.setVerticalHeaderLabels(modelHorizontialTitleLabelList)
        for i in range(5):
            for j in range(5):
                item = QStandardItem(str(i + j))
                self.model.setItem(i, j, item)

        self.tabletView = QTableView()
        self.tabletView.setModel(self.model)

        self.tabletView.horizontalHeader().setStretchLastSection(True)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabletView)

        self.testRowColumn()

        self.setLayout(mainLayout)

    def testRowColumn(self):
        # 用rowAt()和columnAt(),返回一个坐标在table中的行和列的序号
        x, y = 100, 200
        row_at_x = self.tabletView.rowAt(x)
        column_at_y = self.tabletView.columnAt(y)
        print('坐标(%d,%d)在表格中是第%d行,第%d列' % (x, y, row_at_x + 1, column_at_y + 1))
        # 如果(x,y)不在表格内,函数返回值是-1

        # setRowHeight,setColumnWidth:可以设置行高'列宽
        self.tabletView.setRowHeight(1, 50)
        self.tabletView.setColumnWidth(1, 150)
        # <int> columnWidth():返回指定列的宽度
        # <int> rowHeight():返回指定行的高度
        print('第(2,2)单元格的列宽,行高为为:%d,%d(像素)' % (self.tabletView.columnWidth(1), self.tabletView.rowHeight(1)))

        # setSpan():设定指定行和列的行跨度和列跨度
        self.tabletView.setSpan(2, 2, 2, 2)
        # <int> rowSpan():返回指定行的位置的行跨度
        # <int> columnSpan:返回指定(row,column)的列跨度
        print('第(3,3)单元格的的行和列跨度为(%dx%d)' % (self.tabletView.columnSpan(2, 2), self.tabletView.rowSpan(2, 2)))

        # setCornerButtonEnable():设置是否启用左上角的按钮
        # 此按钮(用来全选整个表格),默认是启用的
        self.tabletView.setCornerButtonEnabled(False)  # 此时,左上角的按钮将不再起作用

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QMenu(self)
        hideMenu = menu.addAction('&Hide')
        hideMenu.triggered.connect(self.hideCurrentColumn)

        menu.exec_(QContextMenuEvent.globalPos())

    def hideCurrentColumn(self):
        print('第%d列被隐藏了!'%self.tabletView.currentIndex().column())
        self.tabletView.setColumnHidden(self.tabletView.currentIndex().column(),True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tableDemo = TableDemo()
    tableDemo.show()
    sys.exit(app.exec_())
