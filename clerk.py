import sys
import PyQt5
import sqlite3
import datetime
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sqlite3 import Error

# load the UIs
clerkUI, _ = loadUiType("./ui/clerk.ui")
justificationUI, _ = loadUiType("./ui/justification-dialog.ui")
        
class JustificationDialog (QDialog, justificationUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

class ClerkApp(QMainWindow, clerkUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleButtons()
        self.fillComboBox()
        self.fillTab(0)
        self.cur = store_db.cursor()
        self.offers = []
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
        self.pushButtonRefresh.clicked.connect(self.refresh) 

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
