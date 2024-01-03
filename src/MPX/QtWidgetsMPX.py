#!/usr/bin/env python3
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'pysidex/src/'))

from MPX.pysidex.src.PySideX import QtWidgetsX
from __feature__ import snake_case


class ApplicationWindow(QtWidgetsX.QApplicationWindow):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        self.set_window_title('MPX Application Frame')

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        self.set_minimum_height(500)
        self.set_minimum_width(500)

        self.__main_layout = QtWidgets.QVBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.__main_layout)

        self.__headerbar = QtWidgetsX.QHeaderBar(self)
        self.__main_layout.add_widget(self.__headerbar)

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__headerbar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__headerbar.set_text(text)
