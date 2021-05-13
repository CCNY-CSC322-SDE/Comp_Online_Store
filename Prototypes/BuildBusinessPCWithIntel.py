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

# load pc builder ui
pcBuilderUI, _ = loadUiType("./ui/pc-builder.ui")
productInfoUI, _ = loadUiType("./ui/product-info.ui")


# ProductDetails class will initialize product-details.ui
class ProductInfo(QWidget, productInfoUI):
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
        sql = ''' SELECT product.product_id as id, product_name, purpose, architecture, price, 
                cpu, gpu, ram_size, hdd_size, operating_system, dimensions, weight
                FROM product
                INNER JOIN system ON product.product_id = system.product_id
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
        self.productPrice = product[4]
        self.productCPU = product[5]
        self.productGPU = product[6]
        self.productRAM = product[7]
        self.productHDD = product[8]
        self.productOS = product[9]
        self.productDimensions = product[10]
        self.productWeight = product[11]

    def widgets(self):
        self.labelProductName = QLabel()
        self.labelProductName.setText(str(self.productName))

        self.labelPrice = QLabel()
        self.labelPrice.setText(str(self.productPrice))

        self.labelPurpose = QLabel()
        self.labelPurpose.setText(
            str(self.product_purpose[self.productPurpose]))

        self.labelArchitecture = QLabel()
        self.labelArchitecture.setText(
            str(self.product_architecture[self.productArchitecture]))

        self.labelOS = QLabel()
        self.labelOS.setText(str(self.productOS))

        self.labelCPU = QLabel()
        self.labelCPU.setText(str(self.productCPU))

        self.labelGPU = QLabel()
        self.labelGPU.setText(str(self.productGPU))

        self.labelRAM = QLabel()
        self.labelRAM.setText(str(self.productRAM))

        self.labelHDDSize = QLabel()
        self.labelHDDSize.setText(str(self.productHDD))

        self.labelDimensions = QLabel()
        self.labelDimensions.setText(str(self.productDimensions))

        self.labelWeight = QLabel()
        self.labelWeight.setText(str(self.productWeight))

        # add rows and on each row add the labels
        self.formLayoutProductInfo.addRow(
            QLabel("Name:"), self.labelProductName)

        self.formLayoutProductInfo.addRow(
            QLabel("Price in USD:"), self.labelPrice)

        self.formLayoutProductInfo.addRow(
            QLabel("Main Purpose:"), self.labelPurpose)

        self.formLayoutProductInfo.addRow(
            QLabel("Architecture:"), self.labelArchitecture)

        self.formLayoutProductInfo.addRow(
            QLabel("Operating System:"), self.labelOS)

        self.formLayoutProductInfo.addRow(
            QLabel("CPU:"), self.labelCPU)

        self.formLayoutProductInfo.addRow(
            QLabel("GPU:"), self.labelGPU)

        self.formLayoutProductInfo.addRow(
            QLabel("Memory(RAM):"), self.labelRAM)

        self.formLayoutProductInfo.addRow(
            QLabel("HDD Size:"), self.labelHDDSize)

        self.formLayoutProductInfo.addRow(
            QLabel("Dimensions:"), self.labelDimensions)

        self.formLayoutProductInfo.addRow(
            QLabel("Weight in lbs:"), self.labelWeight)

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


# BusinessPCWindow class will initialize the register.ui
class BuildBusinessPCWithIntel(QWidget, pcBuilderUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        # product purpose and architecture
        self.product_purpose = {0: "Business", 1: "Computing", 2: "Gaming"}
        self.product_architecture = {0: "Intel", 1: "AMD", 2: "ARM"}

        self.UI()
        self.handleClickEvents()

    def UI(self):
        self.selectCPU()
        self.selectMotherboard()
        self.totalPrice()

        # show the CPU tab on form load
        self.tabWidgetSelectedComponents.setCurrentIndex(0)

    # handle click events
    def handleClickEvents(self):
        self.pushButtonAddAllToCart.clicked.connect(self.addAllToCart)

    # select the  CPU
    def selectCPU(self):
        # sql to retrieve details of the product based on product id
        sql = ''' SELECT product.product_id as id, product_name, purpose, architecture, cpu_socket, speed, processor_count, price
                FROM product
                INNER JOIN cpu ON product.product_id = cpu.product_id
                WHERE purpose = 0 AND architecture = 0 AND UPPER(product_name) LIKE 'INTEL%'
                ORDER BY id DESC
                LIMIT 1; '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self. cpuID = product[0]
        self.cpuName = product[1]
        self.cpuPurpose = product[2]
        self.cpuArchitecture = product[3]
        self.cpuSocket = product[4]
        self.cpuSpeed = product[5]
        self.cpuProcessorCount = product[6]
        self.cpuPrice = product[7]

        # create QLabel
        self.labelCPUName = QLabel()
        self.labelCPUName.setText(str(self.cpuName))

        self.labelCPUPurpose = QLabel()
        self.labelCPUPurpose.setText(
            str(self.product_purpose[self.cpuPurpose]))

        self.labelCPUArchitecture = QLabel()
        self.labelCPUArchitecture.setText(
            str(self.product_architecture[self.cpuArchitecture]))

        self.labelCPUSocket = QLabel()
        self.labelCPUSocket.setText(str(self.cpuSocket))

        self.labelCPUSpeed = QLabel()
        self.labelCPUSpeed.setText(str(self.cpuSpeed))

        self.labelCPUProcessorCount = QLabel()
        self.labelCPUProcessorCount.setText(str(self.cpuProcessorCount))

        self.labelCPUPrice = QLabel()
        self.labelCPUPrice.setText(str(self.cpuPrice))

        # add rows and on each row add the labels
        self.formLayoutCPU.addRow(
            QLabel("Product Name:"), self.labelCPUName)

        self.formLayoutCPU.addRow(
            QLabel("Price in USD:"), self.labelCPUPrice)

        self.formLayoutCPU.addRow(
            QLabel("Main Purpose:"), self.labelCPUPurpose)

        self.formLayoutCPU.addRow(
            QLabel("Architecture:"), self.labelCPUArchitecture)

        self.formLayoutCPU.addRow(
            QLabel("CPU Socket:"), self.labelCPUSocket)

        self.formLayoutCPU.addRow(
            QLabel("CPU Speed:"), self.labelCPUSpeed)

        self.formLayoutCPU.addRow(
            QLabel("# of Cores:"), self.labelCPUProcessorCount)

    # select Motherboard
    def selectMotherboard(self):
        # sql to retrieve details of the product based on product id
        sql = ''' SELECT product.product_id as id, product_name, purpose, architecture, cpu_socket, chpiset, ram_slots, ram_capacity, ram_type, price
                FROM product
                INNER JOIN motherboard ON product.product_id = motherboard.product_id
                WHERE purpose = 0 AND architecture = 0 AND UPPER(chpiset) LIKE '%INTEL%'
                ORDER BY id DESC
                LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.motherboardID = product[0]
        self.motherboardName = product[1]
        self.motherboardPurpose = product[2]
        self.motherboardArchitecture = product[3]
        self.motherboardCPUSocket = product[4]
        self.motherboardChipset = product[5]
        self.motherboardRAMSlots = product[6]
        self.motherboardRAMCapacity = product[7]
        self.motherboardRAMType = product[8]
        self.motherboardPrice = product[9]

        self.labelMotherboardName = QLabel()
        self.labelMotherboardName.setText(str(self.motherboardName))

        self.labelMotherboardPurpose = QLabel()
        self.labelMotherboardPurpose.setText(
            str(self.product_purpose[self.motherboardPurpose]))

        self.labelMotherboardArchitecture = QLabel()
        self.labelMotherboardArchitecture.setText(
            str(self.product_architecture[self.motherboardArchitecture]))

        self.labelMotherboardCPUSocket = QLabel()
        self.labelMotherboardCPUSocket.setText(str(self.motherboardCPUSocket))

        self.labelMotherboardChipset = QLabel()
        self.labelMotherboardChipset.setText(str(self.motherboardChipset))

        self.labelMotherboardRAMSlots = QLabel()
        self.labelMotherboardRAMSlots.setText(str(self.motherboardRAMSlots))

        self.labelMotherboardRAMCapacity = QLabel()
        self.labelMotherboardRAMCapacity.setText(
            str(self.motherboardRAMCapacity))

        self.labelMotherboardRAMType = QLabel()
        self.labelMotherboardRAMType.setText(str(self.motherboardRAMType))

        self.labelMotherboardPrice = QLabel()
        self.labelMotherboardPrice.setText(str(self.motherboardPrice))

        # add rows and on each row add the labels
        self.formLayoutMotherboard.addRow(
            QLabel("Product Name:"), self.labelMotherboardName)

        self.formLayoutMotherboard.addRow(
            QLabel("Price in USD:"), self.labelMotherboardPrice)

        self.formLayoutMotherboard.addRow(
            QLabel("Main Purpose:"), self.labelMotherboardPurpose)

        self.formLayoutMotherboard.addRow(
            QLabel("Architecture:"), self.labelMotherboardArchitecture)

        self.formLayoutMotherboard.addRow(
            QLabel("CPU Socket:"), self.labelMotherboardCPUSocket)

        self.formLayoutMotherboard.addRow(
            QLabel("Chipset:"), self.labelMotherboardChipset)

        self.formLayoutMotherboard.addRow(
            QLabel("# of RAM Slots:"), self.labelMotherboardRAMSlots)

        self.formLayoutMotherboard.addRow(
            QLabel("RAM Capacity:"), self.labelMotherboardRAMCapacity)

        self.formLayoutMotherboard.addRow(
            QLabel("RAM Type:"), self.labelMotherboardRAMType)

    # select the Memory
    def selectMemory(self):
        pass

    # select Video Cards
    def selectVideoCards(self):
        pass

    # select the  Case
    def selectCase(self):
        pass

    # select Power Supply
    def selectPowerSupply(self):
        pass

    # select the  Storage
    def selectStorage(self):
        pass

    # select CPU cooler
    def selectCPUCooler(self):
        pass

    # select Operating System
    def selectOperatingSystem(self):
        pass

    # calculate total price
    def totalPrice(self):
        # calculate total price
        self.totalPrice = 0
        self.totalPrice = self.totalPrice + self.cpuPrice + self.motherboardPrice

        self.labelTotalPrice = QLabel()
        self.labelTotalPrice.setText(str(self.totalPrice))

        self.formLayoutTotalPrice.addRow(
            QLabel("Total Price: $"), self.labelTotalPrice)

    # add all the products to the cart
    def addAllToCart(self):
        pass
