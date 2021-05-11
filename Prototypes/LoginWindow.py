import sys
import os
import PyQt5
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# database connection
con = sqlite3.connect("./store_system.db")
cur = con.cursor()

# load login window ui
loginUI, _ = loadUiType("./ui/login.ui")


# LoginWindow class will initialize the login.ui
class LoginWindow(QWidget, loginUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
