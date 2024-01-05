#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'pysidex/src/'))

from MPX.pysidex.src.PySideX import QtWidgetsX
from __feature__ import snake_case


class QApplicationWindow(QtWidgetsX.QApplicationWindow):
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


class QWidgetColor(QtWidgets.QWidget):
    """..."""

    def __init__(self, color: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if color:
            self.set_auto_fill_background(True)

            palette = self.palette()
            palette.set_color(QtGui.QPalette.Window, QtGui.QColor(color))

            self.set_palette(palette)

        layout = QtWidgets.QVBoxLayout()
        self.set_layout(layout)
        layout.add_widget(QtWidgets.QLabel(' '))


class QSideBarApplicationWindow(QtWidgetsX.QApplicationWindow):
    """..."""
    resize_event_signal = QtCore.Signal(object)

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        # Flags
        self.__h_side_width = 250
        self.__h_side_gap = 80

        self.__v_side_width = 300
        self.__v_side_gap = 0

        self.__width_flip = self.__h_side_width + self.__h_side_gap + 1

        # Settings
        self.__screen = self.screen()
        self.set_window_title('MPX Application Window')

        self.set_minimum_width(self.__h_side_width + self.__h_side_gap)
        self.set_minimum_height(200)
        self.resize(self.__initial_width(), 500)

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.__main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.__main_layout)

        # Side view
        self.__sideview_layout = QtWidgets.QVBoxLayout()
        self.__sideview_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__sideview_layout)

        self.__sideview_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__sideview_headerbar.set_maximum_width(self.__h_side_width)
        self.__sideview_headerbar.set_right_control_buttons_visible(False)
        self.__sideview_layout.add_widget(self.__sideview_headerbar)

        self.__sideview_widget = QtWidgets.QWidget()
        self.__sideview_widget.set_fixed_width(self.__h_side_width)
        self.__sideview_layout.add_widget(self.__sideview_widget, 9)

        self.__sideview_layout_new = QtWidgets.QVBoxLayout()
        self.__sideview_layout_new.set_alignment(QtCore.Qt.AlignTop)
        self.__sideview_widget.set_layout(self.__sideview_layout_new)

        self.set_side_view_color()

        # Page view
        self.__pageview_layout = QtWidgets.QVBoxLayout()
        self.__pageview_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__pageview_layout)

        self.__pageview_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__pageview_headerbar.set_left_control_buttons_visible(False)
        self.__pageview_layout.add_widget(self.__pageview_headerbar)

        self._resize_event_signal.connect(self._resize_event)

    def _resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)

        if self.size().width() < self.__width_flip:
            print('Flip...')

        # Control buttons visibility
        if self.is_maximized():
            if self.platform_settings().window_use_global_menu():
                self.__sideview_headerbar.set_left_control_buttons_visible(
                    False)
        elif self.is_full_screen():
            self.__sideview_headerbar.set_left_control_buttons_visible(False)
        else:
            self.__sideview_headerbar.set_left_control_buttons_visible(True)

    def main_layout(self) -> QtWidgets.QHBoxLayout:
        """..."""
        return self.__main_layout

    def page_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__pageview_layout

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__sideview_headerbar.set_window_icon(icon)
        self.__pageview_headerbar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__pageview_headerbar.set_text(text)

    def set_side_view_color(self, color: tuple = (0, 0, 0, 0.1)):
        self.__sideview_widget.set_object_name('side_widget_style')
        self.__sideview_headerbar.set_object_name('side_headerbar_style')
        self.__sideview_layout.set_object_name('sideview_layout_style')

        radius = self.platform_settings().window_border_radius()
        self.set_style_sheet(
            '#sideview_layout_style {width: 300px;}'
            '#side_headerbar_style {'
            '   background-color: '
            f'    rgba({color[0]}, {color[1]}, {color[2]}, {color[3]});'
            f'   border-top-left-radius: {radius[0]};'
            '   margin: 1px 0px 0px 1px;}'
            '#side_widget_style {'
            '   background-color: '
            f'    rgba({color[0]}, {color[1]}, {color[2]}, {color[3]});'
            f'   border-bottom-left-radius: {radius[3]};'
            '   margin: 0px 0px 1px 1px;}')

    def side_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__sideview_layout_new

    def __initial_width(self) -> int:
        # Vertical
        if (self.__screen.size().width() <
                (self.__h_side_width + self.__h_side_gap) < 500):
            return self.__h_side_width
        # Horizontal
        return self.__h_side_width * 3
