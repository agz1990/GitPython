from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class DigiClock(QLCDNumber):
    def __init__(self, parent=None):
        super(DigiClock, self).__init__(parent)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.blue)
        self.setPalette(p)

        self.dragPosition = None

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.5)

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.showTime)
        timer.start(1000)

        self.showColon = True
        self.showTime()
        self.resize(150, 60)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        if event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("mm:ss")
        if self.showColon:
            text = text[0:2] + ":" + text[3:]
            self.showColon = False
        else:
            text = text[0:2] + " " + text[3:]
            self.showColon = True
        self.display(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = DigiClock()
    form.show()
    app.exec_()
    pass
