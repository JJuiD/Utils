from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from plugin.base import ModelProxy
from view.data import gMainWindow


class CsvView(QDockWidget):
    def __init__(self, model: ModelProxy):
        QDockWidget.__init__(self, "csv", gMainWindow())

        gMainWindow().addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self)

        self.model = model
        # self.setFixedWidth(400)
        # self.setFixedHeight(300)

        hBoxWidget1 = QWidget()
        hBoxWidget1.setStyleSheet('''QWidget{background-color:#66CCFF;}''')
        self.inputLineEdit = QLineEdit(hBoxWidget1)
        self.inputLineEdit.setPlaceholderText("csv目录")
        self.inputBtn = QPushButton(hBoxWidget1)
        self.inputBtn.setText("...")
        self.inputBtn.clicked.connect(self.onClickInputBtn)
        hBoxLayOut1 = QHBoxLayout()
        hBoxLayOut1.addWidget(self.inputLineEdit)
        hBoxLayOut1.addWidget(self.inputBtn)
        hBoxWidget1.setLayout(hBoxLayOut1)

        hBoxWidget2 = QWidget()
        hBoxWidget2.setStyleSheet('''QWidget{background-color:#FFCCFF;}''')
        self.exportLineEdit = QLineEdit(hBoxWidget2)
        self.exportLineEdit.setPlaceholderText("导出目录")
        self.exportBtn = QPushButton(hBoxWidget2)
        self.exportBtn.setText("...")
        self.exportBtn.clicked.connect(self.onClickExportBtn)
        hBoxLayOut2 = QHBoxLayout()
        hBoxLayOut2.addWidget(self.exportLineEdit)
        hBoxLayOut2.addWidget(self.exportBtn)
        hBoxWidget2.setLayout(hBoxLayOut2)

        hBoxWidget3 = QWidget()
        hBoxWidget3.setStyleSheet('''QWidget{background-color:#FFCCFF;}''')
        self.exportComboBox = QComboBox(hBoxWidget3)
        self.exportComboBox.addItems(self.model.getComBoBoxItems())
        self.exportComboBox.activated.connect(self.onComboBoxActivated)
        self.sureBtn = QPushButton(hBoxWidget3)
        self.sureBtn.setText("ok")
        self.sureBtn.clicked.connect(self.onClickSureBtn)
        hBoxLayOut3 = QHBoxLayout()
        hBoxLayOut3.addStretch(1)
        hBoxLayOut3.addWidget(self.exportComboBox)
        hBoxLayOut3.addWidget(self.sureBtn)
        hBoxLayOut3.addStretch(1)
        hBoxWidget3.setLayout(hBoxLayOut3)

        vBoxWidget = QWidget()
        vBoxLayOut = QVBoxLayout()
        vBoxLayOut.addWidget(hBoxWidget1)
        vBoxLayOut.addWidget(hBoxWidget2)
        vBoxLayOut.addWidget(hBoxWidget3)
        vBoxWidget.setLayout(vBoxLayOut)

        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addWidget(hBoxWidget1)

        # QFileDialog.getExistingDirectory(self, "csv目录", "./")
        # 最后，把布局放到窗口中里。
        self.setWidget(vBoxWidget)

        # self.setLayout(hBoxLayOut1)
        # self.setWidget(hBoxWidget1)
        # self.setFloating(False)
        # self.setStyleSheet('''QWidget{background-color:#66CCFF;}''')


    def onClickInputBtn(self):
        path = QFileDialog.getExistingDirectory(self, "csv目录", "./")
        self.inputLineEdit.setText(path)

    def onClickExportBtn(self):
        path = QFileDialog.getExistingDirectory(self, "导出目录", "./")
        self.exportLineEdit.setText(path)

    def onComboBoxActivated(self, index):
        self.model.setExportType(self.exportComboBox.currentIndex())

    def onClickSureBtn(self):
        pass

    def closeEvent(self, event: QCloseEvent):
        self.model.setViewCreate(False)

        print("!!!!!!!!!!!!", self.width(), self.height())
