import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

from ui.page import Page


class ListPage(Page):
    def __init__(self, parent=None):
        super(ListPage, self).__init__(parent)

        self.table = None

        self.setup_ui()

    def setup_ui(self):
        self.list_table()

        self.init_table()

    def list_table(self):
        self.table = QTableWidget(self)
        self.table.setObjectName("listPageTable")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if self.table.columnCount() < 3:
            self.table.setColumnCount(3)

        self.layout.addWidget(self.table)

    def init_table(self):
        self.table.setRowCount(0)
        mock_data = [
            {"name": "演示视频.mp4", "type": "video", "url": "http://vjs.zencdn.net/v/oceans.mp4", "detail": "1080P", "remote": ""},
            {"name": "测试音频.mp3", "type": "audio", "url": "", "detail": "320kbps"},
            {"name": "测试文档.txt", "type": "txt", "url": r"C:\Users\YI\Desktop\edi_server_20260113.log", "detail": ""},
            {"name": "测试图片.png", "type": "image", "url": r"C:\Users\YI\Downloads\extract.png", "detail": ""}
        ]
        for i, info in enumerate(mock_data):
            self.table.insertRow(i)
            name_item = QTableWidgetItem(info['name'])
            name_item.setData(Qt.ItemDataRole.UserRole, info)
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, QTableWidgetItem(info['type']))
            self.table.setItem(i, 2, QTableWidgetItem(info['detail']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ListPage()
    window.show()
    sys.exit(app.exec())
