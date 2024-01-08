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
        self.set_header_bar_title(self.window_title())

        # Search
        self.tbutton = QtWidgets.QToolButton()
        self.tbutton.set_icon(QtGui.QIcon.from_theme('search'))
        self.side_panel_header_bar().add_widget_to_right(self.tbutton)

        for i in ['Home', 'Download', 'Image', 'Document', 'Video', 'Music']:
            btn = QtWidgets.QPushButton(str(i))
            btn.clicked.connect(self.on_btn)
            self.side_panel_layout().add_widget(btn)

        self.lbl = QtWidgets.QPushButton('...')
        self.frame_view_layout().add_widget(self.lbl)
        self.frame_view_layout().set_alignment(QtCore.Qt.AlignCenter)

        self.set_style_sheet(
            'QToolButton {'
            '   background: transparent;'
            '   padding: 2px;'
            '   border: 0px;'
            '   border-radius: 3px;}'
            'QToolButton:hover {'
            '   background: transparent;'
            '   padding: 2px;'
            '   border: 0px;'
            '   border-radius: 3px;'
            '   background-color: rgba(127, 127, 127, 0.2);}'
        )

        self.side_panel_has_opened_signal.connect(self.panel_has_opened)
        self.side_panel_was_closed_signal.connect(self.panel_closed)
        self.switched_to_vertical_signal.connect(self.switched_to_vertical)
        self.switched_to_horizontal_signal.connect(self.switched_to_horizontal)
        self.set_panel_fixed_width(200)

    def on_btn(self) -> None:
        self.lbl.set_text(self.sender().text())
        self.close_side_panel()

    @staticmethod
    def panel_has_opened(event: QtCore.Signal) -> None:
        print(event)

    @staticmethod
    def panel_closed(event: QtCore.Signal) -> None:
        print(event)

    @staticmethod
    def switched_to_vertical(event: QtCore.Signal) -> None:
        print(event)

    @staticmethod
    def switched_to_horizontal(event: QtCore.Signal):
        print(event)


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
