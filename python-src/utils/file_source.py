import os

from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QMessageBox, QWidget

from utils.error import FILE_SOURCE


@dataclass
class Result:
    value: Optional[bytes] = None
    error: Optional[FILE_SOURCE] = None


class FileSourceUtils:
    @staticmethod
    def get_file_source(path, is_local=True) -> Result:
        if is_local:
            if not os.path.exists(path):
                return Result(value=None, error=FILE_SOURCE.NOT_FOUND)
            with open(path, 'rb') as f:
                return Result(value=f.read())

    @staticmethod
    def get_image_source(parent: QWidget, path, is_local=True) -> Optional[QImage]:
        res = FileSourceUtils.get_file_source(path, is_local)
        if res.error is not None:
            QMessageBox.warning(parent, "Get Image Error", res.error.value)
            return None

        image = QImage()
        image.loadFromData(QByteArray(res.value))

        if image.isNull():
            QMessageBox.warning(parent, "Parse Imager Error", "Invalid image data")
            return None

        return image

    @staticmethod
    def get_text_source(parent: QWidget, path, is_local=True) -> Optional[str]:
        res = FileSourceUtils.get_file_source(path, is_local)
        if res.error is not None:
            QMessageBox.warning(parent, "Get Text Error", res.error.value)
            return None

        context = res.value.decode('utf-8')
        return context

