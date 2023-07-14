from easy.singleton import Singleton

class ModelManager_(Singleton):
	def __init__(self):
		self._models = {}
	def init(self):
		pass
	def preload(self, model):
		self._models[model.Name] = model
		model.init()
	def models(self):
		return self._models
	def at(self, name):
		return self._models[name]
	def exit(self):
		for model in self._models.values():
			model.exit()

ModelManager = ModelManager_()

