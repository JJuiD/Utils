from enum import Enum

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class ViewEnterType(Enum):
	Page = 1
	Dock = 2


class ViewBase:
	EnterType = None
	def __init__(self, *args):
		self._model = None
	def dataModel(self, model=None):
		if model is not None:
			self._model = model
		return self._model
	def init(self):
		pass
	def bindIdler(self):
		pass
