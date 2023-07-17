from easy.idler import bindIdlerListWhen, IdlerListEvent
from manager.model_manager import ModelManager
from manager.ui_manager import setBackGroundStyle
from view.base import *

class RSSItem(QWidget):
	def __init__(self, data, item: QListWidgetItem):
		QWidget.__init__(self)

		self.layout = QVBoxLayout()
		self.item = item

		self.title = QLabel(data["title"])
		font = self.title.font()
		font.setBold(True)
		font.setPixelSize(22)
		self.title.setFont(font)
		self.minHeight = 100

		self.browser = QTextBrowser()
		self.browser.setHtml(data["summary"])

		setBackGroundStyle(self)
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.browser)

		self.setLayout(self.layout)
		self.hidewSummary()

	def showSummary(self):
		self.browser.setVisible(True)
		self.item.setSizeHint(QSize(self.item.listWidget().width(), self.item.listWidget().height()-self.minHeight-20))
	def hidewSummary(self):
		self.browser.setVisible(False)
		self.item.setSizeHint(QSize(self.item.listWidget().width(), self.minHeight))

class RSSView(QListWidget, ViewBase):
	EnterType = ViewEnterType.Page
	def init(self):
		# 连接双击事件的处理函数
		self.itemDoubleClicked.connect(self.onItemDoubleClicked)
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
		self.addItem(item)  # 添加item
		widget = RSSItem(data, item)  # 调用上面的函数获取对应
		self.setItemWidget(item, widget)  # 为item设置widget
		# item.setText("11111111111111")
		# w = RSSItem(data, self)
		# print("!!!!!!!!!!!!!!!", w.height())
		# w.setSizeIncrement(item.sizeHint().width(), w.height()+2)
		# self.setItemWidget(item, w)
	def onItemDoubleClicked(self, item):
		widget = self.itemWidget(item)

		for index in range(self.count()):
			currentItem = self.item(index)
			itemWidget = self.itemWidget(currentItem)
			if itemWidget == widget:
				itemWidget.showSummary()
			else:
				itemWidget.hidewSummary()

	def removeItem(self, item):
		# 删除item
		w = self.itemWidget(item)
		self.removeItemWidget(item)
		item = self.takeItem(self.indexFromItem(item).row())
		w.close()
		w.deleteLater()
		del item
