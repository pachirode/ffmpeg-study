import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication, QPushButton, QSpacerItem, QSizePolicy, \
    QLabel, QHBoxLayout, QMainWindow, QTabWidget, QDialog, QMessageBox

from ui.edit import EditPage
from ui.image import ImagePage
from ui.list import ListPage
from ui.media import MediaPage
from ui.tab import LocalTab, SSHTab, GrpcTab, HTTPTab
from utils.file_path import FilePathUtils
from utils.file_source import FileSourceUtils
from utils.log import LoggerManager

logger = LoggerManager.get_logger()


class MediaManager(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MediaManager')
        # self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

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



class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建连接")
        self.resize(QGuiApplication.primaryScreen().availableSize() * 2 / 5)

        self.tab_widget = QTabWidget()
        self.ok_btn = QPushButton("确认")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addLayout(h_layout)
        h_layout.addWidget(self.ok_btn)
        h_layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        self.tab_widget.addTab(LocalTab(), "本地连接")
        self.tab_widget.addTab(SSHTab(), "SSH 远程连接")
        self.tab_widget.addTab(GrpcTab(), "Grpc")
        self.tab_widget.addTab(HTTPTab(), "HTTP/HTTPS")

    def get_connection_info(self):
        current_index = self.tab_widget.currentIndex()
        current_widget = self.tab_widget.widget(current_index)
        return current_widget.get_info()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件管理系统")
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

        self.connections = {}

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setObjectName("mainTab")
        self.tab_widget.setTabsClosable(True)
        self.setCentralWidget(self.tab_widget)

        self.setup_menu()

    def setup_menu(self):
        menubar = self.menuBar()
        connection_menu = menubar.addMenu("连接")
        new_conn_action = connection_menu.addAction("新建连接")
        new_conn_action.triggered.connect(self.new_connection)

    def new_connection(self):
        dialog = ConnectionDialog(self)
        if dialog.exec():
            conn_type, root_path, info = dialog.get_connection_info()
            key = self._generate_connection_info(conn_type, info)
            if key is None:
                QMessageBox.warning(self, "提示", "该链接模式暂时不支持")
                return
            if key in self.connections:
                QMessageBox.information(self, "提示", "该链接已经存在，直接切换")
                self.tab_widget.setCurrentIndex(self.connections[key])
                return

            ip = "local"
            if info is not None:
                ip = info.get("host", "unknown")

            tab_page = MediaManager()
            tab_index = self.tab_widget.addTab(tab_page, f"{ip}-{conn_type}")
            self.tab_widget.setCurrentIndex(tab_index)
            self.connections[key] = tab_index

    def _generate_connection_info(self, conn_type, info):
        if conn_type == "file":
            return f"local:{info}"
        elif conn_type == "ssh":
            return f"ssh:{info['host']}:{info['port']}:{info['username']}"
        else:
            return None


if __name__ == '__main__':
    logger.debug("Test PySide6 Widget")
    app = QApplication(sys.argv)
    # window = MediaManager()
    # window.show()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
