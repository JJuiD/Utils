import json
from enum import Enum

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
	def value(self, value=None):
		if value == None:
			return self._value
		self._value = value


class IdlerListEvent(Enum):
	Add = 1

# i = Idler(111)
# i = 2
# print(i)

class IdlerList:
	def __init__(self, value:list=None, sort=None):
		self._value = value
		self._listeners = {}
		self._k = 0
		self._sort = sort
		self.sort()
	def __iter__(self):
		self._k = 0
		return self
	def __next__(self):
		if self._k < len(self._value):
			v = self._value[self._k]
			self._k += 1
			return v
		else:
			raise StopIteration
	def json(self):
		return self._value
	def extend(self, l):
		for item in l:
			self.append(item)
	def extendFront(self, l: list):
		for item in l[::-1]:
			self.appendFront(item)
	def appendFront(self, item):
		self._value.insert(0, item)
		if self._listeners.get(IdlerListEvent.Add):
			for f in self._listeners.get(IdlerListEvent.Add):
				f(item)
	def append(self, item):
		self._value.append(item)
		if self._listeners.get(IdlerListEvent.Add):
			for f in self._listeners.get(IdlerListEvent.Add):
				f(item)

	def sort(self, key=None):
		if key == None:
			return self._value.sort(key=self._sort)
		return self._value.sort(key=key)
	def addListeners(self, key, f):
		if self._listeners.get(key) is None:
			self._listeners[key] = []
		self._listeners[key].append(f)

def bindIdlerListWhen(list, event, f):
	list.addListeners(event, f)