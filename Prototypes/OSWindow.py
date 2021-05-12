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
osUI, _ = loadUiType("./ui/os.ui")
productInfoUI, _ = loadUiType("./ui/product-info.ui")


# ProductDetails class will initialize product-details.ui
class OSInfo(QWidget, productInfoUI):
    # initialize the productDetailsUI
    def __init__(self, id):
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
        sql = ''' SELECT product.product_id as id, product_name, version, bit_version, price
                FROM product
                INNER JOIN os ON product.product_id = os.product_id
                WHERE id = ? '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query, (productId,)).fetchone()

        # store product attribute values into variables
        self.productID = product[0]
        self.productName = product[1]
        self.productVersion = product[2]
        self.bitVersion = product[3]
        self.price = product[4]

    def widgets(self):
        self.labelProductName = QLabel()
        self.labelProductName.setText(str(self.productName))

        self.labelProductVersion = QLabel()
        self.labelProductVersion.setText(str(self.productVersion))

        self.labelBitVersion = QLabel()
        self.labelBitVersion.setText(str(self.bitVersion))

        self.labelPrice = QLabel()
        self.labelPrice.setText(str(self.price))

        # add rows and on each row add the labels
        self.formLayoutProductInfo.addRow(
            QLabel("Product Name:"), self.labelProductName)

        self.formLayoutProductInfo.addRow(
            QLabel("Price in USD:"), self.labelPrice)

        self.formLayoutProductInfo.addRow(
            QLabel("Version:"), self.labelProductVersion)

        self.formLayoutProductInfo.addRow(
            QLabel("Bit Version:"), self.labelBitVersion)

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
        pass


# CPUWindow class will initialize the register.ui
class OSWindow(QWidget, osUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.listOSs()
        self.handleClickEvents()

    # handle click events
    def handleClickEvents(self):
        # when one of the psu items is double clicked
        self.tableWidgetOSs.doubleClicked.connect(
            self.selectOS)

     # this method will create and open the product details window, when products are double clicked
    def openOSWindow(self, productId):
        self.osInfoWindow = OSInfo(productId)
        self.osInfoWindow.show()

    # display the list of CPUs
    def listOSs(self):
        # hide the product id column
        self.tableWidgetOSs.setColumnHidden(0, True)
        self.tableWidgetOSs.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetOSs.rowCount())):
            self.tableWidgetOSs.removeRow(i)

        # sql query to retrieve suggested systems from db
        sql = ''' SELECT product.product_id as id, product_name, version, bit_version, price
                FROM product
                INNER JOIN os ON product.product_id = os.product_id '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetCPUs
        for row_data in query:

            row_number = self.tableWidgetOSs.rowCount()
            self.tableWidgetOSs.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set text data to item
                # change the alignment to center
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidgetOSs.setItem(  # set item on tableWidget
                    row_number, column_number, item)

        self.tableWidgetOSs.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # select CPU
    def selectOS(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 4):
            listProduct.append(self.tableWidgetOSs.item(
                self.tableWidgetOSs.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openOSWindow(productId)
