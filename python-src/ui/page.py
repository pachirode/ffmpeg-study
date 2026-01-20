import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTableWidget, QVBoxLayout, QWidget


class Page(QWidget):
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.back_btn = None

        self.top_bar()

    def top_bar(self):
        bar = QHBoxLayout()
        bar.setObjectName("listPageTopBar")

        path_label = QLabel("当前文件路径", self)
        path_label.setObjectName("listPagePathLabel")

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.back_btn = QPushButton("返回上一层", self)
        self.back_btn.setObjectName("listPageBackBtn")

        bar.addWidget(self.back_btn)
        bar.addWidget(path_label)
        bar.addItem(spacer)

        self.layout.addLayout(bar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Page()
    window.show()
    sys.exit(app.exec())
