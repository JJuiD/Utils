

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from easy.singleton import Singleton
from manager.model_manager import ModelManager


class DockWidget(QDockWidget):
	def __init__(self, parent):
		QDockWidget.__init__(self, parent)
		self._view = None
		self._model = None
		self._area = Qt.DockWidgetArea.LeftDockWidgetArea
		self.dockLocationChanged.connect(self.onDockLocationChanged)
	def init(self, model):
		self._model = model
		viewClass = model.ViewClass
		self._view = viewClass(self)
		self._view.init(model)
		self._view.bindIdler()

		self.setWidget(self._view)
		self.setObjectName(model.Name)
		# 预加载
		if self.settingValue("state"):
			self._area = self.settingValue("area")
		self.parent().addDockWidget(self._area, self)
	def onDockLocationChanged(self, area):
		self._area = area
	def settingValue(self, key):
		return UIManager.setting().value(self.name() + "/" + key)
	def closeEvent(self, event):
		self._model.onClose()
		# 删除缓存
		UIManager.setting().remove(self.name())
		UIManager.destoryView(self)
		event.accept()
	def name(self):
		return self._model.Name
	def setting(self):
		self._model.setting()
		UIManager.setting().beginGroup(self.name())
		UIManager.setting().setValue("area", self._area)
		UIManager.setting().setValue("state", True)
		self._view.setting()
		UIManager.setting().endGroup()

class UIManager_(Singleton):
	def __init__(self):
		self._root = None
		self._childs = {}
		self._setting = QSettings('ui.ini', QSettings.Format.IniFormat)

		# print("!!!!!!!!!!!!!!!")
		# self._setting.beginGroup("test")
		# self._setting.setValue("key", 111)
		# self._setting.endGroup()
		# print(self._setting.value("test"))
		# print(self._setting.value("test/key"))
		# self._setting.remove("test")
		# print(self._setting.value("test/key"))
		# print("-----------------end")

	def init(self, mainWindow):
		self._root = mainWindow
		for model in ModelManager.models():
			stateKey = model.Name + "/state"
			if self._setting.value(stateKey):
				self.createView(model)
		self._root.restoreGeometry(self._setting.value("window_geometry"))
		self._root.restoreState(self._setting.value("window_state"))

	def createView(self, model):
		if self._childs.get(model.Name) is not None:
			widget = self._childs.get(model.Name)
		else:
			widget = DockWidget(self._root)
			widget.init(model)
			# self._root.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, widget)
			self._childs[model.Name] = widget
		return widget
	def destoryView(self, widget):
		del self._childs[widget.name()]
	def setting(self):
		return self._setting
	def close(self):
		self._setting.setValue("window_geometry", self._root.saveGeometry())
		self._setting.setValue("window_state", self._root.saveState())
		for name, child in self._childs.items():
			child.setting()

UIManager = UIManager_()
