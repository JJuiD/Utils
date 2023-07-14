from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.log import Log
from easy.singleton import Singleton

# DockModel
class Model(Singleton):
	Name = ""
	ViewClass = None

	def __init__(self):
		Singleton.__init__(self)
	# def show(self):
	# 	UIManager.createView(Qt.DockWidgetArea.NoDockWidgetArea, self.createView())
	def init(self):
		pass
	def close(self):
		self.onClose()
	def onClose(self):
		pass
	def exit(self):
		pass
