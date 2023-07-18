

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.singleton import Singleton
from easy.user_default import UserDefault
from manager.model_manager import ModelManager
from view.base import ViewEnterType


class DockWidget(QDockWidget):
	def __init__(self, parent):
		QDockWidget.__init__(self, parent)
		self._view = None
		self._model = None
		self._area = Qt.DockWidgetArea.LeftDockWidgetArea
		self.dockLocationChanged.connect(self.onDockLocationChanged)
	def init(self, model):
		self._model = model
		ViewClass = model.ViewClass
		self._view = ViewClass(self)
		self._view.dataModel(model)
		self._view.init()
		self._view.bindIdler()

		self.setWidget(self._view)
		self.setObjectName(model.Name)
		if self.settingValue("state"):
			self._area = self.settingValue("area")
	def open(self):
		self.parent().addDockWidget(self._area, self)
	def onDockLocationChanged(self, area):
		self._area = area
	def settingValue(self, key, value=None):
		if value == None:
			return UserDefault.value(self.name() + "/" + key)
		UserDefault.setValue(self.name() + "/" + key, value)
	def closeEvent(self, event):
		self._model.exit()
		# 删除缓存
		UserDefault.remove(self.name())
		UIManager.close(self)
		event.accept()
	def name(self):
		return self._model.Name
	def exit(self):
		self._model.exit()
		self.settingValue("area", self._area)
		self.settingValue("state", True)

class PageWidget():
	def __init__(self, parent):
		self._view = None
		self._model = None
		self._parent = parent
	def init(self, model):
		self._model = model
		ViewClass = model.ViewClass
		self._view = ViewClass(self._parent)
		self._view.dataModel(model)
		self._view.init()
		self._view.bindIdler()

		self._view.setObjectName(model.Name)
		# 预加载
		if self.settingValue("state"):
			pass
		self._parent.stackedWidget.addWidget(self._view)
	# self._area = self.settingValue("area")
	def open(self):
		self._parent.stackedWidget.setCurrentWidget(self._view)
	def settingValue(self, key, value=None):
		if value == None:
			return UserDefault.value(self.name() + "/" + key)
		UserDefault.setValue(self.name() + "/" + key, value)
	def closeEvent(self, event):
		self._model.onClose()
		# 删除缓存
		UserDefault.remove(self.name())
		UIManager.close(self)
		event.accept()
	def name(self):
		return self._model.Name
	def exit(self):
		self._model.exit()
		self.settingValue("state", True)


def setBackGroundStyle(widget):
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

def setPushButtonStyle(widget: QPushButton, icon):
	widget.setStyleSheet("""
QPushButton {
	background-image: url();
	background-position: left center;
	background-repeat: no-repeat;
	border: none;
	border-left: 22px solid transparent;
	background-color: transparent;
	text-align: left;
	padding-left: 44px;
}
QPushButton:hover {
	background-color: rgb(40, 44, 52);
}
QPushButton:pressed {
	background-color: rgb(189, 147, 249);
	color: rgb(255, 255, 255);
}
""")

class UIManager_(Singleton):
	def __init__(self):
		self._root = None
		self._childs = {}
	def root(self):
		return self._root
	def init(self, mainWindow):
		self._root = mainWindow
		# for model in ModelManager.models():
		# 	stateKey = model.Name + "/state"
		# 	if UserDefault.value(stateKey):
		# 		self.openView(model)
		self._root.restoreGeometry(UserDefault.value("window_geometry"))
		self._root.restoreState(UserDefault.value("window_state"))
	def open(self, name):
		model = ModelManager.at(name)
		if self._childs.get(name) is None:
			widget = None
			if model.ViewClass.EnterType == ViewEnterType.Dock:
				widget = DockWidget(self._root)
			elif model.ViewClass.EnterType == ViewEnterType.Page:
				widget = PageWidget(self._root)
			widget.init(model)
			self._childs[model.Name] = widget
		widget = self._childs.get(model.Name)
		widget.open()
		return widget
	def close(self, widget):
		del self._childs[widget.name()]
	def exit(self):
		UserDefault.setValue("window_geometry", self._root.saveGeometry())
		UserDefault.setValue("window_state", self._root.saveState())
		for name, child in self._childs.items():
			child.exit()

UIManager = UIManager_()
