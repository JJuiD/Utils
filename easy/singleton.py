import time
import threading


class Singleton(object):
	_instance_lock = threading.Lock()

	def __init__(self):
		pass

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, "_instance"):
			with cls._instance_lock:
				if not hasattr(cls, "_instance"):
					cls._instance = object.__new__(cls)
		return cls._instance