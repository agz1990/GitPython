#!/usr/bin/python
# -*- coding: utf-8 -*-

# checkbox.py

from PyQt4 import QtCore, QtGui
import User
from ThreadWeb import MiThreadWeb
import sys
from time import sleep


users = User.WebUsers('u.txt')

def GetNextUser():
    return users.getNextUser()


class MiThreadUi(QtCore.QThread):
    def __init__(self, parent, gird, tid):
        super(MiThreadUi, self).__init__(parent)
        self.processbar = QtGui.QProgressBar()
        self.startbtn = QtGui.QPushButton("启动线程")
        self.tid = tid
        self.label = QtGui.QLabel("线程：%d" % self.tid)
        self.status = QtGui.QLabel("准备就绪")
        self.initUI(tid, gird)
        self.web = MiThreadWeb(self.SetCurStatus)



    def initUI(self, tid, grid):
        grid.addWidget(self.label, tid, 0)
        grid.addWidget(self.status, tid, 1)
        grid.addWidget(self.processbar, tid, 2)
        grid.addWidget(self.startbtn, tid, 3)
        self.processbar.setMaximum(100)

        self.connect(self.startbtn, QtCore.SIGNAL('clicked()'), self.start)
        self.connect(self, QtCore.SIGNAL('finished ()'), self.start)

    def run(self):
        print ("run!!")
        user = GetNextUser()
        if user == None:
            self.disconnect(self, QtCore.SIGNAL('finished ()'), self.start)
            if self.web.dr:
                self.web.dr.quit()
            return
        self.web.setUserInfo(user)
        self.SetDriverGeometryByTid(self.web)
        if self.web.login() == False:
            return
        if self.web.fillUserInfo():
            self.web.waitforInputCaptcha()

        self.web.logout()
        self.msleep(2000)


    def SetCurStatus(self, status):
        self.processbar.setValue(status[0])
        self.status.setText(status[1])


    def SetDriverGeometryByTid(self, web):
        screen = QtGui.QDesktopWidget().screenGeometry()
        maxcol = 3
        maxrow = 2
        drw = screen.width() / maxcol
        drh = (screen.height() - 100) / maxrow
        drx = (self.tid % maxcol) * drw
        dry = (self.tid // maxcol) * drh
        print ("tid=%d   x=%d y=%d w=%d h=%d" % (self.tid , drx, dry , drw, drh))
        web.setDriverRect(drx, dry, drw, drh)
        pass

    def refreshAuthNunber(self):
        self.web.refreshAuthNunber()


class UOrder(QtGui.QWidget):

    def __init__(self):
        super(UOrder, self).__init__()
        self.ts = []
        self.initUI()

    def initUI(self):

        self.setGeometry(400, 300, 400, 240)
        grid = QtGui.QGridLayout(self)
        for iCnt in range(6):
            miobj = MiThreadUi(self, grid, iCnt)
            self.ts.append(miobj)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = UOrder()
    ex.show()
    app.exec_()
