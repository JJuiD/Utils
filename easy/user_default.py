import io
import os
import collections
import xml.etree.ElementTree as ET

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from easy.singleton import Singleton

def XmlItem(value, isRead=False):
	return value
def ByteArray(value, isRead=False):
	if isRead:
		return QByteArray.fromHex(bytes(value, 'utf-8'))
	return bytes(value.toHex()).decode('utf-8')

InitData = [
	["layout_settings.window_geometry", "01d9d0cb00030000000000ce000000c40000070f0000033b000000cf000000e30000070e0000033a00000000000000000780000000cf000000e30000070e0000033a"]
]
def ParseType(key):
	if key == "layout_settings":
		return ByteArray

PATH = r".\UserDefault.xml"
class UserDefault_(Singleton):
	def getForeverLocalKey(self, key, default=None):
		value = self._cache.get(key)
		if value == None:
			self._setElementText(key, default)
		return value
	def setForeverLocalKey(self, key, value):
		self._setElementText(key, value)
	def __init__(self):
		super().__init__()
		self._tree = None
		self._root = None
		self._cache = {}
		self._keyF = {}

		if os.path.exists(PATH):
			self._tree = ET.parse(PATH)
			self._root = self._tree.getroot()
		else:
			self._root = ET.fromstring('<root></root>')
			self._tree = ET.ElementTree(self._root)

		# 初始化数据
		for item in InitData:
			strArray = item[0].split(".")
			key = strArray[0]
			f = XmlItem
			if len(strArray) == 2:
				key = strArray[1]
				f = ParseType(strArray[0])
			element = self._findOrNew(key)
			if element.text is None:
				element.text = item[1]
			self._keyF[key] = f
			self._cache[key] = self._parseValue(key, element.text, isRead=True)
		self._write()

		# 在集合中获取所有电影
		# movies = collection.getElementsByTagName("movie")
		# # 打印每部电影的详细信息
		# for movie in movies:
		#	 if movie.hasAttribute("title"):
		#		 "Title: %s" % movie.getAttribute("title")
		#
		#	 type = movie.getElementsByTagName('type')[0]
		#	 format = movie.getElementsByTagName('format')[0]
		#	 rating = movie.getElementsByTagName('rating')[0]
		#	 description = movie.getElementsByTagName('description')[0]
	def _write(self):
		def indent(elem, level=0):
			i = "\n" + level * "\t"
			if len(elem):
				if not elem.text or not elem.text.strip():
					elem.text = i + "\t"
				if not elem.tail or not elem.tail.strip():
					elem.tail = i
				for elem in elem:
					indent(elem, level + 1)
				if not elem.tail or not elem.tail.strip():
					elem.tail = i
			else:
				if level and (not elem.tail or not elem.tail.strip()):
					elem.tail = i

		indent(self._root)
		self._tree.write(PATH, encoding="utf-8", xml_declaration=True)

	def _parseValue(self, key, value, isRead=False):
		f = self._keyF.get(key)
		if f is not None:
			value = f(value, isRead=isRead)
		return value

	def _setElementText(self, key, value):
		element = self._findOrNew(key)
		element.text = self._parseValue(key, value)
		self._cache[key] = value
		self._write()

	def _findOrNew(self, key):
		element = self._root.find(key)
		if element == None:
			element = ET.Element(key)
			self._root.append(element)
		return element



UserDefault = UserDefault_()



