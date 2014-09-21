#!/usr/bin/env python
# coding=utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep

class DBComboBoxDelegate(QItemDelegate):

    def __init__(self, comboModel, parent=None):
        print("1")
        QItemDelegate.__init__(self, parent)
        self.comboModel = comboModel

    def __createComboView(self, parent):
        view = QTableView(parent)
        view.setModel(self.comboModel)
        view.setAutoScroll(False)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.resizeColumnsToContents()
        view.resizeRowsToContents()
        view.setMinimumWidth(view.horizontalHeader().length())
        return view

    def createEditor(self, parent, option, index):
        print("2")
        combo = QComboBox(parent)
        # !! The important part: First set the model, then the view on the combo box
        combo.setModel(self.comboModel)
        # combo.setModelColumn(1)
        combo.setView(self.__createComboView(parent))
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        print("xxxx")
        if editor.currentIndex() >= 0:
            realidx = editor.model().index(editor.currentIndex(), 0)  # 确保取第一列的值
            value = editor.model().data(realidx)
            model.setData(index, value)



class ButtonDelegate(QItemDelegate):

    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):

        pass
#     def setEditorData(self, editor, index):
#         value = index.model().data(index, Qt.EditRole)
#         editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):

        pass

    def editorEvent(self, event, model, option, index):
        print("editorEvent")

    def paint(self, painter, option, index):

        value = int(index.data())
        print(type(value))
        progressBarOption = QStyleOptionProgressBar()
        progressBarOption.rect = option.rect;
        progressBarOption.minimum = 0;
        progressBarOption.maximum = 100;
        progressBarOption.progress = int(value);
        progressBarOption.text = "%d%%" % int(value)
        progressBarOption.textVisible = True;
        progressBarOption.textAlignment = Qt.AlignHCenter;

        QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarOption, painter)



###############################################################################


class MainForm(QWidget):

    def __init__(self):
        super(MainForm, self).__init__()
        self.ts = []
        self.count = 0
        self.model = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 400, 200)
        table = QTableView(self)
        self.gird = QGridLayout(self)
        self.gird.addWidget(table)

        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        comboModel = QStandardItemModel(4, 2, table)
        comboModel.setHorizontalHeaderLabels(['Name', 'Description'])
        comboModel.setData(comboModel.index(0, 0), (u'树袋熊'))
        comboModel.setData(comboModel.index(0, 1), (u'生活在树上的熊'))
        comboModel.setData(comboModel.index(1, 0), (u'松鼠'))
        comboModel.setData(comboModel.index(1, 1), (u'可爱的松树精灵'))
        comboModel.setData(comboModel.index(2, 0), (u'大眼猴'))
        comboModel.setData(comboModel.index(2, 1), (u'这猴眼睛真大'))
        comboModel.setData(comboModel.index(3, 0), (u'猫头鹰'))
        comboModel.setData(comboModel.index(3, 1), (u'夜的精灵正站在树枝上'))


        model = QStandardItemModel(2, 3, table)
        model.setHorizontalHeaderLabels([ '用户', '进程状态', '进度' ])
        model.setData(model.index(0, 0), (u'松鼠'))
        model.setData(model.index(0, 2), 80)
        model.setData(model.index(0, 1), (u'12'))
        model.setData(model.index(1, 2), 80)
        model.setData(model.index(2, 2), 80)
#         table.setCellWidget(1, 0, QPushButton("按键", self))

        self.table = table
        self.model = model

        table.setModel(model)
        table.setItemDelegateForColumn(0, DBComboBoxDelegate(comboModel, table))
        table.setItemDelegateForColumn(2, ButtonDelegate(table))
        table.horizontalHeader().setStretchLastSection(True)
        self.setWindowTitle('Grid + Combo Testing')


        self.timer = QTimer(self);
        self.connect(self.timer, SIGNAL('timeout()'), self.update);
        self.timer.start(200);

    def update(self):
        if  self.count < 100:

            self.count += 1
#             self.model.setItem(2, 1, QStandardItem(str(self.count)))
            self.model.appendRow([QStandardItem(str(self.count)), QStandardItem(str(self.count)), QStandardItem(str(self.count))])

            self.table.selectRow (self.table.rowCount())
            print(self.count)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    ui = MainForm()
    ui.show()

    sys.exit(app.exec_())
