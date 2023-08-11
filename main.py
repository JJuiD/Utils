import functools
import sys

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.log import Log

# from qt_material import apply_stylesheet
from manager.model_manager import ModelManager
from manager.time_manager import TimeManager
from manager.ui_manager import UIManager
from modules.ui_functions import UIFunctions

from ui_main import UIMainWindow

from view.common.menu import MenuBar
# 预加载
from model.csv.base import CsvModel
from model.rss.base import RSS

from widgets import CustomGrip

# ModelManager.preload(CsvModel)
ModelManager.preload(RSS)

GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

MENU_SELECTED_STYLESHEET = """
	border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
	background-color: rgb(40, 44, 52);
	"""

def selectMenu(getStyle):
	global MENU_SELECTED_STYLESHEET
	select = getStyle + MENU_SELECTED_STYLESHEET
	return select

def deselectMenu(getStyle):
	global MENU_SELECTED_STYLESHEET
	deselect = getStyle.replace(MENU_SELECTED_STYLESHEET, "")
	return deselect

class MainWindow(UIMainWindow):
	def __init__(self):
		super().__init__()
		# EventMainWindow.__init__(self)
		self.initLeftMenu()
		self.initEvent()
		self.initWindowTitle()
		# self.initMenuBar()
		self.initManager()

		self.installEventFilter(self)

		tray_icon = QSystemTrayIcon(self)
		tray_icon.setIcon(QIcon("images/icons/cil-cloudy.png"))
		tray_icon.show()

		tray_icon.activated.connect(self.on_tray_activated)

	def on_tray_activated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			# 显示主窗口
			self.showNormal()

	def onSetCurrentWidget(self, sender):
		name = sender.objectName()
		self.resetStyle(name)
		sender.setStyleSheet(selectMenu(sender.styleSheet()))
		UIManager.open(name)
	def initLeftMenu(self):
		self.leftMenuClickCall = {}
		def addLeftMenu(name, iconPath):
			btn = QPushButton(self.topMenu)
			btn.setObjectName(name)
			self.toggleButton.sizePolicy().setHeightForWidth(btn.sizePolicy().hasHeightForWidth())
			btn.setSizePolicy(self.toggleButton.sizePolicy())
			btn.setMinimumSize(QSize(0, 45))
			btn.setFont(self.topMenuFont)
			btn.setCursor(QCursor(Qt.PointingHandCursor))
			btn.setLayoutDirection(Qt.LeftToRight)
			btn.setStyleSheet(iconPath)
			btn.clicked.connect(functools.partial(self.onSetCurrentWidget, btn))
			self.topMenuVLayout.addWidget(btn)
			return btn
		self.btnRss = addLeftMenu(u"rss", u"background-image: url(:/icons/images/icons/cil-rss.png);")

	def initEvent(self):
		self.toggleButton.clicked.connect(self.onClickToggleMenu)
		# MINIMIZE
		self.minimizeAppBtn.clicked.connect(self.showMinimized)
		# MAXIMIZE/RESTORE
		self.maximizeRestoreAppBtn.clicked.connect(self.maximizeRestore)
		# CLOSE APPLICATION
		self.closeAppBtn.clicked.connect(self.close)
		# 左下角设置按钮
		self.toggleLeftBox.clicked.connect(self.openCloseLeftBox)
		self.extraCloseColumnBtn.clicked.connect(self.openCloseLeftBox)
		# 右上角设置按钮
		self.settingsTopBtn.clicked.connect(self.toggleRightBox)
		# 侧边按钮动画表现
		self.stackedWidget.setCurrentWidget(self.home)
		self.btn_home.setStyleSheet(selectMenu(self.btn_home.styleSheet()))
		# 侧边按钮
		self.btn_home.clicked.connect(self.onLeftMenuButtonClick)
		self.btn_widgets.clicked.connect(self.onLeftMenuButtonClick)
		self.btn_new.clicked.connect(self.onLeftMenuButtonClick)
		self.btn_save.clicked.connect(self.onLeftMenuButtonClick)

	def onLeftMenuButtonClick(self):
		# GET BUTTON CLICKED
		btn = self.sender()
		btnName = btn.objectName()

		# SHOW HOME PAGE
		if btnName == "btn_home":
			self.stackedWidget.setCurrentWidget(self.home)
		# SHOW WIDGETS PAGE
		elif btnName == "btn_widgets":
			self.stackedWidget.setCurrentWidget(self.widgets)
		# SHOW NEW PAGE
		elif btnName == "btn_new":
			self.stackedWidget.setCurrentWidget(self.new_page)  # SET PAGE
		elif btnName == "btn_save":
			print("Save BTN clicked!")

		# PRINT BTN NAME
		print(f'Button "{btnName}" pressed!')
		self.resetStyle(btnName)  # RESET ANOTHERS BUTTONS SELECTED
		btn.setStyleSheet(selectMenu(btn.styleSheet()))  # SELECT MENU

	def openCloseLeftBox(self, enable):
		# GET WIDTH
		width = self.extraLeftBox.width()
		widthRightBox = self.extraRightBox.width()
		color = "background-color: rgb(44, 49, 58);"

		# GET BTN STYLE
		style = self.toggleLeftBox.styleSheet()

		# SET MAX WIDTH
		if width == 0:
			# SELECT BTN
			self.toggleLeftBox.setStyleSheet(style + color)
			if widthRightBox != 0:
				style = self.settingsTopBtn.styleSheet()
				self.settingsTopBtn.setStyleSheet(style.replace("background-color: #ff79c6;", ''))
		else:
			# RESET BTN
			self.toggleLeftBox.setStyleSheet(style.replace(color, ''))

		self.startBoxAnimation(width, widthRightBox, "left")

	def toggleRightBox(self, enable):
		# GET WIDTH
		width = self.extraRightBox.width()
		widthLeftBox = self.extraLeftBox.width()
		color = "background-color: #ff79c6;"

		# GET BTN STYLE
		style = self.settingsTopBtn.styleSheet()

		# SET MAX WIDTH
		if width == 0:
			# SELECT BTN
			self.settingsTopBtn.setStyleSheet(style + color)
			if widthLeftBox != 0:
				style = self.toggleLeftBox.styleSheet()
				self.toggleLeftBox.setStyleSheet(style.replace("background-color: rgb(44, 49, 58);", ''))
		else:
			# RESET BTN
			self.settingsTopBtn.setStyleSheet(style.replace(color, ''))

		self.startBoxAnimation(widthLeftBox, width, "right")

	def resetStyle(self, widget):
		for w in self.topMenu.findChildren(QPushButton):
			if w.objectName() != widget:
				w.setStyleSheet(deselectMenu(w.styleSheet()))

	def startBoxAnimation(self, left_box_width, right_box_width, direction):
		right_width = 0
		left_width = 0

		# Check values
		if left_box_width == 0 and direction == "left":
			left_width = 240
		else:
			left_width = 0
		# Check values
		if right_box_width == 0 and direction == "right":
			right_width = 240
		else:
			right_width = 0

		# ANIMATION LEFT BOX
		self.left_box = QPropertyAnimation(self.extraLeftBox, b"minimumWidth")
		self.left_box.setDuration(500)
		self.left_box.setStartValue(left_box_width)
		self.left_box.setEndValue(left_width)
		self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

		# ANIMATION RIGHT BOX
		self.right_box = QPropertyAnimation(self.extraRightBox, b"minimumWidth")
		self.right_box.setDuration(500)
		self.right_box.setStartValue(right_box_width)
		self.right_box.setEndValue(right_width)
		self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

		# GROUP ANIMATION
		self.group = QParallelAnimationGroup()
		self.group.addAnimation(self.left_box)
		self.group.addAnimation(self.right_box)
		self.group.start()

	def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标
		if event.button() == Qt.LeftButton:
			self._moveDrag = True
			self._mpos = event.globalPosition().toPoint() - self.pos()
			event.accept()
	def mouseMoveEvent(self, event):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
		if Qt.LeftButton and self._moveDrag:
			self.move(event.globalPosition().toPoint() - self._mpos)
			event.accept()
	def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
		self._moveDrag = False

	def onClickToggleMenu(self, enable):
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

	def maximizeRestore(self):
		if self.maxSizeState == False:
			self.showMaximized()
			self.appMargins.setContentsMargins(0, 0, 0, 0)
			self.maximizeRestoreAppBtn.setToolTip("Restore")
			self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
			self.frame_size_grip.hide()
			self.leftGrip.hide()
			self.rightGrip.hide()
			self.topGrip.hide()
			self.bottomGrip.hide()
		else:
			self.showNormal()
			self.resize(self.width() + 1, self.height() + 1)
			self.appMargins.setContentsMargins(10, 10, 10, 10)
			self.maximizeRestoreAppBtn.setToolTip("Maximize")
			self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
			self.frame_size_grip.show()
			self.leftGrip.show()
			self.rightGrip.show()
			self.topGrip.show()
			self.bottomGrip.show()
		self.maxSizeState = not self.maxSizeState

	def initWindowTitle(self):
		# if Settings.ENABLE_CUSTOM_TITLE_BAR:
		#	 #STANDARD TITLE BAR
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		# MOVE WINDOW / MAXIMIZE / RESTORE
		self.dragPos = None
		self.maxSizeState = False

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

		self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

	def initMenuBar(self):
		menuBar = MenuBar(self)
		self.setMenuBar(menuBar)
	def resizeEvent(self, event):
		# Update Size Grips
		self.leftGrip.setGeometry(0, 10, 10, self.height())
		self.rightGrip.setGeometry(self.width() - 10, 10, 10, self.height())
		self.topGrip.setGeometry(0, 0, self.width(), 10)
		self.bottomGrip.setGeometry(0, self.height() - 10, self.width(), 10)
	def initManager(self):
		UIManager.init(self)

		TimeManager.init()
		self._thread = QTimer()
		self._thread.timeout.connect(TimeManager.update)
		self._thread.setInterval(1000)
		self._thread.start()

		ModelManager.init()

	def eventFilter(self, watched: QObject, event: QEvent):
		if event.type() == QEvent.ApplicationStateChange:
			print("ApplicationStateChange")
		return super().eventFilter(watched, event)
	def closeEvent(self, event: QCloseEvent):
		# 创建消息框
		message_box = QMessageBox(self)
		message_box.setIcon(QMessageBox.Question)
		message_box.setWindowTitle("保存到后台")
		message_box.setText("是否将应用程序保存到后台？")
		message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		# 如果用户选择“是”，将应用程序保存到后台
		if message_box.exec() == QMessageBox.Yes:
			QCoreApplication.instance().setQuitLockEnabled(True)
			TimeManager.sleep()
			event.ignore()
			self.hide()
		else:
			# 如果用户选择“否”，执行默认的关闭操作
			Log.exit()
			UIManager.exit()
			# TimeManager.exit()
			ModelManager.exit()
			self._thread.stop()
			super().closeEvent(event)

if __name__ == "__main__":
	app = QApplication([])
	# apply_stylesheet(app, theme='light_teal.xml')

	# 使得程序能在后台运行，关闭最后一个窗口不退出程序
	QApplication.setQuitOnLastWindowClosed(False)

	gui = MainWindow()
	gui.show()
	sys.exit(app.exec())