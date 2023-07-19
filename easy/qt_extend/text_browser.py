from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QTextBrowser
import re

class TextBrowser(QTextBrowser):
	def __init__(self, parent=None):
		QTextBrowser.__init__(self, parent)
		self._network = QNetworkAccessManager(self)
		self._network.finished.connect(self.onHandleNetworkReply)
		self._text = None
		self._count = 0

		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	def initSummary(self, text):
		# QTextBrowser.setHtml(self, text)
		self._text = text
		self.document().clear()

		pattern = r'<img.*?src="(.*?)".*?>'
		matches = re.findall(pattern, text)
		if matches:
			for url in matches:
				request = QNetworkRequest(url)
				self._network.get(request)
				self._count = self._count + 1
	def onHandleNetworkReply(self, reply):
		self._count = self._count - 1
		if reply.error() == QNetworkReply.NoError:
			self.document().addResource(QTextDocument.ImageResource, reply.url(), reply.readAll())

		if self._count == 0:
			self.setHtml(self._text)