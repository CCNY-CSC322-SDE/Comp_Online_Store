import sys
import os
import PyQt5
import sqlite3
import datetime
import re
import binascii
import pyscrypt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sqlite3 import Error

# import user defined classes
from Prototypes.ProductInfo import ProductInfo
from Prototypes.ProductSearchWindow import ProductSearchWindow
from Prototypes.RegistrationWindow import RegistrationWindow
from Prototypes.CPUWindow import CPUWindow
from Prototypes.MotherboardWindow import MotherboardWindow
from Prototypes.MemoryRAMWindow import MemoryRAMWindow
from Prototypes.GPUWindow import GPUWindow
from Prototypes.CaseWindow import CaseWindow
from Prototypes.PSUWindow import PSUWindow
from Prototypes.StorageWindow import StorageWindow
from Prototypes.CPUCoolerWindow import CPUCoolerWindow
from Prototypes.OSWindow import OSWindow
from Prototypes.BusinessPCWindow import BusinessPCWindow
from Prototypes.ComputingPCWindow import ComputingPCWindow
from Prototypes.GamingPCWindow import GamingPCWindow
from Prototypes.BuildBusinessPCWithIntel import BuildBusinessPCWithIntel
from Prototypes.BuildBusinessPCWithAMD import BuildBusinessPCWithAMD

# connect to the database and create a cursor
import forum

con = sqlite3.connect("./Database/store_system.db")
cur = con.cursor()

# load the main window ui
mainUI, _ = loadUiType("./ui/mainwindow.ui")
cartUI, _ = loadUiType("./ui/cart.ui")
loginUI, _ = loadUiType("./ui/login-dialog.ui")
logoutUI, _ = loadUiType("./ui/logout-dialog.ui")

