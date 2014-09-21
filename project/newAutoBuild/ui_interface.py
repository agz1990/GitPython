# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Sun Jan 12 22:12:06 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_lang(object):
    def setupUi(self, lang):
        lang.setObjectName(_fromUtf8("lang"))
        lang.resize(380, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lang.sizePolicy().hasHeightForWidth())
        lang.setSizePolicy(sizePolicy)
        lang.setMaximumSize(QtCore.QSize(600, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/appIcon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        lang.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(lang)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(lang)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.procCheckBtn = QtGui.QPushButton(self.groupBox)
        self.procCheckBtn.setMinimumSize(QtCore.QSize(75, 75))
        self.procCheckBtn.setMaximumSize(QtCore.QSize(75, 75))
        self.procCheckBtn.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/abc_check.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.procCheckBtn.setIcon(icon1)
        self.procCheckBtn.setIconSize(QtCore.QSize(75, 75))
        self.procCheckBtn.setFlat(True)
        self.procCheckBtn.setObjectName(_fromUtf8("procCheckBtn"))
        self.gridLayout_2.addWidget(self.procCheckBtn, 0, 3, 1, 1)
        self.procTextBtn = QtGui.QPushButton(self.groupBox)
        self.procTextBtn.setMinimumSize(QtCore.QSize(75, 75))
        self.procTextBtn.setMaximumSize(QtCore.QSize(75, 75))
        self.procTextBtn.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/txt2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.procTextBtn.setIcon(icon2)
        self.procTextBtn.setIconSize(QtCore.QSize(75, 75))
        self.procTextBtn.setFlat(True)
        self.procTextBtn.setObjectName(_fromUtf8("procTextBtn"))
        self.gridLayout_2.addWidget(self.procTextBtn, 0, 0, 1, 1)
        self.procTarBtn = QtGui.QPushButton(self.groupBox)
        self.procTarBtn.setEnabled(True)
        self.procTarBtn.setMinimumSize(QtCore.QSize(75, 75))
        self.procTarBtn.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(12)
        self.procTarBtn.setFont(font)
        self.procTarBtn.setAutoFillBackground(True)
        self.procTarBtn.setLocale(QtCore.QLocale(QtCore.QLocale.CongoSwahili, QtCore.QLocale.DemocraticRepublicOfCongo))
        self.procTarBtn.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/rar2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.procTarBtn.setIcon(icon3)
        self.procTarBtn.setIconSize(QtCore.QSize(75, 75))
        self.procTarBtn.setFlat(True)
        self.procTarBtn.setObjectName(_fromUtf8("procTarBtn"))
        self.gridLayout_2.addWidget(self.procTarBtn, 0, 2, 1, 1)
        self.openXlsBtn = QtGui.QPushButton(self.groupBox)
        self.openXlsBtn.setEnabled(True)
        self.openXlsBtn.setMinimumSize(QtCore.QSize(75, 75))
        self.openXlsBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.openXlsBtn.setMouseTracking(False)
        self.openXlsBtn.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/excel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openXlsBtn.setIcon(icon4)
        self.openXlsBtn.setIconSize(QtCore.QSize(75, 75))
        self.openXlsBtn.setFlat(True)
        self.openXlsBtn.setObjectName(_fromUtf8("openXlsBtn"))
        self.gridLayout_2.addWidget(self.openXlsBtn, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pushButton_2.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/ftp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon5)
        self.pushButton_2.setIconSize(QtCore.QSize(75, 75))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.reloadBtn = QtGui.QPushButton(self.groupBox)
        self.reloadBtn.setEnabled(True)
        self.reloadBtn.setMinimumSize(QtCore.QSize(75, 75))
        self.reloadBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.reloadBtn.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/reload.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reloadBtn.setIcon(icon6)
        self.reloadBtn.setIconSize(QtCore.QSize(75, 75))
        self.reloadBtn.setCheckable(False)
        self.reloadBtn.setFlat(True)
        self.reloadBtn.setObjectName(_fromUtf8("reloadBtn"))
        self.gridLayout_2.addWidget(self.reloadBtn, 1, 3, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.outputDir = QtGui.QLineEdit(lang)
        self.outputDir.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputDir.sizePolicy().hasHeightForWidth())
        self.outputDir.setSizePolicy(sizePolicy)
        self.outputDir.setMaximumSize(QtCore.QSize(500, 16777215))
        self.outputDir.setObjectName(_fromUtf8("outputDir"))
        self.gridLayout.addWidget(self.outputDir, 2, 0, 1, 1)
        self.destFileName = QtGui.QLineEdit(lang)
        self.destFileName.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.destFileName.sizePolicy().hasHeightForWidth())
        self.destFileName.setSizePolicy(sizePolicy)
        self.destFileName.setMaximumSize(QtCore.QSize(500, 16777215))
        self.destFileName.setObjectName(_fromUtf8("destFileName"))
        self.gridLayout.addWidget(self.destFileName, 0, 0, 1, 1)
        self.selectOutDir = QtGui.QPushButton(lang)
        self.selectOutDir.setMaximumSize(QtCore.QSize(23, 16777215))
        self.selectOutDir.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/res/target.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectOutDir.setIcon(icon7)
        self.selectOutDir.setFlat(True)
        self.selectOutDir.setObjectName(_fromUtf8("selectOutDir"))
        self.gridLayout.addWidget(self.selectOutDir, 2, 1, 1, 1)
        self.selectXlsBtn = QtGui.QPushButton(lang)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectXlsBtn.sizePolicy().hasHeightForWidth())
        self.selectXlsBtn.setSizePolicy(sizePolicy)
        self.selectXlsBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.selectXlsBtn.setMaximumSize(QtCore.QSize(23, 16777215))
        self.selectXlsBtn.setText(_fromUtf8(""))
        self.selectXlsBtn.setIcon(icon4)
        self.selectXlsBtn.setIconSize(QtCore.QSize(23, 23))
        self.selectXlsBtn.setFlat(True)
        self.selectXlsBtn.setObjectName(_fromUtf8("selectXlsBtn"))
        self.gridLayout.addWidget(self.selectXlsBtn, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.langGroupBox = QtGui.QGroupBox(lang)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langGroupBox.sizePolicy().hasHeightForWidth())
        self.langGroupBox.setSizePolicy(sizePolicy)
        self.langGroupBox.setMinimumSize(QtCore.QSize(200, 125))
        self.langGroupBox.setMaximumSize(QtCore.QSize(500, 500))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.langGroupBox.setFont(font)
        self.langGroupBox.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.langGroupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.langGroupBox.setFlat(False)
        self.langGroupBox.setCheckable(False)
        self.langGroupBox.setObjectName(_fromUtf8("langGroupBox"))
        self.gridLayout_3.addWidget(self.langGroupBox, 2, 0, 1, 1)

        self.retranslateUi(lang)
        QtCore.QMetaObject.connectSlotsByName(lang)

    def retranslateUi(self, lang):
        lang.setWindowTitle(_translate("lang", "LanguageTools", None))
        self.groupBox.setTitle(_translate("lang", "Tools", None))
        self.procCheckBtn.setToolTip(_translate("lang", "检查语言表数据", None))
        self.procTextBtn.setToolTip(_translate("lang", "<html><head/><body><p><span style=\" font-weight:600;\">生成文本文件</span></p></body></html>", None))
        self.procTarBtn.setToolTip(_translate("lang", "<html><head/><body><p><span style=\" font-weight:600;\">生成压缩文件</span></p></body></html>", None))
        self.openXlsBtn.setToolTip(_translate("lang", "打开源语言表", None))
        self.pushButton_2.setToolTip(_translate("lang", "获取远程Excle文件(暂未实现)", None))
        self.reloadBtn.setToolTip(_translate("lang", "重新加载语言表", None))
        self.langGroupBox.setTitle(_translate("lang", "Choose Language", None))

import interface_rc