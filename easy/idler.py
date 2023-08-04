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
	def value(self, value=None):
		if value == None:
			return self._value
		self._value = value


class IdlerListEvent(Enum):
	Add = 1
	Update = 2

# i = Idler(111)
# i = 2
# print(i)

class IdlerEvent:
	def __init__(self, f, autoNotify):
		self._f = f
		self._autoNotify = autoNotify
	def call(self, item=None):
		if item == None:
			return self._f()
		return self._f(item)
	def isAutoNotify(self):
		return self._autoNotify

class IdlerList:
	def __init__(self, value:list=None, sort=None):
		self._value = value
		self._listeners = {}
		self._k = 0
		self._sort = sort
		self._valueChanged = False
		self.sort()
	def __len__(self):
		return len(self._value)
	def __getitem__(self, index):
		return self._value[index]
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
	def _onCheck(self, event):
		if event == IdlerListEvent.Update:
			return self._valueChanged
		return True
	def _on(self, event, item=None, auto=False):
		ev = self._listeners.get(event)
		if ev is not None:
			if self._onCheck(event) and (auto or ev.isAutoNotify()):
				ev.call(item)
				self._onAfter(event)
	def _onAfter(self, event):
		if event == IdlerListEvent.Update:
			self._valueChanged = False
	# 主动推送
	def on(self, event):
		self._on(event, auto=True)
	def remove(self, item):
		self._value.remove(item)
		self._on(IdlerListEvent.Update)
	# def appendFront(self, item):
	# 	self._value.insert(0, item)
	# 	self.sort()
	# 	self._on(IdlerListEvent.Add, item)
	def append(self, item):
		self._value.append(item)
		self.sort()
		self._on(IdlerListEvent.Add, item)
		self._on(IdlerListEvent.Update)
	def sort(self, key=None):
		self._valueChanged = True
		if key == None:
			return self._value.sort(key=self._sort)
		return self._value.sort(key=key)
	def addListeners(self, key, f, autoNotify=True):
		self._listeners[key] = IdlerEvent(f, autoNotify)

def bindIdlerListWhen(list, event, f):
	list.addListeners(event, f)