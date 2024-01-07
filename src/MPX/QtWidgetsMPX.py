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


class QOverlayWidget(QtWidgets.QWidget):
    """..."""

    def __init__(
            self,
            parent: QtWidgets,
            panel_widget: QtWidgets,
            top_panel_layout: QtWidgets.QLayout,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.__parent = parent
        self.__parent_widget = panel_widget
        self.__parent_top_layout = top_panel_layout

        # Color and border
        bg_color = self.__parent.palette().color(QtGui.QPalette.Window)
        bg_radius = self.__parent.platform_settings().window_border_radius()

        # layout
        self.__main_layout = QtWidgets.QVBoxLayout()
        self.__main_layout.set_contents_margins(6, 6, 6, 6)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__main_frame_widget = QtWidgets.QWidget()
        self.__main_frame_widget.set_contents_margins(0, 0, 0, 0)
        self.__main_frame_widget.set_object_name('mainframewidgetstyle')
        self.__main_frame_widget.set_style_sheet(
            '#mainframewidgetstyle {'
            'background-color: rgba(0, 0, 0, 0.0);'
            f'border-top-left-radius: {bg_radius[0]};'
            f'border-top-right-radius: {bg_radius[1]};'
            f'border-bottom-left-radius: {bg_radius[3]};'
            f'border-bottom-right-radius: {bg_radius[2]};'
            '}')
        self.__main_layout.add_widget(self.__main_frame_widget)

        self.__h_layout = QtWidgets.QHBoxLayout()
        self.__h_layout.set_contents_margins(0, 0, 0, 0)
        self.__h_layout.set_spacing(0)
        self.__h_layout.set_alignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__main_frame_widget.set_layout(self.__h_layout)

        # Panel
        self.__panel_widget = QtWidgets.QWidget()
        self.__panel_widget.set_contents_margins(0, 0, 0, 0)
        self.__panel_widget.set_fixed_width(250)
        self.__panel_widget.set_object_name('panelwidgetstyle')
        self.__panel_widget.set_style_sheet(
            '#panelwidgetstyle {'
            'background-color:'
            f'rgba({bg_color.red()}, {bg_color.red()}, '
            f'{bg_color.red()}, {bg_color.alpha_f()});'
            f'border-top-left-radius: {bg_radius[0]};'
            f'border-top-right-radius: 0;'
            f'border-bottom-left-radius: {bg_radius[3]};'
            'border-bottom-right-radius: 0;}')
        self.__h_layout.add_widget(self.__panel_widget)

        self.__panel_layout = QtWidgets.QVBoxLayout()
        self.__panel_layout.set_contents_margins(0, 0, 0, 0)
        self.__panel_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__panel_widget.set_layout(self.__panel_layout)

        # Panel shadow
        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_effect.set_blur_radius(50)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))
        self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 180))
        self.__panel_widget.set_graphics_effect(self.__shadow_effect)

        class CloseWidget(QtWidgets.QWidget):
            def __init__(self, parent_win):
                super().__init__()
                self.__parent = parent_win

            def mouse_press_event(self, ev: QtGui.QMouseEvent) -> None:
                if ev.button() == QtCore.Qt.LeftButton and self.under_mouse():
                    self.__parent.close_panel()

        self.__close_widget = CloseWidget(self)
        self.__h_layout.add_widget(self.__close_widget)

        self.set_style_sheet(self.__parent.style_sheet())

    def move_event(self, event: QtGui.QMoveEvent) -> None:
        logging.info(event)
        self.__parent.move(self.x(), self.y())
        self.resize(self.__parent.width(), self.__parent.height())

    def close_panel(self) -> None:
        # window resize event display control buttons
        self.__panel_layout.remove_widget(self.__parent_widget)
        self.__parent_top_layout.add_widget(self.__parent_widget)
        self.close()

    def main_layout(self) -> QtWidgets.QLayout:
        return self.__panel_layout


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
        self.__side_panel_widget_for_width = QtWidgets.QWidget()
        self.__side_panel_widget_for_width.set_fixed_width(self.__h_side_width)
        self.__main_layout.add_widget(self.__side_panel_widget_for_width, 9)

        self.__side_panel_main_layout = QtWidgets.QVBoxLayout()
        self.__side_panel_main_layout.set_contents_margins(0, 2, 0, 0)
        self.__side_panel_main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__side_panel_widget_for_width.set_layout(
            self.__side_panel_main_layout)

        self.__side_panel_widget_sender = QtWidgets.QWidget()
        self.__side_panel_main_layout.add_widget(
            self.__side_panel_widget_sender)

        self.__side_panel_control_widget_layout = QtWidgets.QVBoxLayout()
        self.__side_panel_control_widget_layout.set_contents_margins(
            0, 0, 0, 0)
        self.__side_panel_widget_sender.set_layout(
            self.__side_panel_control_widget_layout)

        # Header bar
        self.__header_bar_layout = QtWidgets.QVBoxLayout()
        self.__header_bar_layout.set_contents_margins(0, 0, 0, 0)
        self.__side_panel_control_widget_layout.add_layout(
            self.__header_bar_layout)

        self.__side_panel_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__side_panel_headerbar.set_right_control_buttons_visible(False)
        self.__header_bar_layout.add_widget(self.__side_panel_headerbar)

        # Side panel layou 4 user
        self.__side_panel_layout_for_user = QtWidgets.QVBoxLayout()
        self.__side_panel_layout_for_user.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__side_panel_control_widget_layout.add_layout(
            self.__side_panel_layout_for_user)

        self.__side_panel_overlay_widget = QOverlayWidget(
            self, self.__side_panel_widget_sender,
            self.__side_panel_main_layout)

        self.__darken_side_panel()

        # Frame view
        self.__frame_view_top_layout = QtWidgets.QVBoxLayout()
        self.__frame_view_top_layout.set_alignment(QtCore.Qt.AlignTop)
        self.__main_layout.add_layout(self.__frame_view_top_layout)

        self.__frame_view_headerbar = QtWidgetsX.QHeaderBar(self)
        self.__frame_view_headerbar.set_left_control_buttons_visible(False)
        self.__frame_view_top_layout.add_widget(self.__frame_view_headerbar)

        self.__view_panel_button = QtWidgets.QToolButton()
        self.__view_panel_button.set_icon(
            QtGui.QIcon.from_theme('page-2sides'))  # sidebar-collapse
        self.__view_panel_button.clicked.connect(self.__on_view_panel_button)
        self.__frame_view_headerbar.add_widget_to_left(
            self.__view_panel_button)
        self.__view_panel_button.set_visible(False)

        self.__frame_view_layout = QtWidgets.QVBoxLayout()
        self.__frame_view_layout.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__frame_view_top_layout.add_layout(self.__frame_view_layout, 9)

        # Resize
        self._resize_event_signal.connect(self._resize_event)

    def frame_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__frame_view_layout

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__side_panel_headerbar.set_window_icon(icon)
        self.__frame_view_headerbar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__frame_view_headerbar.set_text(text)

    def side_panel_header_bar(self) -> QtWidgetsX.QHeaderBar:
        """..."""
        return self.__side_panel_headerbar

    def side_panel_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__side_panel_layout_for_user

    def _resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)
        self.__switch_vertical_and_horizontal_window()
        self.__visibility_of_window_control_buttons()
        self.__side_panel_overlay_widget.resize(self.width(), self.height())

    def move_event(self, event: QtGui.QMoveEvent) -> None:
        logging.info(event)
        self.__side_panel_overlay_widget.move(self.x(), self.y())

    def __darken_side_panel(self, color: tuple = (0, 0, 0, 0.1)) -> None:
        """..."""
        radius = self.platform_settings().window_border_radius()

        self.__side_panel_widget_for_width.set_object_name('side_widget_style')
        self.__side_panel_widget_for_width.set_style_sheet(
            '#side_widget_style {'
            'background-color:'
            f'rgba({color[0]}, {color[1]}, {color[2]}, {color[3]});'
            f'border-bottom-left-radius: {radius[3]};'
            'margin: 0px 0px 1px 1px; padding: 0px;}')

    def __initial_width(self) -> int:
        # Vertical
        if self.__screen.size().width() < self.__h_side_width < 500:
            # Sets do view
            return self.__h_side_width + self.__h_side_gap
        # Horizontal
        return self.__h_side_width * 3

    def __on_view_panel_button(self) -> None:
        self.__side_panel_main_layout.remove_widget(
            self.__side_panel_widget_sender)
        self.__side_panel_overlay_widget.main_layout().add_widget(
            self.__side_panel_widget_sender)

        self.__side_panel_headerbar.set_left_control_buttons_visible(False)

        self.__side_panel_widget_sender.set_style_sheet(self.style_sheet())
        self.__side_panel_overlay_widget.show()

    def __switch_vertical_and_horizontal_window(self) -> None:
        # Vertical
        if not self.__is_vertical and self.size().width() < self.__width_flip:
            self.__is_vertical = True
            self.__switch_to_vertical()

        # Horizontal
        elif self.__is_vertical and self.size().width() > self.__width_flip:
            self.__is_vertical = False
            self.__switch_to_horizontal()

    def __switch_to_vertical(self) -> None:
        self.__side_panel_widget_for_width.set_visible(False)
        self.__frame_view_headerbar.set_left_control_buttons_visible(True)
        self.__view_panel_button.set_visible(True)
        self.__side_panel_headerbar.set_move_area_as_enable(False)

    def __switch_to_horizontal(self) -> None:
        self.__side_panel_widget_for_width.set_visible(True)
        self.__frame_view_headerbar.set_left_control_buttons_visible(False)
        self.__view_panel_button.set_visible(False)
        self.__side_panel_headerbar.set_move_area_as_enable(True)

    def __visibility_of_window_control_buttons(self) -> None:
        if self.is_maximized():
            if self.platform_settings().window_use_global_menu():
                self.__side_panel_headerbar.set_left_control_buttons_visible(
                    False)
            self.__side_panel_overlay_widget.close_panel()
        elif self.is_full_screen():
            self.__side_panel_headerbar.set_left_control_buttons_visible(False)
            self.__side_panel_overlay_widget.close_panel()
        else:
            self.__side_panel_headerbar.set_left_control_buttons_visible(True)
