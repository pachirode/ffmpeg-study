import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication, QPushButton, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout

from ui.edit import EditPage
from ui.list import ListPage
from ui.media import MediaPage
from ui.image import ImagePage
from utils.file_path import FilePathUtils
from utils.file_source import FileSourceUtils
from utils.log import LoggerManager

logger = LoggerManager.get_logger()


class MediaManager(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MediaManager')
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mediaManager")
        self.feature_stack = QStackedWidget(self.main_widget)
        self.feature_stack.setObjectName("mainStack")
        self.path_util = FilePathUtils()

        self.back_btn = None
        self.bar = None
        self.path_label = None
        self.status_label: QLabel = None

        self.edit_page: EditPage = None
        self.list_page: ListPage = None
        self.media_page: MediaPage = None
        self.image_page: ImagePage = None

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.top_bar()

        self.edit_page = EditPage()
        self.list_page = ListPage()
        self.media_page = MediaPage()
        self.image_page = ImagePage()

        self.feature_stack.addWidget(self.list_page)
        self.feature_stack.addWidget(self.edit_page)
        self.feature_stack.addWidget(self.media_page)
        self.feature_stack.addWidget(self.image_page)

        layout = QVBoxLayout(self.main_widget)
        layout.addLayout(self.bar)
        layout.addWidget(self.feature_stack)
        self.setLayout(layout)

        self.feature_stack.setCurrentIndex(0)

    def top_bar(self):
        self.bar = QHBoxLayout()
        self.bar.setObjectName("listPageTopBar")

        cwd_label = QLabel("当前文件路径: ", self)
        self.path_label = QLabel(self.path_util.get_back(), self)
        self.status_label = QLabel("", self)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.back_btn = QPushButton("返回上一层", self)
        self.back_btn.setObjectName("listPageBackBtn")

        self.bar.addWidget(self.back_btn)
        self.bar.addWidget(cwd_label)
        self.bar.addWidget(self.path_label)
        self.bar.addWidget(self.status_label)
        self.bar.addItem(spacer)

    def back_btn_clicked(self):
        self.path_label.setText(self.path_util.get_back())
        self.feature_stack.setCurrentIndex(0)
        self.status_label.setText("")

    def setup_signals(self):
        self.back_btn.clicked.connect(self.back_btn_clicked)

        self.set_list_page_signal()

    def set_list_page_signal(self):
        self.list_page.table.itemDoubleClicked.connect(self.handle_double_click)

    def handle_double_click(self, item):
        row_data = self.list_page.table.item(item.row(), 0).data(Qt.ItemDataRole.UserRole)
        file_name = row_data['name']
        url = row_data['url']
        match row_data['type']:
            case 'video' | 'audio':
                self.status_label.setText("正在播放")
                self.path_label.setText(self.path_util.get_child(file_name))
                self.feature_stack.setCurrentIndex(2)
                self.media_page.player.setSource(QUrl(url))
                self.media_page.player.play()
            case 'image':
                self.status_label.setText("查看图片")
                self.path_label.setText(self.path_util.get_child(file_name))
                self.feature_stack.setCurrentIndex(3)
                self.image_page.set_image(FileSourceUtils.get_image_source(self, url))
            case 'txt':
                self.status_label.setText("正在修改")
                self.path_label.setText(self.path_util.get_child(file_name))
                self.feature_stack.setCurrentIndex(1)
                self.edit_page.editor.setText(FileSourceUtils.get_text_source(self, url))
            case 'dir':
                self.path_label.setText(self.path_util.get_child(file_name))


if __name__ == '__main__':
    logger.debug("Test PySide6 Widget")
    app = QApplication(sys.argv)
    window = MediaManager()
    window.show()
    sys.exit(app.exec())
