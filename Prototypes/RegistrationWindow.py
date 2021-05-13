import sqlite3
import re

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
        
    # Register Button
    def register(self):
        fname = self.lineEditFirstName.text()
        lname = self.lineEditLastName.text()
        emails = self.lineEditEmail.text()
        address = self.lineEditAddress.text()
        credit = self.lineEditCreditCardNo.text()
        password1 = self.lineEditPassword_1.text()
        password2 = self.lineEditPassword_2.text()

        if self.checkFields(fname, lname, emails, address, credit, password1, password2):
            self.showMessage("Error: All fields must be filled")
        elif self.checkEmail(emails):
            self.showMessage("Error: Invalid email")
        elif self.emailAvoided(emails):
            self.showMessage("Error: Email is banned")
        elif self.emailExist(emails):
            self.showMessage("Error: Email is registered")
        else:
            if self.checkPassword(password1, password2):
                self.showMessage("Success: Login now")
                self.addAccount(fname, lname, address, credit, emails, password1)
                store_db.commit()
                self.close()
            else:
                self.showMessage("Error: Passwords do not match")
                
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

    # Check if the format of email is correct
    def checkEmail(self,email):
        regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if regex.match(email):
            return False

    # Check if the email is avoided
    def emailAvoided(self, email):
        sql = '''SELECT * FROM avoid_list WHERE banned_emails = ? AND is_permaban = ?'''
        self.cur.execute(sql,(str(email),1,))
        row = self.cur.fetchall()
        if len(row) > 0:
            return True

    # Check if the email was registered
    def emailExist(self, email):
        sql = '''SELECT * FROM account WHERE email = ?'''
        self.cur.execute(sql,(str(email),))
        row = self.cur.fetchall()
        if len(row) > 0:
            return True

    # Check if two password match
    def checkPassword(self, password1, password2):
        return password1 == password2
    
    # Add the registered account to database
    def addAccount(self, fname, lname, address, credit, emails, password1):
        sql = '''INSERT INTO account (email,password) VALUES (?,?)'''
        self.cur.execute(sql, (str(emails), str(password1),))

        sql = '''SELECT account_id FROM account WHERE email = ?'''
        self.cur.execute(sql, (str(emails),))
        result = self.cur.fetchone()[0]

        sql = '''INSERT INTO personal_acc (account_id,first_name,last_name,address,credit_card) VALUES (?,?,?,?,?)'''
        self.cur.execute(sql, (result,str(fname),str(lname),str(address),credit,))

    # Close registration form
    def close_window(self):
        store_db.commit()
        self.close()
