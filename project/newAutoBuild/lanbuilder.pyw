# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from excelInput import ExcleInput, Desktop
from ui_interface import Ui_lang
import os
import sys
from pickle import FALSE


def converUI():
    import os
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.ui'):
                os.system('pyuic.py -o ui_%s.py %s' % (file.rsplit('.', 1)[0], file))
            elif file.endswith('.qrc'):
                os.system('pyrcc4 -o %s_rc.py %s -py3' % (file.rsplit('.', 1)[0], file))
# converUI()

class AutoBuildLanguage(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ei = None
        self.Ukeys = {}
        self.initUI()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.ui = Ui_lang()
        self.ui.setupUi(self)

        self.ui.openXlsBtn.setEnabled(False)
        QtGui.QToolTip.setFont(QtGui.QFont("Times", 10))
        self.ui.langGroupBoxGL = QtGui.QGridLayout(self.ui.langGroupBox)
        self.ErrorTextEdit = QtGui.QTextEdit()
        self.ErrorTextEdit.keyPressEvent = self.keyPressEvent
        self.initErrorTextEdit()
        self.ui.destFileName.setText('NewArch.xls')

        # 关联信号与槽
        self.ui.procTarBtn.clicked.connect(self.procTar)
        self.ui.procTextBtn.clicked.connect(self.procText)
        self.ui.procCheckBtn.clicked.connect(self.procCheck)
        self.ui.openXlsBtn.clicked.connect(self.openXlsObj)
        self.ui.reloadBtn.clicked.connect(self.reload)
        self.ui.selectXlsBtn.clicked.connect(self.selectXLS)
        self.ui.selectOutDir.clicked.connect(self.selectDestDir)
        self.ui.destFileName.textChanged.connect(self.initEi)
#         images = QtGui.QIcon(r':\res\rar2.png')
#         self.ui.procTarBtn.setIcon(QtGui.QIcon(r':\res\rar2.png'))
        self.ui.outputDir.setText(Desktop)
        self.ui.outputDir.setToolTip("目标路径:<b>%s</b> " % Desktop)

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def selectXLS(self):
        xls = os.path.abspath(QtGui.QFileDialog.getOpenFileName(self, '选择excel文件', filter = '*.xls'))
        self.ui.destFileName.setText(xls)
        shortname, extendsion = os.path.splitext(xls)
        if extendsion != '.xls' or not os.path.isfile(xls):
            self.ui.destFileName.setText('<请重新选择表格路径>')
            QtGui.QMessageBox.warning (self, "出错啦..", '请查看输入表格路径是否正确...')
            return
    def ShowErrorMsg(self, str):
        QtGui.QMessageBox.warning (self, "出错啦..", str)

    def openXlsObj(self):
        xlsName = self.ui.destFileName.text()
        if os.system(xlsName) is not 0:
            QtGui.QMessageBox.warning (self, "打开Excel文件失败", '请检查Excle:%s 文件是否存在，或已经打开' % xlsName)

    def reload(self):
        xlsName = self.ui.destFileName.text()
        self.initEi(xlsName)
        if self.ErrorTextEdit.isHidden():
            QtGui.QMessageBox.information(self, '从新加载成功', '重新加载语言文件表成功！')
#                 print('self.ErrorTextEdit.isHidden()')
        else :
#             print('re check the xls file...')
            self.ui.procCheckBtn.click()


    def initEi(self, xlsName):
        self.ui.destFileName.setToolTip("目标文件:<b>%s</b> " % xlsName)
        shortname, extendsion = os.path.splitext(xlsName)
        if extendsion != '.xls' or not os.path.isfile(xlsName):
            return
        try:
            self.ei = ExcleInput(xls = xlsName, msgHandle = self.ShowErrorMsg)
            self.UkeysStateChange()
            self.initSelectLanguageGroup()
        except ValueError:
            return

    def procCheck(self):
        self.ei.outKeys = self.getCheckkeysByUkeys()
        self.ErrorTextEdit.clear()
        self.ei.ReportErr(self.UI_Report)


    def getCheckkeysByUkeys(self):
        keysOrder = self.ei.keyNameOrder
        return ''.join([ key for key in keysOrder \
                        if key in self.Ukeys and self.Ukeys[key].isChecked()])
    def procTar(self):

        dest = self.ui.outputDir.text()
        keys = self.getCheckkeysByUkeys()
        try:
            self.ei.ProcTar(keys, dest)
#             "中文".encode(encoding='cp1256', errors='strict')
            QtGui.QMessageBox.information(self, "OK", '执行成功...')
        except Exception as e:
#             print('::::', e)
            QtGui.QMessageBox.warning (self, "出错啦..", str(e))
            raise e

    def procText(self):

        dest = self.ui.outputDir.text()
        keys = self.getCheckkeysByUkeys()
        try:
            self.ei.ProcText(keys, dest)
#             "中文".encode(encoding='cp1256', errors='strict')
            QtGui.QMessageBox.information(self, "OK", '执行成功...')
        except Exception as e:
#             print('::::', e)
            QtGui.QMessageBox.warning (self, "出错啦..", str(e))
            raise e

    def initErrorTextEdit(self):
        TextEdit = self.ErrorTextEdit

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        TextEdit.setPalette(palette)

#         font = TextEdit.font()
#         fm = QtGui.QFontMetrics(font)
        TextEdit.setGeometry(200, 200, 480 + 30, 480)

    def UI_Report(self, keys, outKeys):
        TextEdit = self.ErrorTextEdit
        TextEdit.setTextColor(QtCore.Qt.green)
        out = TextEdit.append
#         out('\n\n')
        out('=' * 80)
        out('##Begin ReportErr: -*- %s -*-... ' % self.ei.xlsName)
        for key in outKeys:
            emsgs = self.ei.getErrMsgByKey(key)
            if len(emsgs):
                for msg in emsgs:
                    if msg['hint'] != ExcleInput.FormatErrorType['comment'][1]\
                    and msg['locate'][1] > 1:  # errRowNum < 2 每列数据第 0 跟第1 保留不做字段显示
                        out('  [%s:%3d] *** %s *** %s' \
                              % (msg['locate'][0], msg['locate'][1], msg['hint'], msg['msg']))
#                 out('\n')
        out('=' * 80)
        TextEdit.show()

    def UkeysStateChange(self, i = 0):
        if len(self.getCheckkeysByUkeys()) == 0:
            self.ui.procTarBtn.setEnabled(False)
            self.ui.procTextBtn.setEnabled(False)
        else:
            self.ui.procTarBtn .setEnabled(True)
            self.ui.procTextBtn.setEnabled(True)

    def addCheckBox(self, key, clicked = False):
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        icon = QtGui.QIcon()
        lanName = 'LANGUAGE.' + key
        try:
            lanName = ExcleInput.key2Name[key]
        except KeyError:
            pass

        icon.addPixmap(QtGui.QPixmap(":/key/res/keypng/%s.png" % lanName), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        checkBox = QtGui.QCheckBox(lanName, self.ui.langGroupBox)
        et = "Encode(%s):<b>%s</b> " % (key, self.ei.getEncodeTypeBykey(key).upper())
        checkBox.setToolTip(et)
        checkBox.setFont(font)
        checkBox.setIconSize(QtCore.QSize(20, 20))
        checkBox.setIcon(icon)
        checkBox.clicked.connect(self.UkeysStateChange)

        if clicked:
            checkBox.click()
        self.Ukeys[key] = checkBox
        self.UkeysStateChange()


    def initSelectLanguageGroup(self):

        lastCheckedkeys = self.getCheckkeysByUkeys()

        if len(lastCheckedkeys) == 0:
            lastCheckedkeys = 'SE'

        GridLayout = self.ui.langGroupBoxGL
        for key in self.Ukeys:
            checkBox = self.Ukeys[key]
            GridLayout.removeWidget(checkBox)
            checkBox.hide()
            checkBox.clicked.disconnect(self.UkeysStateChange)
            checkBox.deleteLater()
        self.Ukeys = {}

        for key in self.ei.keyNameOrder:
            self.addCheckBox(key, key in lastCheckedkeys)

        for i, key in enumerate(self.ei.keyNameOrder):
            GridLayout.addWidget(self.Ukeys[key], i // 3, i % 3)

    def selectDestDir(self):
        dest = QtGui.QFileDialog.getExistingDirectory(self, '选择目标路径')
        if len(dest):
            self.ui.outputDir.setText(dest)
            self.ui.outputDir.setToolTip("目标路径:<b>%s</b> " % dest)

    def keyPressEvent(self, event):

        if event.key() >= ord('A') and event.key() <= ord('z'):
                    print(chr(event.key()))
        if event.key() == QtCore.Qt.Key_Escape:
            self.ErrorTextEdit.hide()

        if event.key() == QtCore.Qt.Key_F5:
            self.reload()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("res/简体中文.png"))
    app.processEvents()
    widget = AutoBuildLanguage()
    widget.show()
    splash.finish(widget)
    sys.exit(app.exec_())





