from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from easy.singleton import Singleton

PluginList = []

class Plugin(Singleton):
	def __init__(self):
		Singleton.__init__(self)
		PluginList.append(self)

	def getModel(self):
		print("error getModel is None", self)
