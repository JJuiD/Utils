from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from easy.idler import Idler
class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)
        self._idler = None
    def bindIdler(self, idler:Idler):
        self._idler = idler
    def setText(self, a0: str):
        QLineEdit.setText(self, a0)
        if self._idler is not None:
            self._idler.value(a0)

