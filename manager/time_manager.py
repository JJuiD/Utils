from collections import OrderedDict

from easy.singleton import Singleton

from PySide6.QtCore import QTimer

IDCounter = 1
class Timer:
	def __init__(self, call, lerp, count=None):
		global IDCounter
		self.id = IDCounter
		IDCounter = IDCounter + 1

		self._call = call
		self._lerp = lerp
		self._total = 0
		self._count = count
		self._lock = False
	def update(self, delta):
		if self._lock == True:
			return False
		self._lock = True
		self._call()
		self._lock = False
		# self._total += delta
		# while self._total > self._lerp:
		# 	if self._count is None or self._count > 0:
		# 		self._total -= self._lerp
		# 		self._call()
		# 		if self._count is not None:
		# 			self._count -= 1
		# 			if self._count == 0:
		# 				return True
		return False

TIME_DELTA = 1000

class TimeManager_(Singleton):
	def __init__(self):
		self._timer = OrderedDict()
		self._sleep = {}
		self._isSleep = False
	def init(self):
		pass
	def addTimer(self, call, lerp, count=None, inSleep=False):
		timer = Timer(call, lerp, count=count)
		self._timer[timer.id] = timer
		self._sleep[timer.id] = inSleep
	def update(self):
		delIndex = []
		for id, timer in self._timer.items():
			if self._sleep[id] and self._isSleep is False:
				return

			isOver = timer.update(TIME_DELTA)
			if isOver:
				delIndex.append(id)

		if len(delIndex) > 0:
			for id in delIndex:
				del self._timer[id]

	def sleep(self):
		self._isSleep = True
	def wake(self):
		self._isSleep = False
	# def exit(self):
	# 	self._thread.stop()



TimeManager = TimeManager_()