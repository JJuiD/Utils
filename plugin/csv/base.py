import csv
import sys
from enum import Enum

from easy.file import *
from plugin.base import *
from plugin.csv.view import CsvView
from view.data import MenuBarData


class CsvExportType(Enum):
    Lua = 1

class CsvModelProxy(ModelProxy):
    def showMainView(self, parent):
        return CsvView(parent)

    def getMenuBar(self):
        return MenuBarData("csv", [
            ["导出类型", "", self.onClickExportType]
        ])
    def onClickExportType(self):
        pass
class CsvPlugin_(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.exportType = Idler()
        self.inputPath = Idler("")
        self.outputPath = Idler("")

    def getModel(self):
        return CsvModelProxy(self)

CsvPlugin = CsvPlugin_()