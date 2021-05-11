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

# load registration window ui
registerUI, _ = loadUiType("./ui/register.ui")


# RegistrationWindow class will initialize the register.ui
class RegistrationWindow(QWidget, registerUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
