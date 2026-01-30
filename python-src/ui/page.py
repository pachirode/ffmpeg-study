import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget


class Page(QWidget):
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

        self.layout = QVBoxLayout(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Page()
    window.show()
    sys.exit(app.exec())
