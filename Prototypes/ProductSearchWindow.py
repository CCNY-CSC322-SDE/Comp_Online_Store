import sys
import os
import PyQt5
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

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
