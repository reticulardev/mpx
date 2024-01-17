#!/usr/bin/env python3
import logging
import os
import sys
import time

from PySide6 import QtCore, QtGui, QtWidgets

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'pysidex/src/'))

from PySideX import QtWidgetsX
from __feature__ import snake_case


class _QOverlaySidePanel(QtWidgets.QWidget):
    """..."""
    panel_closed_signal = QtCore.Signal(object)

    def __init__(
            self,
            parent: QtWidgets,
            panel: QtWidgets,
            panel_box: QtWidgets.QLayout,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Param
        self.__parent = parent
        self.__parent_panel = panel
        self.__parent_box = panel_box

        # Settings
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup | QtCore.Qt.Dialog)

        self.set_style_sheet(self.__parent.style_sheet())

        # Main layout
        self.__main_box = QtWidgets.QVBoxLayout()
        self.__main_box.set_contents_margins(6, 6, 6, 6)
        self.__main_box.set_spacing(0)
        self.set_layout(self.__main_box)

        self.__main_frame = QtWidgets.QWidget()
        self.__main_frame.set_contents_margins(0, 0, 0, 0)
        self.__main_frame.set_object_name('__mainframewidgetstyle')
        self.__main_frame.set_style_sheet(
            '#__mainframewidgetstyle {background-color: rgba(0, 0, 0, 0.2);}')
        self.__main_box.add_widget(self.__main_frame)

        self.__horizontal_frame_box = QtWidgets.QHBoxLayout()
        self.__horizontal_frame_box.set_contents_margins(0, 0, 0, 0)
        self.__horizontal_frame_box.set_spacing(0)
        self.__main_frame.set_layout(self.__horizontal_frame_box)

        # Panel background
        self.__panel_background = QtWidgets.QWidget()
        self.__horizontal_frame_box.add_widget(self.__panel_background)

        self.__panel_background_box = QtWidgets.QVBoxLayout()
        self.__panel_background_box.set_contents_margins(0, 0, 0, 0)
        self.__panel_background.set_layout(self.__panel_background_box)

        # Panel
        self.__panel = QtWidgets.QWidget()
        self.__panel.set_contents_margins(0, 0, 0, 0)
        self.__panel_background_box.add_widget(self.__panel)

        self.__panel_box = QtWidgets.QVBoxLayout()
        self.__panel_box.set_contents_margins(0, 0, 0, 0)
        self.__panel_box.set_alignment(QtCore.Qt.AlignTop)
        self.__panel.set_layout(self.__panel_box)

        # Panel shadow
        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_effect.set_blur_radius(50)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))
        self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 100))
        self.__panel_background.set_graphics_effect(self.__shadow_effect)

        class CloseArea(QtWidgets.QWidget):
            def __init__(self, parent_win) -> None:
                super().__init__()
                self.__parent = parent_win

            def mouse_press_event(self, ev: QtGui.QMouseEvent) -> None:
                if ev.button() == QtCore.Qt.LeftButton and self.under_mouse():
                    self.__parent.close_panel()

        self.__close_area = CloseArea(self)
        self.__horizontal_frame_box.add_widget(self.__close_area)
        self.__context_menu = None

    def close_panel(self) -> None:
        self.__panel_box.remove_widget(self.__parent_panel)
        self.__parent_box.add_widget(self.__parent_panel)
        self.panel_closed_signal.emit('panel-closed-signal')
        self.close()

    def context_menu_event(self, event):
        if not self.__context_menu:
            self.__context_menu = self.__parent.quick_context_menu()

        if self.__context_menu:
            self.__context_menu.exec(event.global_pos())

    def main_layout(self) -> QtWidgets.QLayout:
        return self.__panel_box
    
    def move_event(self, event: QtGui.QMoveEvent) -> None:
        logging.info(event)
        self.__parent.move(self.x(), self.y())
        self.resize(self.__parent.width(), self.__parent.height())

    def open_panel(self) -> None:
        self.__parent_box.remove_widget(self.__parent_panel)
        self.__panel_box.add_widget(self.__parent_panel)

        self.__parent.set_left_control_buttons_visible(False)
        self.__parent_panel.set_style_sheet(self.style_sheet())
        self.show()

    def panel(self) -> QtWidgets.QWidget:
        return self.__panel

    def panel_background(self) -> QtWidgets.QWidget:
        return self.__panel_background

    def set_fixed_width(self, width: int) -> None:
        self.__panel.set_fixed_width(width)
        self.__panel_background.set_fixed_width(width)

    def __str__(self) -> str:
        return '_QOverlaySidePanel()'

    def __repr__(self) -> str:
        return '_QOverlaySidePanel(QtWidgets.QWidget)'


