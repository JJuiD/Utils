import sys

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from plugin.csv.base import CsvPlugin

# from qt_material import apply_stylesheet
from easy.user_default import UserDefault
from view.data import initMainWindow
from view.menu import MenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initEvent()
        self.initCentralWidget()
        self.initMenuBar()

        initMainWindow(self)

    def initEvent(self):
        self.restoreGeometry(UserDefault.getForeverLocalKey("window_geometry"))

    def initCentralWidget(self):
        self.centerWidget = QWidget()
        self.setCentralWidget(self.centerWidget)

    def initMenuBar(self):
        menuBar = MenuBar(self)
        self.setMenuBar(menuBar)

    def closeEvent(self, a0: QCloseEvent):
        UserDefault.setForeverLocalKey("window_geometry", self.saveGeometry())


if __name__ == "__main__":
    app = QApplication([])
    # apply_stylesheet(app, theme='dark_teal.xml')
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())