class CartWindow(QMainWindow, cartUI):  # LoginWindow class will initialize the login.ui
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.subtotal = 0
        self.cur = con.cursor()
        self.init_cart()
        self.verticalLayout.setAlignment(Qt.AlignTop)

        self.pushButton.clicked.connect(self.checkout)
        self.pushButton_2.clicked.connect(self.close_window)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def init_cart(self):
        global user_cart
        self.deleteItemsOfLayout(self.verticalLayout)
        self.subtotal = 0
        user_cart = fetch_cart()

        if(len(user_cart) == 0):
            label = QLabel('No items in cart.')
            self.verticalLayout.addWidget(label)
        else:
            count = 0
            for row in user_cart:
                string = 'Item Name: ' + \
                    row[0] + '\nPrice: ' + \
                    str(row[1]) + '\nAmount: ' + str(row[2]) + '\n'
                self.subtotal += (row[1] * row[2])
                h_layout = QHBoxLayout()
                label = QLabel(string)
                label.setMinimumHeight(100)
                button = QPushButton(text="Remove", objectName=str(
                    count) + "_remove", clicked=self.removeItem)
                button.setMaximumWidth(100)
                h_layout.addWidget(label)
                h_layout.addWidget(button)
                self.verticalLayout.addLayout(h_layout)
                count += 1

        self.label_3.setText("Subtotal: " + str(round(self.subtotal, 2)))

    def close_window(self):
        con.commit()
        self.close()

    def removeItem(self):
        global user_cart
        button = self.sender()
        index = int(re.sub('[^0-9]', '', button.objectName()))
        self.subtotal -= user_cart[index][1] * user_cart[index][2]
        sql = '''DELETE FROM cart WHERE account_id = ? and product_id = ?'''
        params = (user[0], user_cart[index][3])
        self.cur.execute(sql, params)
        self.deleteItemsOfLayout(self.verticalLayout.itemAt(index))
        self.label_3.setText("Subtotal: " + str(round(self.subtotal, 2)))

        con.commit()
        self.init_cart()

    def checkout(self):
        global user_cart
        msg = QMessageBox()

        if (self.radioButton.isChecked() and self.subtotal > user[1]):
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Insufficient Balance.")
            msg.setInformativeText("Please pick a different payment method.")
            msg.setWindowTitle("Error")
            msg.exec_()
        elif (user[2] == 'none'):
            # ASSUMES: user can only enter a valid credit card so credit card could only be a valid one or none
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No Credit Card on file.")
            msg.setInformativeText("Please pick a different payment method.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            # add transaction to transaction db
            sql = '''INSERT INTO user_orders(account_id, subtotal, purchase_date, date_shipped, tracking_no, order_status) VALUES (?,?,?,?,?,?)'''
            params = (user[0], self.subtotal, datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), "NULL", "NULL", 0)
            self.cur.execute(sql, params)
            transaction_id = self.cur.lastrowid

            # add purchased items to purchased items db
            for row in user_cart:
                sql = '''INSERT INTO purchased_items(transaction_id, item_name, amount, item_price, vote_score) VALUES (?,?,?,?,?)'''
                params = (transaction_id, row[0], row[2], row[1], "NULL")
                self.cur.execute(sql, params)

                sql = '''UPDATE product SET quantity_sold = quantity_sold + ? WHERE product_name = ?'''
                params = (row[2], row[0])
                self.cur.execute(sql, params)

            # clear user cart
            sql = '''DELETE FROM cart WHERE account_id = ?'''
            params = (user[0],)
            self.cur.execute(sql, params)

            # update user balance
            if(self.radioButton.isChecked()):
                sql = '''UPDATE personal_acc SET balance = ? WHERE account_id = ?'''
                params = (user[1] - self.subtotal, user[0])
                self.cur.execute(sql, params)

            msg.setIcon(QMessageBox.Information)
            msg.setText("Purchase successful.")
            msg.setInformativeText(
                "Processing your order can take a few business days.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
            self.close_window()

class LoginDialog(QDialog, loginUI): #INCOMPLETE: NEED TO CHECK IF USER IS BANNED
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.cur = con.cursor()
        self.param = [None] * 2
        self.pushButtonCancel.clicked.connect(self.close_window)
        self.pushButtonLogin.clicked.connect(self.login)
        self.parent = parent

    def login(self):
        self.param[0] = self.lineEditEmailAddress.text()
        self.param[1] = self.lineEditPassword.text()
        if(self.checkEmail()):
            self.validate_password()

    def checkEmail(self):
        regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex_email, self.param[0])):
            return True
        else:
            self.showMessage("Error: Please enter a valid email.")
            return False

    def validate_password(self):
        hash_params = ""
        row = None
        sql = '''SELECT account_id, password FROM account WHERE email = ?'''
        params = (self.param[0],)
        self.cur.execute(sql, params)

        if(self.param[1] != ""):
            row = self.cur.fetchone()
            if(row is not None):
                hash_params = row[1].split("|")
                if(hash_params[5] == str(self.hash_password(self.param[1], hash_params[0], hash_params[1], hash_params[2], hash_params[3], hash_params[4]))):
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
        sql = '''SELECT account.account_id, balance, credit_card FROM account LEFT JOIN personal_acc ON account.account_id = personal_acc.account_id WHERE account.account_id = ?'''
        params = (acc_id,)
        cur.execute(sql, params)
        user = cur.fetchone()
        self.close_window()
        self.parent.login_button_change()

    def close_window(self):
        self.lineEditEmailAddress.setText("")
        self.lineEditPassword.setText("")
        self.close()
        
