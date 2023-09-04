from enum import Enum

from easy.idler import Idler
from model.base import *
from model.csv.process import LuaProcess, Process
from view.csv import CsvView

class CsvExportType(Enum):
	Lua = 0
	CSharp = 1

ExportProcess = {
	CsvExportType.Lua: LuaProcess
}

class CsvModel_(Model):
	Name = "csv"
	ViewClass = CsvView
	def __init__(self):
		Model.__init__(self)
		self.exportType = Idler()
		self.inputPath = Idler("")
		self.outputPath = Idler("")

		self._process: Process = None
	def getComBoBoxItems(self):
		return [
			"lua",
			"c#"
		]
	def setExportType(self, index):
		global ExportProcess
		self.exportType.value(CsvExportType(index))
		self._process = ExportProcess.get(self.exportType.value())
	def run(self):
		self._process.run(self.inputPath.value(), self.outputPath.value())
	def onClose(self):
		self._view = None



CsvModel = CsvModel_()