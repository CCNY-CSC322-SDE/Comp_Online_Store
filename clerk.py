import sys
import PyQt5
import sqlite3
import datetime
import re
import binascii
import pyscrypt
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sqlite3 import Error

# load the UIs
clerkUI, _ = loadUiType("./ui/clerk.ui")
justificationUI, _ = loadUiType("./ui/justification-dialog.ui")
loginUI, _ = loadUiType("./ui/login-dialog.ui")
logoutUI, _ = loadUiType("./ui/logout-dialog.ui")

class LoginDialog(QDialog, loginUI):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.cur = store_db.cursor()
        self.param = [None] * 2
        self.pushButtonCancel.clicked.connect(self.close_window)
        self.pushButtonLogin.clicked.connect(self.login)
        self.parent = parent

    def login(self):
        self.param[0] = self.lineEditEmailAddress.text()
        self.param[1] = self.lineEditPassword.text()
        if(self.checkEmail()):
            if(self.validEmail()):
                if(self.rightAccType()):
                    self.validate_password()

    def checkEmail(self):
        regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if (re.search(regex_email, self.param[0])):
            return True
        else:
            self.showMessage("Error: Please enter a valid email.")
            return False
            
    def rightAccType(self):
        sql = '''SELECT supplier_acc.account_id FROM account LEFT JOIN supplier_acc ON account.account_id = supplier_acc.account_id WHERE email = ? AND supplier_name IS NOT NULL'''
        params = (self.param[0],)
        self.cur.execute(sql, params)
        row = self.cur.fetchone()
        if(row is not None):
            return True
        else:
            self.showMessage("User is not a clerk account.")
            return False
            
    def validEmail(self):
        sql = '''SELECT banned_emails, is_permaban, sent_notif FROM avoid_list WHERE banned_emails = ?'''
        params = (self.param[0],)
        self.cur.execute(sql, params)
        row = self.cur.fetchone()
        if(row is not None):
            if(row[1]):
                self.showMessage("User is permanently banned.")
            else:
                self.showMessage("User is suspended.")
            if(not row[2]):
                self.showMessage("Email is sent regarding details.")
                sql = '''UPDATE avoid_list SET sent_notif = 1 WHERE banned_emails = ?'''
                params = (self.param[0],)
                self.cur.execute(sql, params)
                
            return False
            store_db.commit()
        else:
            return True

    def validate_password(self):
        hash_params = ""
        row = None
        sql = '''SELECT account_id, password FROM account WHERE email = ?'''
        params = (self.param[0],)
        self.cur.execute(sql, params)

        if (self.param[1] != ""):
            row = self.cur.fetchone()
            if (row is not None):
                hash_params = row[1].split("|")
                if (hash_params[5] == str(
                        self.hash_password(self.param[1], hash_params[0], hash_params[1], hash_params[2],
                                           hash_params[3], hash_params[4]))):
                    self.showMessage("Login Successful.")
                    self.loadData(row[0])
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
        hashed = pyscrypt.hash(password=bytes(string, 'utf-8'),
                               salt=bytes(param4, 'utf-8'),
                               N=int(param0),
                               r=int(param1),
                               p=int(param2),
                               dkLen=int(param3))

        return hashed.hex()

    def loadData(self, acc_id):
        global user
        global cur
        sql = '''SELECT account.account_id, supplier_name FROM account LEFT JOIN supplier_acc ON account.account_id = supplier_acc.account_id WHERE account.account_id = ?'''
        params = (acc_id,)
        self.cur.execute(sql, params)
        user = self.cur.fetchone()
        self.close_window()
        self.parent.login_button_change()
        self.parent.fillComboBox()

    def close_window(self):
        self.lineEditEmailAddress.setText("")
        self.lineEditPassword.setText("")
        self.close()
        
