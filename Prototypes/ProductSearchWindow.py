import sys
import os
import PyQt5
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Api import product as productApi

# database connection
con = sqlite3.connect("./Database/store_system.db")
cur = con.cursor()

# load the ui for product search window
searchUI, _ = loadUiType("./ui/product-search.ui")


# SearchWindow class will initialize the register.ui
class ProductSearchWindow(QWidget, searchUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        # set position
        self.setGeometry(150, 0, 1200, 750)
        self.setFixedSize(self.size())
        self.systems = []
        self.checkBoxIntel.stateChanged.connect(lambda: self.updateProcessor(self.checkBoxIntel))
        self.checkBoxAmd.stateChanged.connect(lambda: self.updateProcessor(self.checkBoxAmd))
        self.checkBoxArm.stateChanged.connect(lambda: self.updateProcessor(self.checkBoxArm))
        self.checkBoxMac.stateChanged.connect(lambda: self.updateOS(self.checkBoxMac))
        self.checkBoxWindows.stateChanged.connect(lambda: self.updateOS(self.checkBoxWindows))
        self.checkBoxLinux.stateChanged.connect(lambda: self.updateOS(self.checkBoxLinux))
        self.checkBox_RAM_8GB.stateChanged.connect(lambda: self.updateRam(self.checkBox_RAM_8GB))
        self.checkBox_RAM_12GB.stateChanged.connect(lambda: self.updateRam(self.checkBox_RAM_12GB))
        self.checkBox_RAM_16GB.stateChanged.connect(lambda: self.updateRam(self.checkBoxRAM_16GB))
        self.checkBox_Hard_Disk_256GB.stateChanged.connect(lambda: self.updateHDD(self.checkBox_Hard_Disk_256GB))
        self.checkBox_Hard_Disk_512GB.stateChanged.connect(lambda: self.updateHDD(self.checkBox_Hard_Disk_512GB))
        self.checkBox_Hard_Disk_1TB.stateChanged.connect(lambda: self.updateHDD(self.checkBox_Hard_disk_1TB))
        self.getSystems()

    def updateSystemsList(self):
        self.searchListWidget.clear()
        for system in self.systems:
            listItem = ProductListItem(parent=None, system=system)
            qListWidgetItem = QListWidgetItem(self.searchListWidget)
            qListWidgetItem.setSizeHint(listItem.sizeHint())
            self.searchListWidget.addItem(qListWidgetItem)
            self.searchListWidget.setItemWidget(qListWidgetItem, listItem)

    def getSystems(self):
        results = productApi.getAllSystems()
        self.allSystems = results
        self.systems = results
        self.updateSystemsList()

    def updateProcessor(self, b):
        processor = b.text().strip().lower()
        newSystems = []
        for system in self.systems:
            if processor in system.cpu.lower() or system.cpu.lower() in processor:
                newSystems.append(system)
        self.systems = newSystems
        self.updateSystemsList()

    def updateHDD(self, b):
        hdd = b.text().strip().lower()
        newSystems = []
        for system in self.systems:
            if hdd in system.hdd_size.lower() or system.hdd_size.lower() in hdd:
                newSystems.append(system)
        self.systems = newSystems
        self.updateSystemsList()

    def updateRAM(self, b):
        ram = b.text().strip().lower()
        newSystems = []
        for system in self.systems:
            if ram in system.ram_size.lower() or system.ram_size.lower() in ram:
                newSystems.append(system)
        self.systems = newSystems
        self.updateSystemsList()

    def updateOS(self, b):
        newSystems = []
        os = b.text().strip().lower()
        if b.isChecked() == True:
            for system in self.systems:
                if os in system.operating_system.lower() or system.operating_system.lower() in os:
                    newSystems.append(system)
            self.systems = newSystems
        self.updateSystemsList()


class ProductListItem(QWidget):
    def __init__(self, parent=None, system=None):
        super(ProductListItem, self).__init__(parent)
        self.system = system
        layout = QVBoxLayout()
        self.productItemBoxLayout = QHBoxLayout()
        self.cpuLabel = QLabel(system.cpu)
        self.ramSizeLabel = QLabel(system.ram_size)
        self.gpuLabel = QLabel(system.gpu)
        self.hddLabel = QLabel(system.hdd_size)
        self.osLabel = QLabel(system.operating_system)

        self.productItemBoxLayout.addWidget(self.cpuLabel)
        self.productItemBoxLayout.addWidget(self.ramSizeLabel)
        self.productItemBoxLayout.addWidget(self.gpuLabel)
        self.productItemBoxLayout.addWidget(self.hddLabel)
        self.productItemBoxLayout.addWidget(self.osLabel)

        layout.addLayout(self.productItemBoxLayout)
        self.setLayout(layout)
