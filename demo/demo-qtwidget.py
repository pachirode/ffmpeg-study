import sys
from pprint import pprint

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Slot, Qt


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qwidget Demo")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        self.red = QtWidgets.QWidget(self)
        green = QtWidgets.QWidget(self)
        blue = QtWidgets.QWidget(self)

        self.red.resize(100, 100)
        self.red.setStyleSheet("background-color: rgb(255, 0, 0);border-radius: 50px;")
        self.red.move(300, 100)

        green.resize(100, 100)
        green.setStyleSheet("background-color: rgb(0, 255, 0);border-radius: 50px;")
        green.move(400, 100)

        blue.resize(100, 100)
        blue.setStyleSheet("background-color: rgb(0, 0, 255);border-radius: 50px;")
        blue.move(500, 100)

        self.test_resize()
        self.test_size()
        self.test_position()
        self.test_margin()
        self.test_child()
        self.test_visible()
        self.test_level()
        self.test_focus()
        self.test_focus_policy()
        self.test_cursor()

    def test_resize(self):
        btn = QtWidgets.QPushButton("Resize", self)
        btn.move(100, 300)
        label = QtWidgets.QLabel("test", self)
        label.move(0, 100)

        def test_slot():
            new_content = label.text() + " test"
            label.setText(new_content)
            label.adjustSize()
            self.adjustSize()

        btn.clicked.connect(test_slot)
        self.label = label

    def test_size(self):
        print(self.height(), self.width(), self.size())

    def test_position(self):
        print(self.x(), self.y())

    def test_margin(self):
        self.label.setContentsMargins(100, 200, 0, 0)
        print(self.label.contentsMargins())
        print(self.label.contentsRect())

    def test_child(self):
        pprint(self.children())
        print(self.childAt(100, 300))
        print(self.childrenRect())  # 所有子控件组成的矩形，被隐藏的除外

    def test_visible(self):
        @Slot()
        def test_slot() -> None:
            if self.label.isVisible():
                self.label.setVisible(False)
            else:
                self.label.setVisible(True)

        button_1 = QtWidgets.QPushButton("Visible", self)
        button_1.move(100, 200)
        button_1.clicked.connect(test_slot)

    def test_level(self):
        self.test_widget = QtWidgets.QWidget(self)
        self.test_widget.resize(100, 100)
        self.test_widget.setStyleSheet("background-color: rgb(255, 255, 0);border-radius: 50px;")
        self.test_widget.move(300, 100)

        button = QtWidgets.QPushButton("Level", self)

        @Slot()
        def test_slot():
            self.test_widget.stackUnder(self.red)

        button.clicked.connect(test_slot)

    def test_focus(self):
        # 只有当前获得焦点的控件才能和用户交互
        le = QtWidgets.QLineEdit(self)
        le.move(150, 300)

        cbb = QtWidgets.QComboBox(self)
        cbb.addItem("1")
        cbb.addItem("2")
        cbb.move(500, 100)

        btn = QtWidgets.QPushButton("Focus", self)
        btn.move(300, 450)
        btn.clicked.connect(lambda: print(btn.hasFocus()))
        btn.clicked.connect(lambda: print(le.hasFocus()))
        btn.clicked.connect(lambda: print(self.focusWidget()))

    def test_focus_policy(self):
        self.red.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.test_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTabOrder(self.red, self.test_widget)

    def test_cursor(self):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
