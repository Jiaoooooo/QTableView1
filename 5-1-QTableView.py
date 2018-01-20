import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QTableView, QVBoxLayout, QHeaderView, QGridLayout, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit)
from PyQt5.QtCore import QEvent, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator


class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.setWindowTitle('TableView示例')
        self.resize(600, 600)
        self.model = QStandardItemModel(4, 4)
        '''
        QStandardItemModel:'Q标准化模型'类提供了一个用于存储定制数据的通用模型。 
        'Q标准化模型'可以作为标准Qt数据类型的存储库。
        它是模型/视图类之一，也是Qt模型/视图框架的一部分。 
        'Q标准化模型'提供了一种经典的基于项目的方法来处理模型。
        'Q标准化模型'提供了Q标准化模型中的项目。 
        'Q标准化模型'实现了QAbstractItemModel接口，这意味着该模型可以用于提供支持该接口
        的任何视图中的数据(如QListView、QTableView和QTreeView，以及自定义的类型)。

        当您需要一个列表或树时，通常会创建一个空的'q标准化模型'，
        并使用appendRow()将项目添加到模型中，并使用item()来访问项目。
        如果您的模型代表一个表，那么您通常将表的维度传递给'q标准化模型'构造函数，
        并使用setItem()将条目放置到表中。您还可以使用setRowCount()和setColumnCount()来改变模型的维度。
        要插入项，请使用insertRow()或insertColumn()，并删除项目，使用removeRow()或removeColumn()。
        '''
        tableTittleList = ['行数', '针数', '次数', '收针']
        self.model.setHorizontalHeaderLabels(tableTittleList)
        dataList = ['5', '7', 'dd', '90', '34', '', '1', '33', '45', '31', '34', '12', '89', '12', '1', '513']

        for [n, (i, j)] in enumerate([(i, j) for i in range(4) for j in range(4)]):
            item = QStandardItem(dataList[n])
            self.model.setItem(i, j, item)

        self.tabletView = QTableView()
        self.tabletView.setModel(self.model)
        # 设置tableView的最后一列会跟随窗口水平伸缩
        self.tabletView.horizontalHeader().setStretchLastSection(True)
        # 设置tableView的所有列都会跟谁窗口伸缩
        self.tabletView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.stateLabel = QLabel('Size:(0x0),Mouse:(0,0)')
        self.setStateLabel()

        self.tabletView.clicked.connect(self.setStateLabel)

        # 添加一些按钮:删除行,插入行,清空行,
        delBtn = QPushButton('删除')
        insertRowBtn = QPushButton('插入')
        clrBtn = QPushButton('清除')

        # 添加2个lineEdit和一个btn 用来查询用户指定的位置的数据
        rowLine = QLineEdit()
        colLine = QLineEdit()
        findBtn = QPushButton('查询')
        # 创建一个整数验证器,用来限制输入的数据为0~300的整数
        intValidator = QIntValidator()
        intValidator.setRange(0, 300)
        # 添加信号槽
        rowLine.setValidator(intValidator)
        colLine.setValidator(intValidator)
        rowLine.setPlaceholderText('输入查询的行数')
        colLine.setPlaceholderText('输入要查询的列数')
        findBtn.clicked.connect(lambda: self.findData(int(rowLine.text()), int(colLine.text())))

        # 为按钮添加信号槽
        delBtn.clicked.connect(self.removeRow)
        insertRowBtn.clicked.connect(self.insertRow)
        clrBtn.clicked.connect(self.clearSelectedItem)

        btnGridLayout = QGridLayout()
        btnGridLayout.addWidget(delBtn, 0, 0)
        btnGridLayout.addWidget(insertRowBtn, 0, 1)
        btnGridLayout.addWidget(clrBtn, 0, 2)
        btnGridLayout.addWidget(rowLine, 1, 0)
        btnGridLayout.addWidget(colLine, 1, 1)
        btnGridLayout.addWidget(findBtn, 1, 2)

        # 创建查询框和查询按钮
        searchLine = QLineEdit()
        columnNumLine = QLineEdit()
        searchBtn = QPushButton('搜索')
        columnNumLine.setValidator(intValidator)
        # 为搜索按钮添加槽
        searchBtn.clicked.connect(lambda: self.searchData(searchLine.text(), columnNumLine.text()))

        btnGridLayout.addWidget(searchLine, 2, 0)
        btnGridLayout.addWidget(columnNumLine, 2, 1)
        btnGridLayout.addWidget(searchBtn, 2, 2)

        layout = QVBoxLayout()
        layout.addWidget(self.tabletView)
        layout.addLayout(btnGridLayout)
        layout.addWidget(self.stateLabel)
        self.setLayout(layout)

    def setStateLabel(self,p_arg):
        print(p_arg)
        '''获取当前tableView的大小和鼠标点击的位置,以及选择和框选区大小'''
        selectedIndexes = self.tabletView.selectedIndexes()

        stateList = [self.model.rowCount(), self.model.columnCount(), self.tabletView.currentIndex().row(),
                     self.tabletView.currentIndex().column()]
        self.stateLabel.setText(
            'Size:(%dx%d),Mouse:(%d,%d)' % (stateList[0], stateList[1], stateList[2] + 1, stateList[3] + 1))
        print(stateList)

    def insertRow(self):
        if self.model.rowCount() < 300:
            if self.model.rowCount() == 0:
                self.model.setItem(0, QStandardItem(''))
            else:
                self.model.insertRow(self.tabletView.currentIndex().row())
            print('rowCount = ', self.model.rowCount())
        else:
            QMessageBox.warning(self, '停止', '最大支持300行数据!')

        self.setStateLabel()

    def removeRow(self):
        indexes = self.tabletView.selectedIndexes()
        rowIndexList = []
        for index in indexes:
            rowIndexList.append(index.row())
        rowIndexSet = set(rowIndexList)
        print(len(indexes), len(rowIndexList), len(rowIndexSet))
        self.model.removeRows(self.tabletView.currentIndex().row(), len(rowIndexSet))
        self.setStateLabel()

    def findData(self, n_row, n_col):
        print('开始查询第{0}行,第{1}列的数据...'.format(n_row, n_col))
        index = self.model.index(n_row - 1, n_col - 1)
        # 检查输入的数据是否超出表格范围,并检查表格内容是否为空
        if (n_row - 1) > self.model.rowCount():
            QMessageBox.critical(self, '错误', '输入的行数超过表格最大行数')
        elif (n_col - 1) > self.model.columnCount():
            QMessageBox.critical(self, '错误', '输入的列数超过表格最大列数')
        else:
            data = self.model.data(index)
            if data:
                QMessageBox.information(self, '查询', '({0},{1})位置处的数值是{2}'.format(n_row, n_col, data))
            else:
                QMessageBox.information(self, '查询', '({0},{1})位置处的数值是{2}'.format(n_row, n_col, '空的'))

    def searchData(self, data, column_num):
        # 用来在指定的column_num列找那个查找有没有data的item
        # 如果找到,返回其行数, 如果找不到,告知找不到
        column_num = int(column_num)

        dataItem = QStandardItem(data)
        indexList = self.model.findItems(data, column=column_num - 1)
        list = []
        for i in range(len(indexList)):
            list.append(indexList[i].row())
        if len(list) == 0:
            QMessageBox.information(self, '找不到', '在第{0}列中找不到\n任何值是{1}元素'.format(column_num, data))
        else:
            for i in range(len(list)):
                list[i] = list[i] + 1
            dlgText = """在第{0}列中找到了值是'{1}'的元素共<font color = red>{2}</font>个,分别在第{3}列""".format(column_num, data,
                                                                                               len(list), list)
            QMessageBox.information(self, '找到了', dlgText)

    def clearSelectedItem(self):
        indexes = self.tabletView.selectedIndexes()
        for index in indexes:
            self.model.setItem(index.row(), index.column(), QStandardItem(''))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = Table()
    table.show()
    sys.exit(app.exec_())
