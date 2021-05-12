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
deliveryUI, _ = loadUiType("./ui/delivery.ui")
bidUI, _ = loadUiType("./ui/bid-dialog.ui")
trackingUI, _ = loadUiType("./ui/track-no-dialog.ui")
        
class BiddingDialog (QDialog, bidUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)        
 
class TrackingDialog (QDialog, trackingUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

class DeliveryApp(QMainWindow, deliveryUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleButtons()
        self.cur = store_db.cursor()
        self.fillTab1()
        self.fillTab2()
        self.fillTab3()
        self.offers = []
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.verticalLayout_2.setAlignment(Qt.AlignTop)
        self.verticalLayout_3.setAlignment(Qt.AlignTop)
        
    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())): 
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
                    
    def fillTab1(self):
        self.deleteItemsOfLayout(self.verticalLayout)

        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, user_orders.transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE order_status = 0 AND (user_orders.transaction_id != (SELECT user_orders.transaction_id FROM user_orders LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE bid_offers.account_id = ?) OR (SELECT user_orders.transaction_id FROM user_orders LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE bid_offers.account_id = ?) IS NULL)'''
        params = (user[0], user[0])
        self.cur.execute(sql, params)
        self.orders_no_bid = self.cur.fetchall()
        
        if(len(self.orders_no_bid) == 0):
            label = QLabel('No Open Orders.')
            self.verticalLayout.addWidget(label)
        else:
            iter = 0
            for row in self.orders_no_bid:
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(round(row[3],2)) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                label.setMinimumHeight(100)
                button = QPushButton(text="Put Offer", objectName= str(iter) + "_pick", clicked = self.pickOffer)
                button.setMaximumWidth(100)
                h_layout.addWidget(label)
                h_layout.addWidget(button)
                self.verticalLayout.addLayout(h_layout)
                iter += 1
                
    def fillTab2(self):    
        self.deleteItemsOfLayout(self.verticalLayout_2)
        
        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, bid_amount, user_orders.transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE order_status = 0 AND bid_offers.account_id = ?'''
        params = (user[0],)
        self.cur.execute(sql, params)
        self.orders_bid = self.cur.fetchall()
        
        if(len(self.orders_bid) == 0):
            label = QLabel('No Pending Bids.')
            self.verticalLayout_2.addWidget(label)
        else:
            iter = 0
            for row in self.orders_bid:
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(round(row[3],2)) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                label.setMinimumHeight(100)
                label_2 = QLabel('Bid Offer: ' + str(row[5]))
                label.setMinimumHeight(100)
                h_layout.addWidget(label)
                h_layout.addWidget(label_2)
                self.verticalLayout_2.addLayout(h_layout)
                iter += 1
        
    def fillTab3(self):
        self.deleteItemsOfLayout(self.verticalLayout_3)
        
        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE shipper == ? AND order_status != 2'''
        params = (user[1],)
        self.cur.execute(sql, params)
        self.orders_to_ship = self.cur.fetchall()
        
        if(len(self.orders_to_ship) == 0):
            label = QLabel('No Won Bids to Ship.')
            self.verticalLayout_3.addWidget(label)
        else:
            iter = 0
            for row in self.orders_to_ship:
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(round(row[3],2)) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                label.setMinimumHeight(100)
                button = QPushButton(text="Ship Order", objectName= str(iter) + "_", clicked = self.shipOrder)
                button.setMaximumWidth(100)
                h_layout.addWidget(label)
                h_layout.addWidget(button)
                self.verticalLayout_3.addLayout(h_layout)
                iter += 1
        
        
    def pickOffer(self):
        button = self.sender()
        index = int(re.sub('[^0-9]','', button.objectName()))
        msg = QMessageBox()
        
        dia = BiddingDialog()
        dia.setWindowTitle("Bid Offer")
        entry = dia.exec_()
        if (entry == QDialog.Accepted):
            string = dia.lineEdit.text()
            if(isFloat(string)):
                sql = '''INSERT INTO bid_offers VALUES (?, ?, ?)'''
                params = (user[0], self.orders_no_bid[index][5], float(string))
                self.cur.execute(sql, params)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Bid Offer sent.")
                msg.setInformativeText("If your offer wins, it will show in the won bids tab.")
                msg.setWindowTitle("Confirmation")
                msg.exec_()
            else:
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please enter a number.")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            return   
        
        store_db.commit()
        self.fillTab1()
        self.fillTab2()
        
    def shipOrder(self):
        button = self.sender()
        index = int(re.sub('[^0-9]','', button.objectName()))
        msg = QMessageBox()
        
        dia = TrackingDialog()
        dia.setWindowTitle("Tracking")
        entry = dia.exec_()
        if (entry == QDialog.Accepted):
            string = dia.lineEdit.text()
            if(string.isnumeric()):
                sql = '''UPDATE user_orders SET date_shipped = ?, tracking_no = ?, order_status = 2 WHERE transaction_id = ?'''
                params = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(string), self.orders_to_ship[index][5])
                self.cur.execute(sql, params)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Order shipped.")
                msg.setInformativeText("The user is notified of their tracking number.")
                msg.setWindowTitle("Confirmation")
                msg.exec_()
            else:
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please enter a valid tracking number.")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            return
        
        store_db.commit()
        self.fillTab3()
        
    def refresh(self):
        self.fillTab1()
        self.fillTab2()
        self.fillTab3()
    
    def pickOrder(self):
        return
    
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
    
def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
   
database = r"./Database/store_system.db"
store_db = create_connection(database)
#TEMP VARIABLE: placeholder until login system is coded
user = (6, 'shipper')
        
# this main method is not inside the class, it is in the class level
# this method shows the main window
def main():
    app = QApplication(sys.argv)
    window = DeliveryApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
