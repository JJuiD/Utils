import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from easy.log import Log

# from qt_material import apply_stylesheet
from manager.model_manager import ModelManager
from manager.ui_manager import UIManager
from style import MainWindowStyle
from view.common.main import MainWidget
from view.common.menu import MenuBar
# 预加载
from model.csv.base import CsvModel
from model.rss.base import RSS

ModelManager.preload(CsvModel)
ModelManager.preload(RSS)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.initCentralWidget()
		self.initMenuBar()
		self.initManager()

		MainWindowStyle(self)
	def initManager(self):
		UIManager.init(self)
	def initCentralWidget(self):
		self.centerWidget = MainWidget(self)
		self.setCentralWidget(self.centerWidget)
	def initMenuBar(self):
		menuBar = MenuBar(self)
		self.setMenuBar(menuBar)
	def closeEvent(self, a0: QCloseEvent):
		Log.close()
		UIManager.close()
		a0.accept()


if __name__ == "__main__":
	app = QApplication([])
	# apply_stylesheet(app, theme='light_teal.xml')
	gui = MainWindow()
	gui.show()
	sys.exit(app.exec())