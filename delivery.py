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
        self.fillTabs()
        self.offers = []
        
    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())): 
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
                    
    def fillTabs(self):
        self.deleteItemsOfLayout(self.verticalLayout)
        self.deleteItemsOfLayout(self.verticalLayout_2)
        self.deleteItemsOfLayout(self.verticalLayout_3)

        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, user_orders.transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE order_status = 0 AND user_orders.transaction_id != (SELECT user_orders.transaction_id FROM user_orders LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE bid_offers.account_id = ? OR bid_offers.account_id = NULL)'''
        #sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, user_orders.transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE order_status = 0'''
        params = (user[0],)
        self.cur.execute(sql, params)
        self.orders_no_bid = self.cur.fetchall()
        
        
        #sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, bid_amount FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE order_status = 0 AND transaction_id = (SELECT user_orders.transaction_id FROM user_orders LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE bid_offers.account_id = ?)'''
        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, bid_amount, user_orders.transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id LEFT JOIN bid_offers ON user_orders.transaction_id = bid_offers.transaction_id WHERE order_status = 0 AND bid_offers.account_id = ?'''
        params = (user[0],)
        self.cur.execute(sql, params)
        self.orders_bid = self.cur.fetchall()
        
        #OPTIONAL: optimize
        #for row in orders_no_bid:
         #   if(row[6
        
        sql = '''SELECT first_name, last_name, address, subtotal, purchase_date, transaction_id FROM user_orders LEFT JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE shipper == ? AND order_status != 2'''
        params = (user[1],)
        self.cur.execute(sql, params)
        self.orders_to_ship = self.cur.fetchall()
            
        if(len(self.orders_no_bid) == 0):
            label = QLabel('No Open Orders.')
            self.verticalLayout.addWidget(label)
        else:
            iter = 0
            for row in self.orders_no_bid:
                #TO ADD: minimum height and maximum width to widgets
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(row[3]) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                button = QPushButton(text="Put Offer", objectName= str(iter) + "_pick", clicked = self.pickOffer)
                h_layout.addWidget(label)
                h_layout.addWidget(button)
                self.verticalLayout.addLayout(h_layout)
                iter += 1
                
        if(len(self.orders_bid) == 0):
            label = QLabel('No Pending Bids.')
            self.verticalLayout_2.addWidget(label)
        else:
            iter = 0
            for row in self.orders_bid:
                #TO ADD: minimum height and maximum width to widgets
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(row[3]) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                label_2 = QLabel('Bid Offer: ' + str(row[5]))
                h_layout.addWidget(label)
                h_layout.addWidget(label_2)
                self.verticalLayout_2.addLayout(h_layout)
                iter += 1
                
        if(len(self.orders_to_ship) == 0):
            label = QLabel('No Won Bids to Ship.')
            self.verticalLayout_3.addWidget(label)
        else:
            iter = 0
            for row in self.orders_to_ship:
                #TO ADD: minimum height and maximum width to widgets
                string = 'Name: ' + row[0] + ' ' + row[1] + '\nAddress: ' + row[2] + '\nSubtotal: ' + str(row[3]) + '\nDate Purchased: ' + row[4] + '\n'
                h_layout = QHBoxLayout()
                label = QLabel(string)
                button = QPushButton(text="Ship Order", objectName= str(iter) + "_", clicked = self.shipOrder)
                h_layout.addWidget(label)
                h_layout.addWidget(button)
                self.verticalLayout_3.addLayout(h_layout)
                iter += 1

        
    def pickOffer(self):
        button = self.sender()
        index = int(re.sub('[^0-9]','', button.objectName()))
        msg = QMessageBox()
        
        dia = BiddingDialog()
        entry = dia.exec_()
        if (entry == QDialog.Accepted):
            string = dia.lineEdit.text()
            #TO ADD: string checker for valid bid offer
            #TO ADD: setting precision for floats
            sql = '''INSERT INTO bid_offers VALUES (?, ?, ?)'''
            params = (user[0], self.orders_no_bid[index][5], float(string))
            self.cur.execute(sql, params)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Bid Offer sent.")
            msg.setInformativeText("If your offer wins, it will show in the won bids tab.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
        else:
            return
        
        item = self.verticalLayout.itemAt(index).takeAt(0)
        label = item.widget()
        if label is not None:
            label.setParent(None)
        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        label_2 = QLabel('Bid Offer: ' + string)
        h_layout.addWidget(label_2)
        if(len(self.orders_bid) == 0):
            self.deleteItemsOfLayout(self.verticalLayout_2)
        self.verticalLayout_2.addLayout(h_layout)
        self.deleteItemsOfLayout(self.verticalLayout.itemAt(index))
        self.orders_bid.append(self.orders_no_bid[index])
        del self.orders_no_bid[index]
        if(len(self.orders_no_bid) == 0):
            label = QLabel('No Open Orders.')
            self.verticalLayout.addWidget(label)    
        
        store_db.commit()
        
    def shipOrder(self):
        button = self.sender()
        index = int(re.sub('[^0-9]','', button.objectName()))
        msg = QMessageBox()
        
        dia = TrackingDialog()
        entry = dia.exec_()
        if (entry == QDialog.Accepted):
            string = dia.lineEdit.text()
            #TO ADD: string checker for valid tracking no
            sql = '''UPDATE user_orders SET date_shipped = ?, tracking_no = ?, order_status = 2 WHERE transaction_id = ?'''
            params = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(string), self.orders_to_ship[index][5])
            self.cur.execute(sql, params)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Order shipped.")
            msg.setInformativeText("The user is notified of their tracking number.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
        else:
            return
        
        
        self.deleteItemsOfLayout(self.verticalLayout_3.itemAt(index))
        del self.orders_to_ship[index]
        if(len(self.orders_to_ship) == 0):
            label = QLabel('No Won Bids to Ship.')
            self.verticalLayout_3.addWidget(label)
        
        store_db.commit()
        
    def refresh(self):
        self.fillTabs()
    
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
   
database = r"./Database/store_system.db"
store_db = create_connection(database)
#TEMP VARIABLE: placeholder until login system is coded
user = (3, 'shipper')
        
# this main method is not inside the class, it is in the class level
# this method shows the main window
def main():
    app = QApplication(sys.argv)
    window = DeliveryApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
