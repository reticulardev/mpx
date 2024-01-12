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

    def __init__(self, *args, **kwargs) -> None:
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

        # Search
        self.tbutton = QtWidgets.QToolButton()
        self.tbutton.set_icon(QtGui.QIcon.from_theme('search'))
        self.side_panel_header_bar().add_widget_to_right(self.tbutton)

        for i in ['Download', 'Pictures', 'Documents', 'Videos', 'Music']:
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(self.on_btn)
            self.side_panel_layout().add_widget(btn)

        self.image = QtWidgets.QLabel()
        self.image.set_pixmap(
            QtGui.QIcon.from_theme('folder-download-symbolic').pixmap(96, 96))
        self.frame_view_layout().add_widget(self.image)
        self.frame_view_layout().set_alignment(QtCore.Qt.AlignCenter)

        self.set_style_button = QtWidgets.QPushButton('Set style')
        self.set_style_button.clicked.connect(self.on_set_style_button)
        self.frame_view_layout().add_widget(self.set_style_button)

        self.panel_opened_signal.connect(lambda event: print(event))
        self.panel_closed_signal.connect(lambda event: print(event))
        self.adaptive_mode_signal.connect(lambda event: print(event))
        self.wide_mode_signal.connect(lambda event: print(event))

        # menu
        self.context_menux = QtWidgets.QMenu()
        menu_action = self.context_menux.add_action('Hello')
        menu_action.triggered.connect(self.on_context_menu)

        menu_action = self.context_menux.add_action('World')
        menu_action.triggered.connect(self.on_context_menu)

        self.file_menu = QtWidgets.QMenu('File')
        self.context_menux.add_menu(self.file_menu)

        menu_action = self.file_menu.add_action('Open')
        menu_action.triggered.connect(self.on_context_menu)

        menu_action = self.file_menu.add_action('Save')
        menu_action.triggered.connect(self.on_context_menu)

        # new
        self.ctx_menu = QtWidgetsMPX.QContextMenu(self)
        self.set_context_menu(self.ctx_menu)

    def context_menu_event(self, event):
        self.ctx_menu.exec(event.global_pos())

    def on_context_menu(self):
        print(self.sender().text())

    def on_set_style_button(self) -> None:
        if self.set_style_button.text() == 'Set style':
            self.set_style_sheet(
                'QApplicationWindow {'
                '  background-color: rgba(44, 44, 50, 0.9);'
                '  border: 1px solid #283690;'
                '  border-radius: 10px;}'
                'QToolButton {'
                '  background: transparent;'
                '  padding: 2px;'
                '  border: 0px;'
                '  border-radius: 3px;'
                '  background-color: rgba(100, 100, 100, 0.2);}'
                'QToolButton:hover {'
                '  background: transparent;'
                '  background-color: rgba(100, 100, 100, 0.3);}'
                'QPushButton {'
                '  border: 1px solid rgba(100, 100, 100, 0.3);}'
                'QContextMenu {'
                '  background-color: rgba(44, 44, 50, 0.9);'
                '  border: 1px solid #283690;}')
            self.set_panel_color((79, 54, 95, 0.5))
            self.set_style_button.set_text('Reset style')
        else:
            self.reset_style()
            self.set_style_button.set_text('Set style')

    def on_btn(self) -> None:
        self.image.set_pixmap(QtGui.QIcon.from_theme(
            f'folder-{self.sender().text().lower()}-symbolic').pixmap(96, 96))
        self.close_panel()


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
