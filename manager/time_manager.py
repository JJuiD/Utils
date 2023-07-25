from easy.singleton import Singleton

from threading import Thread
from time import sleep

TIME_DELTA = 1

def timeThread(self):
	while(self._threadRun):
		self.refresh()
		sleep(TIME_DELTA)

class Timer:
	def __init__(self, call, lerp, count=None):
		self._call = call
		self._lerp = lerp
		self._total = 0
		self._count = count
	def update(self, delta):
		self._total += delta
		while self._total > self._lerp:
			if self._count is None or self._count > 0:
				self._total -= self._lerp
				self._call()
				if self._count is not None:
					self._count -= 1
					if self._count == 0:
						return True
		return False


class TimeManager_(Singleton):
	def __init__(self):
		self._timer = []

		self._threadRun = True
		self._thread = Thread(target=timeThread, args=[self], name="TimeManager_")
		self._thread.start()

	def init(self):
		pass
	def addTimer(self, call, lerp, count=None):
		self._timer.append(Timer(call, lerp, count=count))
	def refresh(self):
		delIndex = []
		for i in range(len(self._timer)):
			timer = self._timer[i]
			isOver = timer.update(TIME_DELTA)
			if isOver:
				delIndex.append(i)

		if len(delIndex) > 0:
			for i in delIndex[::-1]:
				self._timer.pop(i)
	def exit(self):
		self._threadRun = False



TimeManager = TimeManager_()