import sys
import os
import PyQt5
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# database connection
con = sqlite3.connect("./Database/store_system.db")
cur = con.cursor()

# load registration window ui
motherboardUI, _ = loadUiType("./ui/motherboard.ui")
productInfoUI, _ = loadUiType("./ui/product-info.ui")
bidUI, _ = loadUiType("./ui/bid-dialog.ui")

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

class BiddingDialog (QDialog, bidUI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)     

# ProductDetails class will initialize product-details.ui
class MotherboardInfo(QWidget, productInfoUI):
    # initialize the productDetailsUI
    def __init__(self, id, user):
        QWidget.__init__(self)
        self.setupUi(self)

        # set window icon and position
        self.setWindowTitle("Product Info and Discussion")
        self.setGeometry(450, 0, 661, 700)
        self.setFixedSize(self.size())

        # product purpose and architecture
        self.product_purpose = {0: "Business", 1: "Computing", 2: "Gaming"}
        self.product_architecture = {0: "Intel", 1: "AMD", 2: "ARM"}

        # variable to hold the id of the product
        self.productId = id
        self.user = user

        self.productUI()

    def productUI(self):
        self.handleButtonClicks()
        self.productDetails(self.productId)
        self.widgets()
        self.getProductRatings()

    # handle button click events
    def handleButtonClicks(self):
        self.pushButtonAddToCart.clicked.connect(self.addProductToCart)

    # retrieve product details from the database
    def productDetails(self, productId):
        # sql to retrieve details of the product based on product id
        sql = ''' SELECT product .product_id as id, product_name,purpose, architecture, cpu_socket, chpiset, ram_slots, ram_capacity, ram_type, price
                FROM product
                INNER JOIN motherboard ON product.product_id = motherboard.product_id
                WHERE id=? '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query, (productId,)).fetchone()

        # store product attribute values into variables
        self.productID = product[0]
        self.productName = product[1]
        self.productPurpose = product[2]
        self.productArchitecture = product[3]
        self.cpuSocket = product[4]
        self.chipset = product[5]
        self.ramSlots = product[6]
        self.ramCapacity = product[7]
        self.ramType = product[8]
        self.price = product[9]

    def widgets(self):
        self.labelProductName = QLabel()
        self.labelProductName.setText(str(self.productName))

        self.labelPurpose = QLabel()
        self.labelPurpose.setText(
            str(self.product_purpose[self.productPurpose]))

        self.labelArchitecture = QLabel()
        self.labelArchitecture.setText(
            str(self.product_architecture[self.productArchitecture]))

        self.labelCPUSocket = QLabel()
        self.labelCPUSocket.setText(str(self.cpuSocket))

        self.labelChipset = QLabel()
        self.labelChipset.setText(str(self.chipset))

        self.labelRAMSlots = QLabel()
        self.labelRAMSlots.setText(str(self.ramSlots))

        self.labelRAMCapacity = QLabel()
        self.labelRAMCapacity.setText(str(self.ramCapacity))

        self.labelRAMType = QLabel()
        self.labelRAMType.setText(str(self.ramType))

        self.labelPrice = QLabel()
        self.labelPrice.setText(str(self.price))

        # add rows and on each row add the labels
        self.formLayoutProductInfo.addRow(
            QLabel("Product Name:"), self.labelProductName)

        self.formLayoutProductInfo.addRow(
            QLabel("Price in USD:"), self.labelPrice)

        self.formLayoutProductInfo.addRow(
            QLabel("Main Purpose:"), self.labelPurpose)

        self.formLayoutProductInfo.addRow(
            QLabel("Architecture:"), self.labelArchitecture)

        self.formLayoutProductInfo.addRow(
            QLabel("CPU Socket:"), self.labelCPUSocket)

        self.formLayoutProductInfo.addRow(
            QLabel("Chipset:"), self.labelChipset)

        self.formLayoutProductInfo.addRow(
            QLabel("# of RAM Slots:"), self.labelRAMSlots)

        self.formLayoutProductInfo.addRow(
            QLabel("RAM Capacity:"), self.labelRAMCapacity)

        self.formLayoutProductInfo.addRow(
            QLabel("RAM Type:"), self.labelRAMType)

    # count the number of each vote_score of a product
    def getProductRatings(self):
        # contains score of the product
        product_scores = {}
        # sql query string to retrieve product rating
        sql = ''' SELECT  COUNT(vote_score)  FROM purchased_items 
            WHERE  item_name=? AND vote_score=? '''

        sqlAvgScore = ''' SELECT AVG(vote_score) FROM purchased_items WHERE item_name=?'''

        # create the sql query
        query = (sql)
        queryAvgScore = (sqlAvgScore)

        # count the number of each score, how many times each score occur
        for score in range(1, 6):
            product_score = cur.execute(
                query, (self.productName, score,)).fetchone()
            # store the score and each occurrence in the dictionary
            product_scores[score] = product_score[0]

        # count the average score
        avg_score = cur.execute(queryAvgScore, (self.productName,)).fetchone()

        self.labelFiveStar = QLabel()
        self.labelFiveStar.setText("(" + str(product_scores[5]) + ")")

        self.labelFourStar = QLabel()
        self.labelFourStar.setText("(" + str(product_scores[4]) + ")")

        self.labelThreeStar = QLabel()
        self.labelThreeStar.setText("(" + str(product_scores[3]) + ")")

        self.labelTwoStar = QLabel()
        self.labelTwoStar.setText("(" + str(product_scores[2]) + ")")

        self.labelOneStar = QLabel()
        self.labelOneStar.setText("(" + str(product_scores[1]) + ")")

        self.labelAverageScore = QLabel()
        self.labelAverageScore.setText("(" + str(avg_score[0]) + ")")

        # add rows in the verticalLayoutRatings layout
        self.formLayoutRatings.addRow(
            QLabel("5 stars:"), self.labelFiveStar)
        self.formLayoutRatings.addRow(
            QLabel("4 stars:"), self.labelFourStar)
        self.formLayoutRatings.addRow(
            QLabel("3 stars:"), self.labelThreeStar)
        self.formLayoutRatings.addRow(
            QLabel("2 stars:"), self.labelTwoStar)
        self.formLayoutRatings.addRow(
            QLabel("1 star:"), self.labelOneStar)
        self.formLayoutRatings.addRow(
            QLabel("Avg Ratings:"), self.labelAverageScore)

    # this method will add the selected product to the cart
    def addProductToCart(self):
        msg = QMessageBox()
        if(self.user[0] is not None):
            sql = '''SELECT COUNT(*) FROM cart WHERE account_id = ? AND product_id = ?'''
            params = (self.user[0], self.productId)
            cur.execute(sql, params)
            in_cart = cur.fetchone()[0]
            
            msg = QMessageBox()
            dia = BiddingDialog()
            dia.label.setWindowTitle("Add to cart")
            dia.label.setText("Enter product quantity")
            dia.lineEdit.setFocus()
            
            entry = dia.exec_()
            if (entry == QDialog.Accepted):
                string = dia.lineEdit.text()
                if(string.isnumeric()):
                    if(int(in_cart) == 1):
                        sql = '''UPDATE cart SET amount = amount + ? WHERE account_id = ? AND product_id = ?'''
                        params = (int(string), self.user[0], self.productId)
                        cur.execute(sql, params)
                    else:
                        sql = '''INSERT INTO cart VALUES (?, ?, ?)'''
                        params = (self.user[0], self.productId, int(string))
                        cur.execute(sql, params)
                        
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Item added to cart.")
                    msg.setWindowTitle("Confirmation")
                    msg.exec_()
                    con.commit()
                    self.close()
                else:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Please enter a valid number.")
                    msg.setWindowTitle("Error")
                    msg.exec_()
            else:
                return 
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please Log In.")
            msg.setWindowTitle("Error")
            msg.exec_()            

# CPUWindow class will initialize the register.ui
class MotherboardWindow(QWidget, motherboardUI):
    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)

        self.listMotherboards()
        self.handleClickEvents()
        self.user = user
       
        
    # handle click events
    def handleClickEvents(self):
        # when one of the cpu items is double clicked
        self.tableWidgetMotherboards.doubleClicked.connect(
            self.selectMotherboard)

     # this method will create and open the product details window, when products are double clicked
    def openMotherboardInfoWindow(self, productId):
        self.motherboardInfoWindow = MotherboardInfo(productId, self.user)
        self.motherboardInfoWindow.show()

    # display the list of CPUs
    def listMotherboards(self):
        # hide the product id column
        self.tableWidgetMotherboards.setColumnHidden(0, True)
        self.tableWidgetMotherboards.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetMotherboards.rowCount())):
            self.tableWidgetMotherboards.removeRow(i)

        # sql query to retrieve suggested systems from db
        sql = ''' SELECT product .product_id as id, product_name, cpu_socket, chpiset, ram_slots, ram_capacity, ram_type, price
                FROM product
                INNER JOIN motherboard ON product.product_id = motherboard.product_id '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetCPUs
        for row_data in query:

            row_number = self.tableWidgetMotherboards.rowCount()
            self.tableWidgetMotherboards.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set text data to item
                # change the alignment to center
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidgetMotherboards.setItem(  # set item on tableWidget
                    row_number, column_number, item)

        self.tableWidgetMotherboards.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # select CPU
    def selectMotherboard(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 6):
            listProduct.append(self.tableWidgetMotherboards.item(
                self.tableWidgetMotherboards.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openMotherboardInfoWindow(productId)
