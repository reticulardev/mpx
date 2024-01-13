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
        self.panel_header_bar().add_widget_to_right(self.tbutton)

        for i in ['Download', 'Pictures', 'Documents', 'Videos', 'Music']:
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(self.on_btn)
            self.panel_layout().add_widget(btn)

        # Image
        self.image = QtWidgets.QLabel()
        self.image.set_pixmap(
            QtGui.QIcon.from_theme('folder-download-symbolic').pixmap(96, 96))
        self.frame_view_layout().add_widget(self.image)
        self.frame_view_layout().set_alignment(QtCore.Qt.AlignCenter)

        # Image context menu
        self.image_qcontext = QtWidgetsMPX.QContextMenu(self)
        self.image_qcontext.add_action('Delete', self.on_context_action)
        self.image_qcontext.add_action('Save', self.on_context_action)

        self.image.set_context_menu_policy(QtGui.Qt.CustomContextMenu)
        self.image.customContextMenuRequested.connect(self.image_context_menu)

        # Style button
        self.set_style_button = QtWidgets.QPushButton('Set style')
        self.set_style_button.clicked.connect(self.on_set_style_button)
        self.frame_view_layout().add_widget(self.set_style_button)

        self.panel_opened_signal.connect(lambda event: print(event))
        self.panel_closed_signal.connect(lambda event: print(event))
        self.adaptive_mode_signal.connect(lambda event: print(event))
        self.wide_mode_signal.connect(lambda event: print(event))

        # Text  and their context menu (Global: use context_menu_event)
        self.context_menu_label = QtWidgets.QLabel('Menu text here')
        self.frame_view_layout().add_widget(self.context_menu_label)

        self.qcontext_menu = QtWidgetsMPX.QContextMenu(self)
        self.set_global_context_menu(self.qcontext_menu)
        self.qcontext_menu.add_action('You', self.on_context_action)
        self.qcontext_menu.add_action('Have', self.on_context_action)
        self.qcontext_menu.add_action('No', self.on_context_action)
        self.qcontext_menu.add_action('Power', self.on_context_action)

    def context_menu_event(self, event):
        print(event)
        self.qcontext_menu.exec(event.global_pos())

    def on_context_action(self):
        self.context_menu_label.set_text(self.sender().text())

    def image_context_menu(self):
        self.image_qcontext.exec(QtGui.QCursor.pos())

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
