#!/usr/bin/env python3
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'pysidex/src/'))

from MPX.pysidex.src.PySideX import QtWidgetsX
from __feature__ import snake_case


class ApplicationFrame(QtWidgetsX.QApplicationWindow):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
