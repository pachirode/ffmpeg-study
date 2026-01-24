import sys

from PySide6.QtGui import QGuiApplication, QImage, QPalette, QImageReader, QColorSpace, QPixmap, QImageWriter
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QLabel, QApplication, QSizePolicy, QScrollArea, QScrollBar, QMessageBox, QHBoxLayout, QPushButton

from ui.page import Page


class ImagePage(Page):
    def __init__(self, parent=None):
        super(ImagePage, self).__init__(parent)
        self.resize(400, 600)

        self.image = QImage()
        self.scale_factor = 1.0
        self.image_label = QLabel(self)
        self.scroll_area = QScrollArea(self)

        self.save_btn = None
        self.copy_btn = None
        self.paste_btn = None
        self.zoom_in_btn = None
        self.zoom_out_btn = None
        self.fit_btn = None

        self.setup_ui()

    def setup_ui(self):
        self.setup_image()
        self.setup_buttons()

    def setup_image(self):
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setVisible(False)

        self.layout.addWidget(self.scroll_area)

    def setup_buttons(self):
        h_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save", self)
        self.copy_btn = QPushButton("Copy", self)
        self.paste_btn = QPushButton("Paste", self)
        self.zoom_in_btn = QPushButton("Zoom in", self)
        self.zoom_out_btn = QPushButton("Zoom out", self)
        self.fit_btn = QPushButton("Fit", self)

        h_layout.addWidget(self.save_btn)
        h_layout.addWidget(self.copy_btn)
        h_layout.addWidget(self.paste_btn)
        h_layout.addWidget(self.zoom_in_btn)
        h_layout.addWidget(self.zoom_out_btn)
        h_layout.addWidget(self.fit_btn)

        self.layout.addLayout(h_layout)

        self.copy_btn.clicked.connect(lambda: QGuiApplication.clipboard().setImage(self.image))
        self.paste_btn.clicked.connect(self.paste)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.fit_btn.clicked.connect(self.fit_to_window)
        self.save_btn.clicked.connect(self.save_file)

    def scale_image(self, factor):
        self.scroll_area.setWidgetResizable(False)
        self.scale_factor *= factor
        self.image_label.setPixmap(QPixmap.fromImage(self.image))
        self.image_label.resize(self.scale_factor * self.image_label.pixmap().size())
        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), factor)

    def adjust_scroll_bar(self, scroll_bar: QScrollBar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2)))

    def load_file(self, file_name):
        reader = QImageReader(file_name)
        reader.setAutoTransform(True)
        new_image = reader.read()
        if new_image.isNull():
            QMessageBox.information(
                self,
                QGuiApplication.applicationDisplayName(),
                f"Cannot load {QDir.toNativeSeparators(file_name)}: {reader.errorString()}",
            )
            return False

        self.set_image(new_image)
        self.setWindowFilePath(file_name)

        return True

    def set_image(self, new_image):
        if new_image is None:
            return
        self.image = new_image
        if self.image.colorSpace().isValid():
            self.image.convertedToColorSpace(QColorSpace.ColorModel.Rgb)
        self.image_label.setPixmap(QPixmap.fromImage(self.image))
        self.scroll_area.setVisible(True)
        self.image_label.adjustSize()

    def save_file(self, file_name):
        pass

    def close(self):
        self.image = QImage()
        self.image_label.clear()
        self.scale_factor = 1.0
        self.scroll_area.close()

    def paste(self):
        self.scale_factor = 1.0
        mime_data = QGuiApplication.clipboard().mimeData()
        if mime_data and mime_data.hasImage():
            image = QGuiApplication.clipboard().image()
            self.set_image(image)

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def normal(self):
        self.scale_factor = 1.0
        self.scale_image(1.0)

    def fit_to_window(self):
        self.scroll_area.setWidgetResizable(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImagePage()
    window.show()
    sys.exit(app.exec())
