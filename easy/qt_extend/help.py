from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.singleton import Singleton

ICON_SIZE = QSize(20, 20)

class UIHelp:
	# 隐藏滑动条
	@staticmethod
	def hideAllScrollBar(widget):
		widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

	@staticmethod
	def setBackGroundStyle(widget: QWidget):
		widget.setStyleSheet("""
QWidget {
	background-color: rgb(27, 29, 35);
	border-radius: 5px;
	padding: 10px;
}
QWidget:hover {
	border: 2px solid rgb(64, 71, 88);
}
QWidget:focus {
	border: 2px solid rgb(91, 101, 124);
}
""")

	@staticmethod
	def setListWidgetStyle(widget: QListWidget):
		widget.setStyleSheet("""
QListWidget::item:selected { border: none; }
""")

	@staticmethod
	def setPushButtonStyle(widget: QPushButton, icon):
		widget.setFixedSize(ICON_SIZE)
		widget.setStyleSheet("""
QPushButton {
	background-image: url(%s);
	background-repeat: no-repeat;
	background-position: center;
	border: none;
	background-color: transparent;
}
QPushButton:hover {
	background-color: rgb(40, 44, 52);
}
QPushButton:pressed {
	background-color: rgb(189, 147, 249);
	color: rgb(255, 255, 255);
}
""" % (icon))

