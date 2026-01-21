import sys
import base64
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QFile, QBuffer, Qt
from PySide6.QtGui import QImageReader, QPixmap


class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("No image")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.load_image()

    def load_image(self):
        # 1. 读取本地文件
        file = QFile(r"C:\Users\YI\Downloads\extract.png")
        if not file.open(QFile.OpenModeFlag.ReadOnly):
            self.label.setText("file open failed")
            return

        raw_data = bytes(file.readAll())
        file.close()

        # 2. 转 base64（模拟传输）
        b64_text = base64.b64encode(raw_data)

        # 3. base64 解码回二进制
        decoded_data = base64.b64decode(b64_text)

        # 4. QBuffer
        buffer = QBuffer()
        buffer.setData(decoded_data)
        buffer.open(QBuffer.OpenModeFlag.ReadOnly)

        # 5. 解码图片
        reader = QImageReader(buffer)
        image = reader.read()

        buffer.close()

        if image.isNull():
            self.label.setText(f"decode failed: {reader.errorString()}")
            return

        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageWindow()
    w.show()
    sys.exit(app.exec())
