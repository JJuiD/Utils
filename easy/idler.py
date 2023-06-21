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


# i = Idler(111)
# i = 2
# print(i)

class IdlerList:
	def __init__(self, value=None):
		self._value = value