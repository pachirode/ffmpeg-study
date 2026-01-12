import random
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hello = ["你好，世界！", "Hello world!"]

        self.resize(800, 600)

        self.button = QtWidgets.QPushButton("Click me")
        self.text = QtWidgets.QLabel("Hello world", alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self) -> None:
        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
