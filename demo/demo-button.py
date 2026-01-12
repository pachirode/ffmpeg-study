import sys

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Slot, Qt


class MyAbstractImpButton(QtWidgets.QAbstractButton):
    # 重写父类方法
    def paintEvent(self, e, /) -> None:
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(20, 154, 151), 5)
        painter.setPen(pen)
        painter.drawText(20, 70, self.text())
        painter.drawEllipse(5, 5, 100, 120)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setup_ui()
        self.test_signal()
        self.test_auto_repeat()
        self.test_shortcut()
        self.test_exclusive()

    def setup_ui(self) -> None:
        self.btn = MyAbstractImpButton(self)
        self.btn.setText("自定义按钮")
        self.btn.resize(150, 150)
        self.btn.move(100, 100)

    def test_signal(self) -> None:
        self.btn.clicked.connect(lambda: print("按钮被点击"))
        self.btn.pressed.connect(lambda: print("按钮被按下"))
        self.btn.released.connect(lambda: print("按钮被释放"))
        self.btn.toggled.connect(lambda: print("按钮状态发生改变"))
        self.btn.setCheckable(True)

    def test_auto_repeat(self):
        self.btn.setAutoRepeat(True)
        self.btn.setAutoRepeatDelay(1000)
        self.btn.setAutoRepeatInterval(1000)

        print(self.btn.autoRepeat())
        print(self.btn.autoRepeatDelay())
        print(self.btn.autoRepeatInterval())

    def test_shortcut(self):
        self.btn.setShortcut(Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_A)
        print(self.btn.shortcut())

    def test_exclusive(self):
        btn1 = QtWidgets.QCheckBox("1", self)
        btn2 = QtWidgets.QCheckBox("2", self)
        btn3 = QtWidgets.QCheckBox("3", self)
        btn1.move(30, 30)
        btn2.move(40, 40)
        btn3.move(50, 50)

        btn1.setAutoExclusive(True)
        btn2.setAutoExclusive(True)
        btn3.setAutoExclusive(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
