from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from easy.log import Log

class LogWidget(QDockWidget):
    def __init__(self, *args, **kwargs):
        QDockWidget.__init__(self, *args)

        self._timer = QTimer(self)
        self._timer.start(300)
        self._timer.timeout.connect(self.onTimeTrigger)

        self.brower = QTextBrowser(self)
        self.brower.setReadOnly(True)
        self.setWidget(self.brower)

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
    def onTimeTrigger(self):
        slist = Log.pop()
        for s in slist:
            self.brower.append(s)