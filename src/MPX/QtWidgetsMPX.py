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
        self.__screen = self.screen()
        self.set_window_title('MPX Application Frame')

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        self.set_minimum_width(self.__min_width())
        self.set_minimum_height(500)

        self.__main_layout = QtWidgets.QVBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.__main_layout)

        self.__headerbar = QtWidgetsX.QHeaderBar(self)
        self.__main_layout.add_widget(self.__headerbar)

    def main_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__main_layout

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__headerbar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__headerbar.set_text(text)

    def __min_width(self) -> int:
        # Min window width value
        return 300 if self.__screen.size().width() <= 500 else 500


class WidgetColor(QtWidgets.QWidget):
    """..."""

    def __init__(self, color: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if color:
            self.set_auto_fill_background(True)

            palette = self.palette()
            palette.set_color(QtGui.QPalette.Window, QtGui.QColor(color))

            self.set_palette(palette)

            # layout = QtWidgets.QVBoxLayout()
            # self.set_layout(layout)
            # layout.add_widget(QtWidgets.QLabel(' '))


class SideBarApplicationWindow(QtWidgetsX.QApplicationWindow):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        self.__screen = self.screen()
        self.set_window_title('MPX Application Frame')

        self.set_minimum_width(250)
        self.set_minimum_height(200)
        self.resize(self.__min_width(), 500)

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.__main_layout)

        # Side view
        self.__side_view_layout = QtWidgets.QVBoxLayout()
        self.__side_view_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__side_view_layout)

        self.__side_view_header_bar = QtWidgetsX.QHeaderBar(self)
        self.__side_view_header_bar.set_right_control_buttons_visible(False)
        self.__side_view_layout.add_widget(self.__side_view_header_bar)

        self.__side_view_widget = WidgetColor('grey')
        self.__side_view_widget.set_fixed_width(250)
        self.__side_view_layout.add_widget(self.__side_view_widget, 9)

        self.__side_view_layout_new = QtWidgets.QVBoxLayout()
        self.__side_view_layout_new.set_alignment(QtCore.Qt.AlignTop)
        self.__side_view_widget.set_layout(self.__side_view_layout_new)

        # Page view
        self.__page_view_layout = QtWidgets.QVBoxLayout()
        self.__page_view_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__page_view_layout)

        self.__page_view_header_bar = QtWidgetsX.QHeaderBar(self)
        self.__page_view_header_bar.set_left_control_buttons_visible(False)
        self.__page_view_layout.add_widget(self.__page_view_header_bar)

    def main_layout(self) -> QtWidgets.QHBoxLayout:
        """..."""
        return self.__main_layout

    def page_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__page_view_layout

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__side_view_header_bar.set_window_icon(icon)
        self.__page_view_header_bar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__page_view_header_bar.set_text(text)

    def side_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__side_view_layout_new

    def __min_width(self) -> int:
        # Min window width value
        return 300 if self.__screen.size().width() < 301 < 500 else 600
