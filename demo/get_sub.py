from PySide6 import QtWidgets
# Python 不会提前加载所有类，需要加载才能看到
from PySide6.QtWidgets import (
    QPushButton,
    QToolButton,
    QCheckBox,
    QRadioButton,
)


def get_sub_classes(cls):
    for sub in cls.__subclasses__():
        print(sub)
        get_sub_classes(sub)


get_sub_classes(QtWidgets.QAbstractButton)
