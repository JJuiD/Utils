from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from easy.singleton import Singleton

PluginList = []

class ModelProxy:
    def __init__(self, model):
        self._model = model
    def showMainView(self, parent):
        pass
    def getMenuBar(self):
        pass

def getValue(v):
    if type(v) == Idler:
        return v._value
    return v

class Idler:
    def __init__(self, value=None):
        self._value = value
        self._listeners = {}
    def __add__(self, other):
        self._value = self._value + getValue(other)
        return self
    def _notify(self, key):
        pass

class Plugin(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        PluginList.append(self.getModel())
    def getModel(self):
        print("error getModel is None", self)
