import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *

from easy.log import Log

# from qt_material import apply_stylesheet
from manager.model_manager import ModelManager
from manager.ui_manager import UIManager
from modules.ui_functions import UIFunctions
from modules.ui_main import Ui_MainWindow
from view.common.main import MainWidget
from view.common.menu import MenuBar
# 预加载
from model.csv.base import CsvModel
from model.rss.base import RSS

ModelManager.preload(CsvModel)
ModelManager.preload(RSS)

class MainWindow(Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi()

		UIFunctions.uiDefinitions(self)
		# self.initMenuBar()
		self.initManager()

	def initManager(self):
		UIManager.init(self)
	def initMenuBar(self):
		menuBar = MenuBar(self)
		self.setMenuBar(menuBar)
	def resizeEvent(self, event):
		# Update Size Grips
		UIFunctions.resize_grips(self)
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