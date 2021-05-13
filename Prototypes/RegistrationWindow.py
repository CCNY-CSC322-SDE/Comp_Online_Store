import sqlite3
import re
import pyscrypt
import os
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUiType
from sqlite3 import Error


# database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


database = r"./Database/store_system.db"
store_db = create_connection(database)
regex_name = "^[A-z](?:[A-z]|[-|'](?=[A-z]))*$"
regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$' 

# load registration window ui
registerUI, _ = loadUiType("./ui/register.ui")

# RegistrationWindow class will initialize the register.ui
class RegistrationWindow(QWidget, registerUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.lineEditFirstName.text()
        self.lineEditLastName.text()
        self.lineEditEmail.text()
        self.lineEditAddress.text()
        self.lineEditCreditCardNo.text()
        self.lineEditPassword_1.text()
        self.lineEditPassword_2.text()
        self.cur = store_db.cursor()
        self.pushButtonCancel.clicked.connect(self.close_window)
        self.pushButtonRegister.clicked.connect(self.register)
        self.valid_registration = None
        self.hashed_pw = ""
        
    # Register Button
    def register(self):
        self.valid_registration = True
        fname = self.lineEditFirstName.text()
        lname = self.lineEditLastName.text()
        emails = self.lineEditEmail.text()
        address = self.lineEditAddress.text()
        credit = self.lineEditCreditCardNo.text()
        password1 = self.lineEditPassword_1.text()
        password2 = self.lineEditPassword_2.text()

        if self.checkFields(fname, lname, emails, address, credit, password1, password2):
            self.showMessage("Error: All fields must be filled.")
        else:
            self.validFname(fname)
            self.validLname(lname)
            self.validAddress(address)
            self.validCC(credit)
            valid_email = self.checkEmail(emails)
            if(not self.emailAvoided(emails, valid_email)):
                if(not self.emailExist(emails, valid_email)):
                    if(self.checkPassword(password1, password2) and self.valid_registration):
                        self.hashed_pw = self.hash_password(password1)
                        self.addAccount(fname, lname, address, credit, emails, self.hashed_pw)
                        store_db.commit()
                        self.close_window()

    # Display error messages
    def showMessage(self, msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    # Check if any text field is empty
    def checkFields(self, fname, lname, email, address, credit, password1, password2):
        if fname == "" or lname == "" or address == "" or email == "" or credit == "" or password1 == "" or password2 == "":
            return True

    def validFname(self, string):
        if(re.search(regex_name, string)):
            self.lineEditFirstName.setStyleSheet("background: white;")
        else:
            self.lineEditFirstName.setStyleSheet("background: rgb(250, 92, 92);")
            self.valid_registration = False       
            
    def validLname(self, string):
        if(re.search(regex_name, string)):
            self.lineEditLastName.setStyleSheet("background: white;")
        else:
            self.lineEditLastName.setStyleSheet("background: rgb(250, 92, 92);")
            self.valid_registration = False    
            
    def validAddress(self, string):
        if(len(string) > 0 and len(string) < 256 and string != "[Enter a Valid Address]"):
            self.lineEditAddress.setStyleSheet("background: white;")
        else:
            self.lineEditAddress.setStyleSheet("background: rgb(250, 92, 92);")
            self.valid_registration = False
            
    def validCC(self, string):
        if(string.isnumeric() and (len(string) == 15 or len(string) == 16)):
            self.lineEditCreditCardNo.setStyleSheet("background: white;")
        else:
            self.lineEditCreditCardNo.setText("[Enter a Valid Credit Card]")
            self.lineEditCreditCardNo.setStyleSheet("background: rgb(250, 92, 92);")
            self.valid_registration = False 
            
    # Check if the format of email is correct
    def checkEmail(self,email):
        if(re.search(regex_email, email)):
            self.lineEditEmail.setStyleSheet("background: white;")
            return True
        else:
            self.lineEditEmail.setStyleSheet("background: rgb(250, 92, 92);")
            self.showMessage("Error: Invalid Email.\nAll other errors are highlighted red.")
            self.valid_registration = False
            return False

    # Check if the email is avoided
    def emailAvoided(self, email, valid_email):
        if(valid_email):
            sql = '''SELECT is_permaban FROM avoid_list WHERE banned_emails = ? AND is_permaban = ?'''
            self.cur.execute(sql,(str(email),1,))
            row = self.cur.fetchone()
            if (row is not None):
                if(self.cur.fetchone()[0]):
                    self.showMessage("Error: Email is permanently banned.\nAll other errors are highlighted red.")
                else:
                    self.showMessage("Error: Email is suspended.\nAll other errors are highlighted red.")
                self.lineEditEmail.setStyleSheet("background: rgb(250, 92, 92);")
                self.valid_registration = False
                return True
            else:
                return False

    # Check if the email was registered
    def emailExist(self, email, valid_email):
        if(valid_email):
            sql = '''SELECT * FROM account WHERE email = ?'''
            self.cur.execute(sql,(str(email),))
            row = self.cur.fetchall()
            if len(row) > 0:
                self.lineEditEmail.setStyleSheet("background: rgb(250, 92, 92);")
                self.showMessage("Error: Email is already registered to an account.\nAll other errors are highlighted red.")
                self.valid_registration = False
                return True
            else:
                self.lineEditEmail.setStyleSheet("background: white;")
                return False
            
    # Check if two password match
    def checkPassword(self, password1, password2):
        if(password1 == password2):
            self.lineEditPassword_1.setStyleSheet("background: white;")
            self.lineEditPassword_2.setStyleSheet("background: white;")
            return True
        else:
            self.lineEditPassword_1.setStyleSheet("background: rgb(250, 92, 92);")
            self.lineEditPassword_2.setStyleSheet("background: rgb(250, 92, 92);")
            self.lineEditPassword_1.setText("")
            self.lineEditPassword_2.setText("")
            self.showMessage("Error: Passwords do not match.\nAll other errors are highlighted red.")
            return False
    
    # Add the registered account to database
    def addAccount(self, fname, lname, address, credit, emails, password1):
        sql = '''INSERT INTO account (email,password) VALUES (?,?)'''
        self.cur.execute(sql, (str(emails), self.hashed_pw,))
        account_id = self.cur.lastrowid

        if(credit != ""):
            sql = '''INSERT INTO personal_acc (account_id,first_name,last_name,address,credit_card) VALUES (?,?,?,?,?)'''
            self.cur.execute(sql, (account_id,str(fname),str(lname),str(address),credit,))
        else:
            sql = '''INSERT INTO personal_acc (account_id,first_name,last_name,address) VALUES (?,?,?,?,?)'''
            self.cur.execute(sql, (account_id,str(fname),str(lname),str(address),))
            
        self.showMessage("Success: Login now")

    # Close registration form
    def close_window(self):
        self.lineEditFirstName.setText("")
        self.lineEditLastName.setText("")
        self.lineEditEmail.setText("")
        self.lineEditAddress.setText("")
        self.lineEditCreditCardNo.setText("")
        self.lineEditPassword_1.setText("")
        self.lineEditPassword_2.setText("")
        self.close()
        
    def hash_password(self, string):
        if(len(string) > 0):
            salt_base = binascii.hexlify(os.urandom(5)).decode()
            # Hash
            hashed = pyscrypt.hash(password = bytes(string, 'utf-8'),
                           salt = bytes(salt_base, 'utf-8'), 
                           N = 1024, 
                           r = 1, 
                           p = 1, 
                           dkLen = 16)
            
            self.showMessage(str(bytes(salt_base, 'utf-8')))
            self.showMessage("Success: Login now")
            pw = ('|'.join(["1024","1","1","16",salt_base,str(hashed.hex())]))
            self.lineEditPassword_1.setStyleSheet("background: white;")
            self.lineEditPassword_2.setStyleSheet("background: white;")
            return pw