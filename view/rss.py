from easy.idler import bindIdlerListWhen, IdlerListEvent
from manager.model_manager import ModelManager
from manager.ui_manager import setBackGroundStyle
from view.base import *

class RSSItem(QWidget):
	def __init__(self, data):
		QWidget.__init__(self)

		self.layout = QHBoxLayout()

		self.title = QLabel(data["title"])
		font = self.title.font()
		font.setBold(True)
		font.setPixelSize(22)
		self.title.setFont(font)

		setBackGroundStyle(self)

		self.layout.addWidget(self.title)
		self.setLayout(self.layout)

class RSSView(QListWidget, ViewBase):
	EnterType = ViewEnterType.Page
	def init(self):
		pass
		# self.setSpacing(20)
		# QApplication.instance().setQuitOnLastWindowClosed(True)
		# 隐藏任务栏,无边框,置顶等
		# self.setWindowFlags(self.windowFlags() | Qt.Tool |
		# 					Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		# 去掉窗口边框
		# self.setFrameShape(self.NoFrame)
		# 背景透明
		# self.viewport().setAutoFillBackground(False)
		# self.setAttribute(Qt.WA_TranslucentBackground, True)
		# 不显示滚动条
		# self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# 获取屏幕高宽
		# rect = QApplication.instance().desktop().availableGeometry(self)
		# self.setMinimumHeight(rect.height())
		# self.setMaximumHeight(rect.height())
		# self.move(rect.width() - self.minimumWidth() - 18, 0)
		# self._timer = QTimer(self, timeout=self.onMessageCreate)

	def bindIdler(self):
		for item in self.dataModel().urlArticles:
			self.info(item)
		bindIdlerListWhen(self.dataModel().urlArticles, IdlerListEvent.Add, self.info)

	def info(self, data):
		item = QListWidgetItem()  # 创建QListWidgetItem对象
		item.setSizeHint(QSize(self.width(), 100))  # 设置QListWidgetItem大小
		widget = RSSItem(data)  # 调用上面的函数获取对应
		self.addItem(item)  # 添加item
		self.setItemWidget(item, widget)  # 为item设置widget
		# item.setText("11111111111111")
		# w = RSSItem(data, self)
		# print("!!!!!!!!!!!!!!!", w.height())
		# w.setSizeIncrement(item.sizeHint().width(), w.height()+2)
		# self.setItemWidget(item, w)
	def removeItem(self, item):
		# 删除item
		w = self.itemWidget(item)
		self.removeItemWidget(item)
		item = self.takeItem(self.indexFromItem(item).row())
		w.close()
		w.deleteLater()
		del item
