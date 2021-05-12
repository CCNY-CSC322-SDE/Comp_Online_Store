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
storageUI, _ = loadUiType("./ui/storage.ui")
productInfoUI, _ = loadUiType("./ui/product-info.ui")


# ProductDetails class will initialize product-details.ui
class StorageInfo(QWidget, productInfoUI):
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
        sql = ''' SELECT product.product_id as id, product_name, dimensions, weight, type, capacity, rotation_speed, price
                FROM product
                INNER JOIN storage ON product.product_id = storage.product_id
                WHERE id = ? '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query, (productId,)).fetchone()

        # store product attribute values into variables
        self.productID = product[0]
        self.productName = product[1]
        self.productDimensions = product[2]
        self.productWeight = product[3]
        self.type = product[4]
        self.capacity = product[5]
        self.rotationSpeed = product[6]
        self.price = product[7]

    def widgets(self):
        self.labelProductName = QLabel()
        self.labelProductName.setText(str(self.productName))

        self.labelDimensions = QLabel()
        self.labelDimensions.setText(str(self.productDimensions))

        self.labelWeight = QLabel()
        self.labelWeight.setText(str(self.productWeight))

        self.labelType = QLabel()
        self.labelType.setText(str(self.type))

        self.labelCapacity = QLabel()
        self.labelCapacity.setText(str(self.capacity))

        self.labelRotationSpeed = QLabel()
        self.labelRotationSpeed.setText(str(self.rotationSpeed))

        self.labelPrice = QLabel()
        self.labelPrice.setText(str(self.price))

        # add rows and on each row add the labels
        self.formLayoutProductInfo.addRow(
            QLabel("Product Name:"), self.labelProductName)

        self.formLayoutProductInfo.addRow(
            QLabel("Price in USD:"), self.labelPrice)

        self.formLayoutProductInfo.addRow(
            QLabel("Type:"), self.labelType)

        self.formLayoutProductInfo.addRow(
            QLabel("Capacity:"), self.labelCapacity)

        self.formLayoutProductInfo.addRow(
            QLabel("Rotation Speed:"), self.labelRotationSpeed)

        self.formLayoutProductInfo.addRow(
            QLabel("Dimensions:"), self.labelDimensions)

        self.formLayoutProductInfo.addRow(
            QLabel("Weight:"), self.labelWeight)

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
class StorageWindow(QWidget, storageUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.listStorages()
        self.handleClickEvents()

    # handle click events
    def handleClickEvents(self):
        # when one of the psu items is double clicked
        self.tableWidgetStorages.doubleClicked.connect(
            self.selectStorage)

     # this method will create and open the product details window, when products are double clicked
    def openStorageWindow(self, productId):
        self.storageInfoWindow = StorageInfo(productId)
        self.storageInfoWindow.show()

    # display the list of CPUs
    def listStorages(self):
        # hide the product id column
        self.tableWidgetStorages.setColumnHidden(0, True)
        self.tableWidgetStorages.setFont(QFont("Times", 12))

        # if already exist, reset table data
        for i in reversed(range(self.tableWidgetStorages.rowCount())):
            self.tableWidgetStorages.removeRow(i)

        # sql query to retrieve suggested systems from db
        sql = ''' SELECT product.product_id as id, product_name, type, capacity, rotation_speed, price
                FROM product
                INNER JOIN storage ON product.product_id = storage.product_id '''

        # execute query
        query = cur.execute(sql)
        # populate tableWidgetCPUs
        for row_data in query:

            row_number = self.tableWidgetStorages.rowCount()
            self.tableWidgetStorages.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem()  # create the item
                item.setText(str(data))  # set text data to item
                # change the alignment to center
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidgetStorages.setItem(  # set item on tableWidget
                    row_number, column_number, item)

        self.tableWidgetStorages.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    # select CPU
    def selectStorage(self):
        # declare variables
        productId = 0
        listProduct = []

        # store all attribute values of a product into listProduct
        for i in range(0, 4):
            listProduct.append(self.tableWidgetStorages.item(
                self.tableWidgetStorages.currentRow(), i).text())
        # get the product id
        productId = listProduct[0]
        self.openStorageWindow(productId)