#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)

from MPX import QtWidgetsMPX
from __feature__ import snake_case


class Window(QtWidgetsMPX.QSidePanelApplicationWindow):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)
        self.set_header_bar_icon(self.__app_icon)

        # Title
        self.set_window_title("My custom MPX app")
        # self.set_header_bar_title(self.window_title())

        for i in ['Home', 'Download', 'Image', 'Document', 'Video', 'Music']:
            self.label = QtWidgets.QLabel(str(i))
            self.side_panel_layout().add_widget(self.label)

        self.set_style_sheet('QLabel {font-size: 14px;}')


class Application(object):
    """..."""
    def __init__(self, args: list) -> None:
        """Class constructor

        Initialize class attributes.

        :param args: List of command line arguments
        """
        self.application = QtWidgets.QApplication(args)
        self.window = Window()

    def main(self) -> None:
        """Start the app"""
        self.window.show()
        sys.exit(self.application.exec())


if __name__ == '__main__':
    app = Application(sys.argv)
    app.main()
