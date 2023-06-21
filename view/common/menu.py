import functools

from PySide6.QtGui import *
from PySide6.QtWidgets import *

from manager.model_manager import ModelManager
from manager.ui_manager import UIManager

class MenuBar(QMenuBar):
	def __init__(self, parent):
		QMenuBar.__init__(self, parent)

		group = self.addMenu("窗口")
		for model in ModelManager.models():
			self._addMenu(group, [model.Name, None, functools.partial(self.onWindowCreate, model)])
	def onWindowCreate(self, model):
		UIManager.createView(model)
	def _addMenu(self, group, item):
		action = QAction(item[0], self.parent())
		if item[1] is not None:
			action.setShortcut(item[1])
		action.triggered.connect(item[2])
		group.addAction(action)