import sqlite3
import re
import pyscrypt
import os
import binascii
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# database connection
con = sqlite3.connect("./Database/store_system.db")
cur = con.cursor()

# load login window ui
loginUI, _ = loadUiType("./ui/login-dialog.ui")

regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$' 

# LoginWindow class will initialize the login.ui
class LoginDialog(QDialog, loginUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.cur = con.cursor()
        self.param = [None] * 2
        self.pushButtonCancel.clicked.connect(self.close_window)
        self.pushButtonLogin.clicked.connect(self.login)
        
    def login(self):
        self.param[0] = self.lineEditEmailAddress.text()
        self.param[1] = self.lineEditPassword.text()
        if(self.checkEmail()):
            self.validate_password()
        
    def checkEmail(self):
        if(re.search(regex_email, self.param[0])):
            return True
        else:
            self.showMessage("Error: Please enter a valid email.")
            return False
            
    def validate_password(self):
        hash_params = ""
        row = None
        sql = '''SELECT password FROM account WHERE email = ?'''
        params = (self.param[0],)
        self.cur.execute(sql, params)
        
        if(self.param[1] != ""): 
            row = self.cur.fetchone()[0]
            if(row is not None):
                hash_params = row.split("|")
                if(hash_params[5] == str(self.hash_password(self.param[1], hash_params[0], hash_params[1], hash_params[2], hash_params[3], hash_params[4]))): 
                    self.showMessage("Login Successful.")
                    self.accept()
                else:
                    self.showMessage("Password does not match.")
            else:
                self.showMessage("Error: Account does not exist.")
        else:
            self.showMessage("Please enter a password.")
            
    def showMessage(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
    
    def hash_password(self, string, param0, param1, param2, param3, param4):
        # Hash
        hashed = pyscrypt.hash(password = bytes(string, 'utf-8'),
                        salt = bytes(param4, 'utf-8'), 
                        N = int(param0), 
                        r = int(param1), 
                        p = int(param2), 
                        dkLen = int(param3))
         
        return hashed.hex()
            
    def close_window(self):
        self.lineEditEmailAddress.setText("")
        self.lineEditPassword.setText("")
        self.close()