from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys



app = QApplication(sys.argv)
btn = QPushButton('')
btn.setIcon(QIcon("image/简体中文.png"))
btn.setIconSize(QSize(75, 75))
btn.setMinimumSize(QSize(75, 75))
btn.setMaximumSize(QSize(75, 75))
btn.setFlat(True)
btn.setWindowFlags(Qt.FramelessWindowHint)
btn.show()


animation = QPropertyAnimation (btn, "geometry")
animation.setDuration(10000);
animation.setStartValue(QRect(0, 0, 100, 30));
animation.setEndValue(QRect(1360, 0, 100, 30));
animation.setEasingCurve(QEasingCurve.OutBounce);
animation.start()
sys.exit(app.exec_())
if __name__ == '__main__':
    pass
