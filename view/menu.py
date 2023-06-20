from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from plugin.base import PluginList
from view.data import MenuBarData


class MenuBar(QMenuBar):
	def __init__(self, parent):
		QMenuBar.__init__(self, parent)

		group = self.addMenu("plugin")
		for model in PluginList:
			menuBarData = model.getMenuBar()
			self._addMenu(group, menuBarData)
	def _addMenu(self, group, menuBarData: MenuBarData):
		group = group.addMenu(menuBarData.name)
		for item in menuBarData.actions:
			# if type(action[1]) == list:
			#	 self._addMenu(group, action[0], action[1])
			# else:
			action = QAction(item[0], self.parent())
			if item[1] != "":
				action.setShortcut(item[1])
			action.triggered.connect(item[2])
			group.addAction(action)