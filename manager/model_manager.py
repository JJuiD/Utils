from easy.singleton import Singleton

class ModelManager_(Singleton):
	def __init__(self):
		self._models = []
	def preload(self, model):
		self._models.append(model)
	def models(self):
		return self._models

ModelManager = ModelManager_()

