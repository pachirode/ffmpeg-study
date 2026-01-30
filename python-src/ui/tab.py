import sys

from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QApplication


class Tab(QWidget):
    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)

        self.layout = QFormLayout()
        self.setLayout(self.layout)

    def get_info(self):
        raise NotImplemented


class LocalTab(Tab):
    def __init__(self, parent=None):
        super(LocalTab, self).__init__(parent)

        self.root_path = QLineEdit()

        self.setup_ui()

    def setup_ui(self):
        self.layout.addRow("本地根目录", self.root_path)

    def get_info(self):
        return "file", self.root_path.text(), None


class SSHTab(Tab):
    def __init__(self, parent=None):
        super(SSHTab, self).__init__(parent)

        self.root_path = QLineEdit()
        self.port = QLineEdit("22")
        self.host = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()

        self.setup_ui()

    def setup_ui(self):
        self.root_path.setPlaceholderText("默认为该用户的根目录")

        self.layout.addRow("主机:", self.host)
        self.layout.addRow("端口:", self.port)
        self.layout.addRow("用户名:", self.username)
        self.layout.addRow("密码:", self.password)

        ip_mask = "000.000.000.000;_"
        self.host.setInputMask(ip_mask)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def get_info(self):
        return "ssh", self.root_path.text(), {
            "host": self.host.text(),
            "port": self.port.text(),
            "username": self.username.text(),
            "password": self.password.text(),
        }


class GrpcTab(Tab):
    def __init__(self, parent=None):
        super(GrpcTab, self).__init__(parent)

        self.label = QLabel("TODO", self)
        self.setVisible(False)


class HTTPTab(Tab):
    def __init__(self, parent=None):
        super(HTTPTab, self).__init__(parent)

        self.label = QLabel("TODO", self)
        self.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LocalTab()
    window.show()
    sys.exit(app.exec())
