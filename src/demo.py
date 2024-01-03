#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)

from MPX import QtWidgetsMPX
from __feature__ import snake_case


class Window(QtWidgetsMPX.ApplicationFrame):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)


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
        """Start the app

        Sets basic window details and starts the application.
        """
        self.window.show()
        sys.exit(self.application.exec())


if __name__ == '__main__':
    app = Application(sys.argv)
    app.main()
