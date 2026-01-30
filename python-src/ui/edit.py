import sys

from PySide6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QTextEdit

from ui.page import Page


class EditPage(Page):
    def __init__(self, parent=None):
        super(EditPage, self).__init__(parent)

        self.editor = None
        self.cancel_btn = None
        self.save_btn = None

        self.setup_ui()

    def setup_ui(self):
        self.setup_editor()
        self.setup_buttons()

    def setup_editor(self):
        self.editor = QTextEdit(self)
        self.editor.setObjectName("editPageEditor")

        self.layout.addWidget(self.editor)

    def setup_buttons(self):
        h_layout = QHBoxLayout()

        self.cancel_btn = QPushButton("取消", self)
        self.cancel_btn.setObjectName("editPageCancelBtn")
        self.save_btn = QPushButton("保存修改", self)
        self.save_btn.setObjectName("editPageSaveBtn")

        h_layout.addWidget(self.cancel_btn)
        h_layout.addWidget(self.save_btn)

        self.layout.addLayout(h_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EditPage()
    window.show()
    sys.exit(app.exec())
