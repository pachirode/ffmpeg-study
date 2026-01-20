import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication

from edit import EditPage
from list import ListPage
from media import MediaPage


class MediaManager(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MediaManager')
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mediaManager")
        self.feature_stack = QStackedWidget(self.main_widget)
        self.feature_stack.setObjectName("mainStack")

        self.edit_page = None
        self.list_page = None
        self.media_page = None

        self.setup_ui()

    def setup_ui(self):
        self.edit_page = EditPage()
        self.list_page = ListPage()
        self.media_page = MediaPage()

        self.feature_stack.addWidget(self.list_page)
        self.feature_stack.addWidget(self.edit_page)
        self.feature_stack.addWidget(self.media_page)

        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.feature_stack)
        self.setLayout(layout)

        self.feature_stack.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaManager()
    window.show()
    sys.exit(app.exec())
