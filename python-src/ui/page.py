import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTableWidget, QVBoxLayout, QWidget


class Page(QWidget):
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

        self.layout = QVBoxLayout(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Page()
    window.show()
    sys.exit(app.exec())
