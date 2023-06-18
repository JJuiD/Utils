import csv
import sys
from enum import Enum

from easy.file import *
from plugin.base import *
from plugin.csv.view import CsvView
from view.data import MenuBarData


class CsvExportType(Enum):
    Lua = 0
    CSharp = 1

class CsvModelProxy(ModelProxy):
    def getMenuBar(self):
        return MenuBarData("csv", [
            ["窗口", "", self.onCreateCsvView]
        ])
    def onCreateCsvView(self, *args, **kwargs):
        print("onCreateCsvView args", args)
        print("onCreateCsvView kwargs", kwargs)

        if self.isViewCreate():
            return

        self._view = CsvView(self)
        self.setViewCreate(True)

    def getComBoBoxItems(self):
        return [
            "lua",
            "c#"
        ]

    def setExportType(self, index):
        print("setExportType", CsvExportType(index))



class CsvPlugin_(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.exportType = Idler()
        self.inputPath = Idler("")
        self.outputPath = Idler("")

    def getModel(self):
        return CsvModelProxy(self)


CsvPlugin = CsvPlugin_()