class QSidePanelApplicationWindow(QtWidgetsX.QApplicationWindow):
    """Window with side panel"""
    adaptive_mode_signal = QtCore.Signal(object)
    move_event_signal = QtCore.Signal(object)
    panel_opened_signal = QtCore.Signal(object)
    panel_closed_signal = QtCore.Signal(object)
    wide_mode_signal = QtCore.Signal(object)

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        # Flags
        self.__minimum_width = 340
        self.__minimum_height = 200
        self.__border_size = 12
        self.__is_panel_open = False
        self.__panel_width = 250
        self.__panel_color_default = (0, 0, 0, 0.05)
        self.__panel_color = self.__panel_color_default
        self.__horizontal_and_vertical_flip_width = 650
        self.__is_vertical = False
        self.__application_style_sheet = self.__parse_application_style()

        # Settings
        self.set_window_title('MPX Application Window')
        self.set_minimum_width(self.__minimum_width)
        self.set_minimum_height(self.__minimum_height)
        self.resize(self.__initial_width(), 500)

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.central_widget().set_layout(self.__main_box)

        # Side view
        self.__widget_for_panel_width = QtWidgets.QWidget()
        self.__widget_for_panel_width.set_fixed_width(self.__panel_width)
        self.__main_box.add_widget(self.__widget_for_panel_width, 9)

        self.__panel_main_box = QtWidgets.QVBoxLayout()
        self.__panel_main_box.set_contents_margins(0, 0, 0, 0)
        self.__panel_main_box.set_alignment(QtCore.Qt.AlignTop)
        self.__widget_for_panel_width.set_layout(self.__panel_main_box)

        self.__panel_sender = QtWidgets.QWidget()
        self.__panel_main_box.add_widget(self.__panel_sender)

        self.__panel_internal_box = QtWidgets.QVBoxLayout()
        self.__panel_internal_box.set_spacing(0)
        self.__panel_internal_box.set_contents_margins(0, 0, 0, 0)
        self.__panel_sender.set_layout(self.__panel_internal_box)

        # Header bar
        self.__header_bar_box = QtWidgets.QHBoxLayout()
        self.__header_bar_box.set_spacing(0)
        self.__header_bar_box.set_contents_margins(0, 0, 6, 0)
        self.__panel_internal_box.add_layout(self.__header_bar_box)

        self.__panel_header_bar = QtWidgetsX.QHeaderBar(self)
        self.__panel_header_bar.set_right_control_buttons_visible(False)
        self.__header_bar_box.add_widget(self.__panel_header_bar)

        self.__panel_close_button = QtWidgets.QToolButton()
        self.__panel_close_button.set_visible(False)
        self.__panel_close_button.clicked.connect(self.close_panel)
        self.__panel_close_button.set_icon(
            QtGui.QIcon.from_theme('arrow-left'))
        self.__header_bar_box.add_widget(self.__panel_close_button)

        # Side panel layou 4 user
        self.__panel_for_user = QtWidgets.QVBoxLayout()
        self.__panel_for_user.set_spacing(6)
        self.__panel_for_user.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__panel_internal_box.add_layout(self.__panel_for_user)

        self.__panel_overlay = _QOverlaySidePanel(
            self, self.__panel_sender, self.__panel_main_box)
        self.__panel_overlay.panel_closed_signal.connect(
            self.__panel_was_closed_signal)
        self.__panel_overlay.set_fixed_width(self.__panel_width)

        self.__set_panel_background_color()
        self.__set_panel_color()

        # Frame view
        self.__frame_view_top_box = QtWidgets.QVBoxLayout()
        self.__frame_view_top_box.set_alignment(QtCore.Qt.AlignTop)
        self.__main_box.add_layout(self.__frame_view_top_box)

        self.__frame_view_header_bar = QtWidgetsX.QHeaderBar(self)
        self.__frame_view_header_bar.set_left_control_buttons_visible(False)
        self.__frame_view_top_box.add_widget(self.__frame_view_header_bar)

        self.__open_panel_button = QtWidgets.QToolButton()
        self.__open_panel_button.set_icon(
            QtGui.QIcon.from_theme('page-2sides'))  # sidebar-collapse
        self.__open_panel_button.clicked.connect(self.__on_open_panel_button)
        self.__frame_view_header_bar.add_widget_to_left(
            self.__open_panel_button)
        self.__open_panel_button.set_visible(False)

        self.__frame_view_box = QtWidgets.QVBoxLayout()
        self.__frame_view_box.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__frame_view_top_box.add_layout(self.__frame_view_box, 9)

        # Signals
        self.resize_event_signal.connect(self.__resize_event)
        self.set_style_signal.connect(lambda _: self.set_panel_color())
        self.reset_style_signal.connect(self.__reset_style)

    def close_panel(self) -> None:
        """..."""
        self.__panel_overlay.close_panel()

    def frame_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__frame_view_box

    def horizontal_and_vertical_flip_width(self) -> int:
        """..."""
        return self.__horizontal_and_vertical_flip_width

    def move_event(self, event: QtGui.QMoveEvent) -> None:
        """..."""
        self.move_event_signal.emit(event)
        self.__panel_overlay.move(self.x(), self.y())

    def panel_color(self) -> tuple:
        """..."""
        return self.__panel_color

    def panel_header_bar(self) -> QtWidgetsX.QHeaderBar:
        """..."""
        return self.__panel_header_bar

    def panel_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__panel_for_user

    def set_close_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__panel_header_bar.set_close_window_button_visible(visible)
        self.__frame_view_header_bar.set_close_window_button_visible(visible)

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__panel_header_bar.set_window_icon(icon)
        self.__frame_view_header_bar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__frame_view_header_bar.set_text(text)

    def set_horizontal_and_vertical_flip_width(self, width: int) -> None:
        """..."""
        self.__horizontal_and_vertical_flip_width = width

    def set_left_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__panel_header_bar.set_left_control_buttons_visible(visible)

    def set_maximize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__panel_header_bar.set_maximize_window_button_visible(visible)
        self.__frame_view_header_bar.set_maximize_window_button_visible(
            visible)

    def set_minimize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__panel_header_bar.set_minimize_window_button_visible(visible)
        self.__frame_view_header_bar.set_minimize_window_button_visible(
            visible)

    def set_panel_color(self, rgba: tuple = None) -> None:
        """..."""
        self.__application_style_sheet = self.__parse_application_style()
        self.__panel_color = rgba if rgba else self.__panel_color_default
        self.__set_panel_background_color()
        self.__set_panel_color()

    def set_panel_fixed_width(self, width: int) -> None:
        """..."""
        self.__panel_width = width
        self.__widget_for_panel_width.set_fixed_width(self.__panel_width)
        self.__panel_overlay.set_fixed_width(self.__panel_width)

    def set_right_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__panel_header_bar.set_right_control_buttons_visible(visible)

    def __parse_application_style(self) -> str:
        """..."""
        return '; '.join(
            [x.replace('#QApplicationWindow', '').replace('{', '').strip()
             for x in self.style_sheet().split('}')
             if 'QApplicationWindow' in x][-1].split(';'))

    def __set_panel_background_color(self) -> None:
        """..."""
        self.__panel_overlay.panel_background().set_object_name(
            '__overlaypanelbackgroundstyle')
        self.__panel_overlay.panel_background().set_style_sheet(
            '#__overlaypanelbackgroundstyle {'
            f'{self.__application_style_sheet}'
            'border: 0px; '
            'border-top-right-radius: 0;'
            'border-bottom-right-radius: 0}')

    def __set_panel_color(self) -> None:
        """..."""
        panel_style = (
            f'{self.__application_style_sheet}'
            'background-color: rgba('
            f'{self.__panel_color[0]}, {self.__panel_color[1]}, '
            f'{self.__panel_color[2]}, {self.__panel_color[3]});'
            'border: 0px; '
            'border-top-right-radius: 0;'
            'border-bottom-right-radius: 0;'
            'padding: 0px;')

        self.__widget_for_panel_width.set_object_name('__panelwidthstyle')
        self.__widget_for_panel_width.set_style_sheet(
            '#__panelwidthstyle {' + panel_style + 'margin: 1px 0px 1px 1px;}')

        self.__panel_overlay.panel().set_object_name('__paneloverlaystyle')
        self.__panel_overlay.panel().set_style_sheet(
            '#__paneloverlaystyle {' + panel_style + '}')

        self.__panel_sender.set_style_sheet(self.style_sheet())

    def __initial_width(self) -> int:
        if self.screen().size().width() < self.__panel_width < 500:
            return self.__minimum_width
        return 750

    def __on_open_panel_button(self) -> None:
        self.__panel_overlay.open_panel()
        self.panel_opened_signal.emit('panel-opened-signal')
        self.__is_panel_open = True

    def __panel_was_closed_signal(self, event: QtCore.Signal) -> None:
        if self.__is_panel_open:
            self.panel_closed_signal.emit(event)
            self.__is_panel_open = False

    def __switch_vertical_and_horizontal_window(self) -> None:
        # Vertical
        if (not self.__is_vertical and self.size().width() <
                self.__horizontal_and_vertical_flip_width):
            self.__is_vertical = True
            self.__switch_to_vertical()
            self.adaptive_mode_signal.emit('adaptive-mode-signal')

        # Horizontal
        elif (self.__is_vertical and self.size().width() >
              self.__horizontal_and_vertical_flip_width):
            self.__is_vertical = False
            self.__switch_to_horizontal()
            self.wide_mode_signal.emit('wide-mode-signal')

    def __switch_to_vertical(self) -> None:
        self.__widget_for_panel_width.set_visible(False)
        self.__frame_view_header_bar.set_left_control_buttons_visible(True)
        self.__open_panel_button.set_visible(True)
        self.__panel_header_bar.set_move_area_as_enable(False)
        self.__panel_close_button.set_visible(True)

    def __switch_to_horizontal(self) -> None:
        self.__widget_for_panel_width.set_visible(True)
        self.__frame_view_header_bar.set_left_control_buttons_visible(False)
        self.__open_panel_button.set_visible(False)
        self.__panel_header_bar.set_move_area_as_enable(True)
        self.__panel_close_button.set_visible(False)

    def __visibility_of_window_control_buttons(self) -> None:
        if self.is_maximized():
            if self.platform_settings().window_use_global_menu():
                self.__panel_header_bar.set_left_control_buttons_visible(False)
            self.__panel_overlay.close_panel()
        elif self.is_full_screen():
            self.__panel_header_bar.set_left_control_buttons_visible(False)
            self.__panel_overlay.close_panel()
        else:
            self.__panel_header_bar.set_left_control_buttons_visible(True)

    def __resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)
        self.__switch_vertical_and_horizontal_window()
        self.__visibility_of_window_control_buttons()
        self.__panel_overlay.resize(self.width(), self.height())

    def __reset_style(self, event) -> None:
        logging.info(event)
        self.set_panel_color()

    def __str__(self) -> str:
        return 'QSidePanelApplicationWindow()'

    def __repr__(self) -> str:
        return 'QSidePanelApplicationWindow(QtWidgetsX.QApplicationWindow)'


class QQuickContextMenu(QtWidgetsX.QQuickContextMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