class LogoutDialog(QDialog, logoutUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        
class JustificationDialog (QDialog, justificationUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

class ClerkApp(QMainWindow, clerkUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleButtons()
        self.fillTab(0)
        self.cur = store_db.cursor()
        self.offers = []
        self.loginWindow = None
        self.comboBoxBids.currentIndexChanged.connect(self.fillTab)
        self.verticalLayout.setAlignment(Qt.AlignTop)
        
    def fillComboBox(self):
        global open_orders
        for row in open_orders:
            self.comboBoxBids.addItem('Id: ' + str(row[0]))

        
    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())): 
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
                    
    def fillTab(self, index):
        self.deleteItemsOfLayout(self.verticalLayout)
        if (self.comboBoxBids.currentIndex() > 0):
            t_id = open_orders[self.comboBoxBids.currentIndex() - 1][0]
            sql = '''SELECT bid_offers.account_id, company_name, bid_amount FROM bid_offers INNER JOIN delivery_acc ON bid_offers.account_id = delivery_acc.account_id WHERE transaction_id = ? ORDER BY bid_amount ASC'''
            params = (t_id,)
            self.cur.execute(sql, params)
            self.offers = self.cur.fetchall()
            offer_count = len(self.offers)
        
            if(offer_count == 0):
                label = QLabel('No Bids')
                self.verticalLayout.addWidget(label)
            else:
                iter = 0
                for row in self.offers:
                    string = 'Company Name: ' + row[1] + '\nBid Amount: ' + str(row[2]) + '\n'
                    h_layout = QHBoxLayout()
                    label = QLabel(string)
                    label.setMinimumHeight(100)
                    button = QPushButton(text="Pick Bid", objectName= str(iter) + "_pick", clicked = self.pickBid)
                    button.setMaximumWidth(100)
                    h_layout.addWidget(label)
                    h_layout.addWidget(button)
                    self.verticalLayout.addLayout(h_layout)
                    iter += 1
        else: 
            label = QLabel('Select an order to view bids.')
            self.verticalLayout.addWidget(label)
        
    def pickBid(self):
        button = self.sender()
        index = int(re.sub('[^0-9]','', button.objectName()))
        msg = QMessageBox()
        global open_orders
        valid_transaction = True
        
        #check if not smallest bid
        if(index > 0):
            dia = JustificationDialog()
            entry = dia.exec_()
            if (entry == QDialog.Accepted):
                string = dia.textEdit.toPlainText()
                if(len(string) == 0):
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Operation Aborted. Try again.")
                    msg.setInformativeText("Please enter a justification.")
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    valid_transaction = False
                elif(len(string) > 255):
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Operation Aborted. Try again.")
                    msg.setInformativeText("Justification is too long.")
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    valid_transaction = False
                else:
                    sql = '''INSERT INTO complaint(offender_id, filed_on, claim, counter_claim) VALUES (?, ?, ?, ?)'''
                    params = (user[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Did not pick the cheapest bid", dia.textEdit.toPlainText())
                    self.cur.execute(sql, params)
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Justification sent successfully.")
                    msg.setInformativeText("A warning will be given if your appeal is rejected.")
                    msg.setWindowTitle("Confirmation")
                    msg.exec_()
            else:
                return
            
        if(valid_transaction):
            #set order status to 1 and shipper to bid winner
            sql = '''UPDATE user_orders SET order_status = 1, shipper = ? WHERE transaction_id = ?'''
            params = (self.offers[index][1], open_orders[self.comboBoxBids.currentIndex() - 1][0])
            self.cur.execute(sql, params)
            
            #delete bids for transaction
            sql = '''DELETE FROM bid_offers WHERE transaction_id = ?'''
            params = (open_orders[self.comboBoxBids.currentIndex() - 1][0],)
            self.cur.execute(sql, params)

            msg.setIcon(QMessageBox.Information)
            msg.setText("Picked Winner.")
            msg.setInformativeText("Update successful.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
            
            del open_orders[self.comboBoxBids.currentIndex() - 1]
            self.comboBoxBids.removeItem(self.comboBoxBids.currentIndex())
            
            store_db.commit()
        
    def refresh(self):
        global open_orders
        for i in range(self.comboBoxBids.count()):
            self.comboBoxBids.removeItem(1)
        open_orders = fetch_open_orders()
        
        self.fillComboBox()
    
    def handleButtons(self):
        self.pushButtonLogin.clicked.connect(self.openLoginWindow)
        self.pushButtonRefresh.clicked.connect(self.refresh) 
        self.pushButtonLogout.clicked.connect(self.logout)
        self.pushButtonLogout.hide()
        
    def openLoginWindow(self, checked):
        if self.loginWindow is None:
            self.loginWindow = LoginDialog(parent=self)
        self.loginWindow.exec_()
        
    def login_button_change(self):
        self.pushButtonLogin.hide()
        self.pushButtonLogout.show()
        
    def logout(self):
        dia = LogoutDialog()
        dia.setWindowTitle("Logout")
        entry = dia.exec_()
        msg = QMessageBox()
        if (entry == QDialog.Accepted):
            user = [None] * 2
            self.pushButtonLogin.show()
            self.pushButtonLogout.hide()
            for i in range(self.comboBoxBids.count() - 1):
                self.comboBoxBids.removeItem(1)
            self.offers = []
            msg.setIcon(QMessageBox.Information)
            msg.setText("Logged out.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
        else:
            return

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
    
def fetch_open_orders():
    cur = store_db.cursor()
    sql = '''SELECT transaction_id FROM user_orders WHERE order_status = 0 ORDER BY transaction_id ASC'''
    cur.execute(sql)
    rows =  cur.fetchall() 
    return rows
   
database = r"./Database/store_system.db"
store_db = create_connection(database)
#TEMP VARIABLE: placeholder until login system is coded
user = (8, 'clerk', 'man')
open_orders = fetch_open_orders()
        
# this main method is not inside the class, it is in the class level
# this method shows the main window
def main():
    app = QApplication(sys.argv)
    window = ClerkApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
