from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class ViewBase:
	def __init__(self, *args, **kwargs):
		self._model = None
	def init(self, model):
		self._model = model
	def model(self):
		return self._model
	def setting(self):
		pass
	def bindIdler(self):
		pass