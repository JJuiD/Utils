import sys

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.log import Log

# from qt_material import apply_stylesheet
from manager.model_manager import ModelManager
from manager.ui_manager import UIManager
from modules.ui_functions import UIFunctions

from ui_main import UIMainWindow
from event_main import EventMainWindow

from view.common.menu import MenuBar
# 预加载
from model.csv.base import CsvModel
from model.rss.base import RSS

from widgets import CustomGrip

ModelManager.preload(CsvModel)
ModelManager.preload(RSS)

GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class MainWindow(UIMainWindow, EventMainWindow):
	def __init__(self):
		UIMainWindow.__init__(self)
		EventMainWindow.__init__(self)

		self.initWindowTitle()
		# self.initMenuBar()
		self.initManager()

	def toggleMenu(self, enable):
		if enable:
			# GET WIDTH
			width = self.leftMenuBg.width()
			maxExtend = 240
			standard = 60

			# SET MAX WIDTH
			if width == 60:
				widthExtended = maxExtend
			else:
				widthExtended = standard

			# ANIMATION
			self.animation = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
			self.animation.setDuration(500)
			self.animation.setStartValue(width)
			self.animation.setEndValue(widthExtended)
			self.animation.setEasingCurve(QEasingCurve.InOutQuart)
			self.animation.start()

	def initWindowTitle(self):
		def dobleClickMaximizeRestore(event):
			# IF DOUBLE CLICK CHANGE STATUS
			if event.type() == QEvent.MouseButtonDblClick:
				QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))
		self.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

		# if Settings.ENABLE_CUSTOM_TITLE_BAR:
		#	 #STANDARD TITLE BAR
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		# MOVE WINDOW / MAXIMIZE / RESTORE
		self.dragPos = None
		def moveWindow(event):
			 global GLOBAL_STATE
			 # IF MAXIMIZED CHANGE TO NORMAL
			 if GLOBAL_STATE:
				 self.maximizeRestore()
			 # MOVE WINDOW
			 if event.buttons() == Qt.LeftButton:
				 if self.dragPos:
				 	self.move(self.pos() + event.globalPos() - self.dragPos)
				 self.dragPos = event.globalPos()
				 event.accept()
		self.titleRightInfo.mouseMoveEvent = moveWindow

		# CUSTOM GRIPS
		self.leftGrip = CustomGrip(self, Qt.LeftEdge, True)
		self.rightGrip = CustomGrip(self, Qt.RightEdge, True)
		self.topGrip = CustomGrip(self, Qt.TopEdge, True)
		self.bottomGrip = CustomGrip(self, Qt.BottomEdge, True)

		# DROP SHADOW
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(17)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 150))
		self.bgApp.setGraphicsEffect(self.shadow)

		# RESIZE WINDOW
		self.sizegrip = QSizeGrip(self.frame_size_grip)
		self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

		# MINIMIZE
		self.minimizeAppBtn.clicked.connect(self.showMinimized)

		# MAXIMIZE/RESTORE
		self.maximizeRestoreAppBtn.clicked.connect(lambda: self.maximizeRestore)

		# CLOSE APPLICATION
		self.closeAppBtn.clicked.connect(self.close)

	def initManager(self):
		UIManager.init(self)
	def initMenuBar(self):
		menuBar = MenuBar(self)
		self.setMenuBar(menuBar)
	def resizeEvent(self, event):
		# Update Size Grips
		self.leftGrip.setGeometry(0, 10, 10, self.height())
		self.rightGrip.setGeometry(self.width() - 10, 10, 10, self.height())
		self.topGrip.setGeometry(0, 0, self.width(), 10)
		self.bottomGrip.setGeometry(0, self.height() - 10, self.width(), 10)
	def maximizeRestore(self):
		global GLOBAL_STATE
		status = GLOBAL_STATE
		if status == False:
			self.showMaximized()
			GLOBAL_STATE = True
			self.appMargins.setContentsMargins(0, 0, 0, 0)
			self.maximizeRestoreAppBtn.setToolTip("Restore")
			self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
			self.frame_size_grip.hide()
			self.leftGrip.hide()
			self.rightGrip.hide()
			self.topGrip.hide()
			self.bottomGrip.hide()
		else:
			GLOBAL_STATE = False
			self.showNormal()
			self.resize(self.width()+1, self.height()+1)
			self.appMargins.setContentsMargins(10, 10, 10, 10)
			self.maximizeRestoreAppBtn.setToolTip("Maximize")
			self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
			self.frame_size_grip.show()
			self.leftGrip.show()
			self.rightGrip.show()
			self.topGrip.show()
			self.bottomGrip.show()
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