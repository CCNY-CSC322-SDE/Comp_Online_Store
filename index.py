import sys
import os
import PyQt5
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# import user defined classes
from Prototypes.ProductInfo import ProductInfo
from Prototypes.ProductSearchWindow import ProductSearchWindow
from Prototypes.RegistrationWindow import RegistrationWindow
from Prototypes.LoginWindow import LoginWindow
from Prototypes.CPUWindow import CPUWindow
from Prototypes.MotherboardWindow import MotherboardWindow

# connect to the database and create a cursor
con = sqlite3.connect("./Database/store_system.db")
cur = con.cursor()

# load the main window ui
mainUI, _ = loadUiType("./ui/mainwindow.ui")


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

        # main navigation buttons
        self.pushButtonHome.clicked.connect(self.openHomeTab)
        self.pushButtonMac.clicked.connect(self.openMacTab)
        self.pushButtonWindows.clicked.connect(self.openWindowsTab)
        self.pushButtonLinux.clicked.connect(self.openLinuxTab)
        self.pushButtonPCBuilder.clicked.connect(self.openPCBuilderTab)
        self.pushButtonComponents.clicked.connect(self.openComponentsTab)
        self.pushButtonDiscussion.clicked.connect(self.openDiscussionTab)

        # connect buttons under components tab to methods
        self.toolButtonCPU.clicked.connect(self.openCPUWindow)
        self.toolButtonMotherboard.clicked.connect(self.openMotherboardWindow)

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

    # this method will create and show the login window, when Login pushButton is clicked
    def openRegistrationWindow(self, checked):
        if self.registrationWindow is None:
            self.registrationWindow = RegistrationWindow()
        self.registrationWindow.show()

    # this method will create and open the login window, when Login pushButton is clicked
    def openLoginWindow(self, checked):
        if self.loginWindow is None:
            self.loginWindow = LoginWindow()
        self.loginWindow.show()

    # this method will create and open the login window, when Login pushButton is clicked
    def openSearchWindow(self, checked):
        if self.searchWindow is None:
            self.searchWindow = ProductSearchWindow()
        self.searchWindow.show()

    # this method will create and open the product details window, when products are double clicked
    def openProductInfoWindow(self, productId):
        self.productInfoWindow = ProductInfo(productId)
        self.productInfoWindow.show()

    # open CPU window and list CPUs
    def openCPUWindow(self):
        self.cpuWindow = CPUWindow()
        self.cpuWindow.show()

    # open Motherboard window and list CPUs
    def openMotherboardWindow(self):
        self.motherboardWindow = MotherboardWindow()
        self.motherboardWindow.show()

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