class LogoutDialog (QDialog, logoutUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

# MainApp class will initialize the mainwindow.ui
class MainApp(QMainWindow, mainUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # set window icon and position
        self.setGeometry(250, 0, 1000, 750)
        self.setFixedSize(self.size())

        # other window instances
        self.loginWindow = None  # No external login window yet.
        self.registrationWindow = None  # No external registration window yet.
        self.searchWindow = None  # No external search window yet.
        self.productDetailsWindow = None
        self.cpuWindow = None
        self.motherboardWindow = None
        self.memoryRAMWindow = None
        self.gpuWindow = None
        self.caseWindow = None
        self.psuWindow = None
        self.storageWindow = None
        self.cpuCoolerWindow = None
        self.osWindow = None
        self.cartWindow = None
        self.businessPCWindow = None
        self.computingPCWindow = None
        self.gamingPCWindow = None
        self.buildBusinessPCWithIntel = None
        self.buildBusinessPCWithAMD = None

        # call methods
        self.mainWindowUI()

    def mainWindowUI(self):
        # call other methods
        self.handleButtons()
        self.openMacTab()
        self.openWindowsTab()
        self.openLinuxTab()
        # call the home tabs at last, so that home tab shows up when app is loaded
        self.openHomeTab()

    # handle button clicks
    def handleButtons(self):
        # open login window on button clicked
        self.pushButtonLogin.clicked.connect(self.openLoginWindow)
        # open registration window on button clicked
        self.pushButtonRegister.clicked.connect(self.openRegistrationWindow)
        # open search window on button clicked
        self.pushButtonSearch.clicked.connect(self.openSearchWindow)

        self.pushButtonCart.clicked.connect(self.openCartWindow)
        
        self.pushButtonLogout.clicked.connect(self.logout)
        self.pushButtonLogout.hide()
        
        self.pushButtonAccount.clicked.connect(self.openAccountWindow)
        self.pushButtonAccount.hide()

        # main navigation buttons
        self.pushButtonHome.clicked.connect(self.openHomeTab)
        self.pushButtonMac.clicked.connect(self.openMacTab)
        self.pushButtonWindows.clicked.connect(self.openWindowsTab)
        self.pushButtonLinux.clicked.connect(self.openLinuxTab)
        self.pushButtonPCBuilder.clicked.connect(self.openPCBuilderTab)
        self.pushButtonComponents.clicked.connect(self.openComponentsTab)
        self.pushButtonDiscussion.clicked.connect(self.openDiscussionTab)

        # connect tool buttons under components tab to methods
        self.toolButtonCPU.clicked.connect(self.openCPUWindow)
        self.toolButtonMotherboard.clicked.connect(self.openMotherboardWindow)
        self.toolButtonMemory.clicked.connect(self.openMemoryRAMWindow)
        self.toolButtonVideoCards.clicked.connect(self.openGPUWindow)
        self.toolButtonCase.clicked.connect(self.openCaseWindow)
        self.toolButtonPowerSupply.clicked.connect(self.openPowerSupplyWindow)
        self.toolButtonStorage.clicked.connect(self.openStorageWindow)
        self.toolButtonCPUCooler.clicked.connect(self.openCPUCoolerWindow)
        self.toolButtonOS.clicked.connect(self.openOSWindow)

        # connect push buttons under pc builder tab to methods
        self.pushButtonPreBuiltBusiness.clicked.connect(
            self.openBusinessPCWindow)

        self.pushButtonPreBuiltComputing.clicked.connect(
            self.openComputingPCWindow)

        self.pushButtonPreBuiltGaming.clicked.connect(
            self.openGamingPCWindow)

        self.pushButtonIntelBusiness.clicked.connect(
            self.openBuildBusinessPCWithIntel)

        self.pushButtonAMDBusiness.clicked.connect(
            self.openBuildBusinessPCWithAMD)

        ########## Handle double click events on the table items #########
 
        # when one of the suggested systems is double clicked
        self.tableWidgetSuggestedSystems.doubleClicked.connect(
            self.selectSuggestedProduct)

        # when one of the best seller items is double clicked
        self.tableWidgetBestSellers.doubleClicked.connect(
            self.selectBestSellerProduct)

        # when one of the mac system items is double clicked
        self.tableWidgetMacSystems.doubleClicked.connect(
            self.selectMacSystem)

        # when one of the mac system items is double clicked
        self.tableWidgetWindowsSystems.doubleClicked.connect(
            self.selectWindowsSystem)

        # when one of the mac system items is double clicked
        self.tableWidgetLinuxSystems.doubleClicked.connect(
            self.selectLinuxSystem)
            
    def login_button_change(self):
        self.pushButtonLogin.hide()
        self.pushButtonRegister.hide()
        self.pushButtonLogout.show()
        self.pushButtonAccount.show()

    def logout(self):
        dia = LogoutDialog()
        dia.setWindowTitle("Logout")
        entry = dia.exec_()
        msg = QMessageBox()
        if (entry == QDialog.Accepted):
            user = []
            self.pushButtonLogin.show()
            self.pushButtonRegister.show()
            self.pushButtonLogout.hide()
            self.pushButtonAccount.hide()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Logged out.")
            msg.setWindowTitle("Confirmation")
            msg.exec_()
        else:
            return

    ####### Open tabs when respective Main window buttons will be clicked #######

    def openHomeTab(self):  # open home tab when Home pushButton is clicked
        self.tabWidget.setCurrentIndex(0)
        # call methods to display suggested and best seller products
        self.displaySuggestedSystems()
        self.displayBestSellerProducts()

    def openMacTab(self):  # open mac tab when Mac pushButton is clicked
        self.tabWidget.setCurrentIndex(1)
        self.displayMacSystems()

    def openWindowsTab(self):  # open windows tab when Windows pushButton is clicked
        self.tabWidget.setCurrentIndex(2)
        self.displayWindowsSystems()

    def openLinuxTab(self):  # open linux tab when Linux pushButton is clicked
        self.tabWidget.setCurrentIndex(3)
        self.displayLinuxSystems()

    def openPCBuilderTab(self):  # open pcBuilder tab when PCBuilder pushButton is clicked
        self.tabWidget.setCurrentIndex(4)

    # open components tab when Components pushButton is clicked
    def openComponentsTab(self):
        self.tabWidget.setCurrentIndex(5)

    # open Discussion tab when Discussion pushButton is clicked
    def openDiscussionTab(self):
        self.tabWidget.setCurrentIndex(6)
        forumApp = forum.ForumApp(parent=self)
        forumApp.show()

    # this method will create and show the login window, when Login pushButton is clicked
    def openRegistrationWindow(self, checked):
        if self.registrationWindow is None:
            self.registrationWindow = RegistrationWindow()
        self.registrationWindow.show()

    # this method will create and open the login window, when Login pushButton is clicked
    def openLoginWindow(self, checked):
        if self.loginWindow is None:
            self.loginWindow = LoginDialog(parent = self)
        self.loginWindow.exec_() 

    def openSearchWindow(self, checked):
        if self.searchWindow is None:
            searchQuery = "Macbook Pro"
            self.searchWindow = ProductSearchWindow()
        self.searchWindow.show()

    def openCartWindow(self, checked):
        if self.cartWindow is None:
            self.cartWindow = CartWindow()
        self.cartWindow.init_cart()
        self.cartWindow.show()

    def openAccountWindow(self, checked):
        pass
        
    # this method will create and open the product details window, when products are double clicked
    def openProductInfoWindow(self, productId):
        self.productInfoWindow = ProductInfo(productId, user)
        self.productInfoWindow.show()

    # open CPU window and list CPUs
    def openCPUWindow(self):
        self.cpuWindow = CPUWindow(user)
        self.cpuWindow.show()

    # open Motherboard window and list CPUs
    def openMotherboardWindow(self):
        self.motherboardWindow = MotherboardWindow(user)
        self.motherboardWindow.show()

    # open Memory RAM window and list CPUs
    def openMemoryRAMWindow(self):
        self.memoryRAMWindow = MemoryRAMWindow(user)
        self.memoryRAMWindow.show()

    # open gpu window and list CPUs
    def openGPUWindow(self):
        self.gpuWindow = GPUWindow(user)
        self.gpuWindow.show()

    # open case window and list CPUs
    def openCaseWindow(self):
        self.caseWindow = CaseWindow(user)
        self.caseWindow.show()

    # open case window and list CPUs
    def openPowerSupplyWindow(self):
        self.psuWindow = PSUWindow(user)
        self.psuWindow.show()

    # open case window and list CPUs
    def openStorageWindow(self):
        self.storageWindow = StorageWindow(user)
        self.storageWindow.show()

    # open case window and list CPUs
    def openCPUCoolerWindow(self):
        self.cpuCoolerWindow = CPUCoolerWindow(user)
        self.cpuCoolerWindow.show()

    # open case window and list CPUs
    def openOSWindow(self):
        self.osWindow = OSWindow(user)
        self.osWindow.show()

    # open case window and list CPUs
    def openBusinessPCWindow(self):
        self.businessPCWindow = BusinessPCWindow()
        self.businessPCWindow.show()

    # open case window and list CPUs
    def openComputingPCWindow(self):
        self.computingPCWindow = ComputingPCWindow()
        self.computingPCWindow.show()

    # open case window and list CPUs
    def openGamingPCWindow(self):
        self.gamingPCWindow = GamingPCWindow()
        self.gamingPCWindow.show()

    # open business pc
    def openBuildBusinessPCWithIntel(self):
        self.buildBusinessPCWithIntel = BuildBusinessPCWithIntel()
        self.buildBusinessPCWithIntel.show()

    # open business pc
    def openBuildBusinessPCWithAMD(self):
        self.buildBusinessPCWithAMD = BuildBusinessPCWithAMD()
        self.buildBusinessPCWithAMD.show()

    ####### display products on the table widgets #########

    # this method will display the suggested systems
    def displaySuggestedSystems(self):
        # hide the product id column
        self.tableWidgetSuggestedSystems.setColumnHidden(0, True)
        self.tableWidgetSuggestedSystems.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetSuggestedSystems.rowCount())):
            self.tableWidgetSuggestedSystems.removeRow(i)

        # sql query to retrieve suggested systems from db
        sql = ''' SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
                 FROM product
                 INNER JOIN system ON product.product_id = system.product_id
                 LIMIT 3 '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetSuggestedSystems
        for row_data in query:

            row_number = self.tableWidgetSuggestedSystems.rowCount()
            self.tableWidgetSuggestedSystems.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set text data to item
                item.setTextAlignment(Qt.AlignHCenter)  # change the alignment
                self.tableWidgetSuggestedSystems.setItem(  # set item on tableWidget
                    row_number, column_number, item)

        self.tableWidgetSuggestedSystems.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # this method will display the best sellers items
    def displayBestSellerProducts(self):
        # hide the product id column
        self.tableWidgetBestSellers.setColumnHidden(0, True)
        self.tableWidgetBestSellers.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetBestSellers.rowCount())):
            self.tableWidgetBestSellers.removeRow(i)

        # sql query to retrieve best selling products from db
        sql = ''' SELECT product.product_id as id, 
                        product_name, 
                        price, cpu, gpu, ram_size, 
                        hdd_size, operating_system, 
                        quantity_sold
                FROM product
                INNER JOIN system ON product.product_id = system.product_id
                ORDER BY product.quantity_sold DESC
                LIMIT 3 '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetBestSellers
        for row_data in query:
            row_number = self.tableWidgetBestSellers.rowCount()  # count number of rows
            self.tableWidgetBestSellers.insertRow(row_number)

            # insert data on each column
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set data
                item.setTextAlignment(Qt.AlignHCenter)  # change the alignment
                self.tableWidgetBestSellers.setItem(
                    row_number, column_number, item)  # set item on tableWidget

        self.tableWidgetBestSellers.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # this method will display the Mac systems
    def displayMacSystems(self):
        # hide the product id column
        self.tableWidgetMacSystems.setColumnHidden(0, True)
        self.tableWidgetMacSystems.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetMacSystems.rowCount())):
            self.tableWidgetMacSystems.removeRow(i)

        # sql query to retrieve mac systems
        sql = ''' SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
                FROM product
                INNER JOIN system ON product.product_id = system.product_id
                WHERE  UPPER( product_name) LIKE '%MAC%' and UPPER( operating_system) LIKE '%MAC%' '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetMacSystems
        for row_data in query:
            row_number = self.tableWidgetMacSystems.rowCount()  # count number of rows
            self.tableWidgetMacSystems.insertRow(row_number)

            # insert data on each column
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set data
                item.setTextAlignment(Qt.AlignHCenter)  # change the alignment
                self.tableWidgetMacSystems.setItem(
                    row_number, column_number, item)  # set item on tableWidget

        # turn off the table edit option
        self.tableWidgetMacSystems.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # this method will display the windows systems
    def displayWindowsSystems(self):
        # hide the product id column
        self.tableWidgetWindowsSystems.setColumnHidden(0, True)
        self.tableWidgetWindowsSystems.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetWindowsSystems.rowCount())):
            self.tableWidgetWindowsSystems.removeRow(i)

        # sql query to retrieve windows systems
        sql = ''' SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
                FROM product
                INNER JOIN system ON product.product_id = system.product_id
                WHERE  UPPER(operating_system) LIKE '%WINDOWS%' '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetMacSystems
        for row_data in query:
            row_number = self.tableWidgetWindowsSystems.rowCount()  # count number of rows
            self.tableWidgetWindowsSystems.insertRow(row_number)

            # insert data on each column
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set data
                item.setTextAlignment(Qt.AlignHCenter)  # change the alignment
                self.tableWidgetWindowsSystems.setItem(
                    row_number, column_number, item)  # set item on tableWidget

        # turn off the table edit option
        self.tableWidgetWindowsSystems.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # this method will display the linux systems
    def displayLinuxSystems(self):
        # hide the product id column
        self.tableWidgetLinuxSystems.setColumnHidden(0, True)
        self.tableWidgetLinuxSystems.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetLinuxSystems.rowCount())):
            self.tableWidgetLinuxSystems.removeRow(i)

        # sql query to retrieve mac systems
        sql = ''' SELECT product.product_id as id, product_name, price, cpu, gpu, ram_size, hdd_size, operating_system
                FROM product
                INNER JOIN system ON product.product_id = system.product_id
                WHERE  UPPER(operating_system) LIKE '%LINUX%' '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetMacSystems
        for row_data in query:
            row_number = self.tableWidgetLinuxSystems.rowCount()  # count number of rows
            self.tableWidgetLinuxSystems.insertRow(row_number)

            # insert data on each column
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set data
                item.setTextAlignment(Qt.AlignHCenter)  # change the alignment
                self.tableWidgetLinuxSystems.setItem(
                    row_number, column_number, item)  # set item on tableWidget

        # turn off the table edit option
        self.tableWidgetLinuxSystems.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    ######## show product info and rating and discussion of each product ########

    # select suggested product that will be added to the cart
    def selectSuggestedProduct(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetSuggestedSystems.item(
                self.tableWidgetSuggestedSystems.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openProductInfoWindow(productId)

    # select best seller product that will be added to the cart
    def selectBestSellerProduct(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetBestSellers.item(
                self.tableWidgetBestSellers.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openProductInfoWindow(productId)

    # select mac system that will be added to the cart
    def selectMacSystem(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetMacSystems.item(
                self.tableWidgetMacSystems.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openProductInfoWindow(productId)

    # select windows system that will be added to the cart
    def selectWindowsSystem(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetWindowsSystems.item(
                self.tableWidgetWindowsSystems.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openProductInfoWindow(productId)

    # select linux system product that will be added to the cart
    def selectLinuxSystem(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetLinuxSystems.item(
                self.tableWidgetLinuxSystems.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openProductInfoWindow(productId)


def fetch_cart():
    cur = con.cursor()
    sql = '''SELECT product_name, price, amount, cart.product_id FROM cart INNER JOIN product ON cart.product_id = product.product_id WHERE account_id = ?'''
    params = (user[0],)
    cur.execute(sql, params)
    rows = cur.fetchall()
    return rows


user = []
user_cart = []

# this main method is not inside the class, it is in the class level
# this method shows the main window


def main():
    app = QApplication(sys.argv)
    # set app icon
    app.setWindowIcon(QIcon("./icons/online-shopping.svg"))
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
