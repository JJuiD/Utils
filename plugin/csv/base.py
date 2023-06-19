import csv
import sys
from enum import Enum

from easy.file import *
from easy.idler import Idler
from plugin.base import *
from plugin.csv.process import LuaProcess, Process
from plugin.csv.view import CsvView
from view.data import MenuBarData

class CsvExportType(Enum):
    Lua = 0
    CSharp = 1

ExportProcess = {
    CsvExportType.Lua: LuaProcess
}

class CsvPlugin_(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.exportType = Idler()
        self.inputPath = Idler("")
        self.outputPath = Idler("")

        self._process : Process = None
        self._view = None
    def getMenuBar(self):
        return MenuBarData("csv", [
            ["窗口", "", self.onCreateCsvView]
        ])
    def onCreateCsvView(self, *args, **kwargs):
        if self._view is not None:
            return

        self._view = CsvView(self)
        # 数据绑定
        self._view.inputLineEdit.bindIdler(self.inputPath)
        self._view.exportLineEdit.bindIdler(self.outputPath)

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
    def closeEvent(self):
        self._view = None



CsvPlugin = CsvPlugin_()