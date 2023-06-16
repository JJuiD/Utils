from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class CsvView(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.setParent(parent)

        self.inputLineEdit = QLineEdit()

        QFileDialog.getExistingDirectory(self, "csv目录", "./")

