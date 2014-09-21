'''
Created on 2013年9月28日

@author: Administrator
'''

from PyQt4 import QtGui, QtCore
import sys

class Palette(QtGui.QWidget):
    sigPenChaged = QtCore.pyqtSignal(QtGui.QPen)
    sigBrushChaged = QtCore.pyqtSignal(QtGui.QBrush)
    def __init__(self):
        super(Palette, self).__init__()
        self.initUI()

    def initUI(self):
        self.penColorCombox = self.createColorComBox()
        self.styleComBox = self.createStyleComBox()
    @QtCore.pyqtSlot()
    def penChaged(self):
        pass

    @QtCore.pyqtSlot()
    def brushChaged(self):
        pass

    def createColorComBox(self):
        cb = QtGui.QComboBox
        pix = QtGui.QPixmap(16, 16)
        pt = QtGui.QPainter(pix)

        pt.fillRect(0, 0, 16, 16, QtCore.Qt.black)
        icon = QtGui.QIcon(pix)
        cb.addItem('str', userData=None)

#         pt.fillRect(0, 0, 16, 16, QtCore.Qt.red)
#         cb.addItem(icon, 'red', QtCore.Qt.red)
#
#         pt.fillRect(0, 0, 16, 16, QtCore.Qt.green)
#         cb.addItem(icon, 'green', QtCore.Qt.green)
#
#         pt.fillRect(0, 0, 16, 16, QtCore.Qt.yellow)
#         cb.addItem(icon, 'yellow', QtCore.Qt.yellow)
#
#         pt.fillRect(0, 0, 16, 16, QtCore.Qt.cyan)
#         cb.addItem(icon, 'cyan', QtCore.Qt.cyan)
#
#         pt.fillRect(0, 0, 16, 16, QtCore.Qt.magemta)
#         cb.addItem(icon, 'magemta', QtCore.Qt.magemta)
        return cb
    def createStyleComBox(self):
        StyleComBox = QtGui.QComboBox
#         StyleComBox.setItemDelegate(QtGui.QItemDelegate(StyleComBox))

        StyleComBox.addItem('Solid', QtCore.Qt.Solid)
        StyleComBox.addItem('Dash', QtCore.Qt.DashLine)
        StyleComBox.addItem('Dot', QtCore.Qt.DotLine)
        StyleComBox.addItem('Dash Dot', QtCore.Qt.DashDotLine)
        StyleComBox.addItem('Dash Dot Dot', QtCore.Qt.DashDotDotLine)
        StyleComBox.addItem('None', QtCore.Qt.NoPen)

# class QPenStyleDelegate(QtGui.QAbstractItemDelegate):
#     def __init__(self):
#         super(QPenStyleDelegate, self).__init__()
#
#     @staticmethod
#     def paint(QPainter,QStyleOption,QModelIndex):
#         text = QtGui



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    pt = Palette()
    pt.show()
    sys.exit(app.exec_())
    pass
