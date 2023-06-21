from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.log import Log

class MainWidget(QWidget):
	def __init__(self, *args, **kwargs):
		QWidget.__init__(self, *args)

		# self._timer = QTimer(self)
		# self._timer.start(300)
		# self._timer.timeout.connect(self.onTimeTrigger)

		self.setWindowTitle("111111111111111")
		# self.setReadOnly(True)

		self.leftMenuFrame = QFrame(self.leftMenuBg)
		self.leftMenuFrame.setObjectName(u"leftMenuFrame")
		self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
		self.leftMenuFrame.setFrameShadow(QFrame.Raised)
		self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
		self.verticalMenuLayout.setSpacing(0)
		self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
		self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)

		# self.isVisible()

		# self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
		# self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
	def onTimeTrigger(self):
		slist = Log.pop()
		for s in slist:
			self.append(s)