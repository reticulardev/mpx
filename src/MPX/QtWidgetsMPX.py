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


class QColorWidget(QtWidgets.QWidget):
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


class QSidePanelApplicationWindow(QtWidgetsX.QApplicationWindow):
    """Window with side panel"""
    resize_event_signal = QtCore.Signal(object)

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        # Flags
        self.__border_size = 12

        self.__h_side_width = 250
        self.__h_side_gap = 50

        self.__v_side_width = 300
        self.__v_side_gap = 0

        self.__width_flip = (self.__h_side_width + self.__h_side_gap) * 2 + 1
        self.__is_vertical = False

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

        # Main layout
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.central_widget().set_layout(self.__main_layout)

        # Side view
        self.__sideview_widget = QtWidgets.QWidget()
        self.__sideview_widget.set_fixed_width(self.__h_side_width)
        self.__main_layout.add_widget(self.__sideview_widget, 9)

        self.__sideview_top_layout = QtWidgets.QVBoxLayout()
        self.__sideview_top_layout.set_contents_margins(0, 0, 0, 0)
        self.__sideview_top_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__sideview_widget.set_layout(self.__sideview_top_layout)

        self.__sideview_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__sideview_headerbar.set_contents_margins(0, 0, 0, 0)
        self.__sideview_headerbar.set_right_control_buttons_visible(False)
        self.__sideview_top_layout.add_widget(self.__sideview_headerbar)

        self.set_side_view_color()

        self.__sideview_layout = QtWidgets.QVBoxLayout()
        self.__sideview_layout.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__sideview_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__sideview_top_layout.add_layout(self.__sideview_layout)

        # Page view
        self.__pageview_layout = QtWidgets.QVBoxLayout()
        self.__pageview_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__pageview_layout)

        self.__pageview_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__pageview_headerbar.set_left_control_buttons_visible(False)
        self.__pageview_layout.add_widget(self.__pageview_headerbar)

        self._resize_event_signal.connect(self._resize_event)

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

    def set_side_view_color(self, color: tuple = (0, 0, 0, 0.1)) -> None:
        """..."""
        self.set_style_sheet(self.__side_view_color(color))

    def side_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__sideview_layout

    def __side_view_color(self, color: tuple = (0, 0, 0, 0.1)) -> str:
        self.__sideview_widget.set_object_name('side_widget_style')
        radius = self.platform_settings().window_border_radius()
        return (
            '#side_widget_style {'
            'background-color:'
            f'rgba({color[0]}, {color[1]}, {color[2]}, {color[3]});'
            f'border-bottom-left-radius: {radius[3]};'
            'margin: 0px 0px 1px 1px; padding: 0px;}')

    def _resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)
        self.__switch_vertical_and_horizontal_window()
        self.__visibility_of_window_control_buttons()

    def __initial_width(self) -> int:
        # Vertical
        if self.__screen.size().width() < self.__h_side_width < 500:
            # Sets do view
            return self.__h_side_width + self.__h_side_gap
        # Horizontal
        return self.__h_side_width * 3

    def __switch_vertical_and_horizontal_window(self) -> None:
        if not self.__is_vertical and self.size().width() < self.__width_flip:
            self.__is_vertical = True
            self.__switch_to_vertical()
            print('Flip - vertical...')
        elif self.__is_vertical and self.size().width() > self.__width_flip:
            self.__is_vertical = False
            self.__switch_to_horizontal()
            print('Flip - horizontal...')

    def __switch_to_vertical(self) -> None:
        self.__sideview_widget.set_visible(False)
        self.__pageview_headerbar.set_left_control_buttons_visible(True)

    def __switch_to_horizontal(self) -> None:
        self.__sideview_widget.set_visible(True)
        self.__pageview_headerbar.set_left_control_buttons_visible(False)

    def __visibility_of_window_control_buttons(self) -> None:
        if self.is_maximized():
            if self.platform_settings().window_use_global_menu():
                self.__sideview_headerbar.set_left_control_buttons_visible(
                    False)
        elif self.is_full_screen():
            self.__sideview_headerbar.set_left_control_buttons_visible(False)
        else:
            self.__sideview_headerbar.set_left_control_buttons_visible(True)
