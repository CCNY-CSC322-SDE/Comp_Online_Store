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
        self.selectMemory()
        self.selectVideoCards()
        self.selectCase()
        self.selectPowerSupply()
        self.selectStorage()
        self.selectCPUCooler()
        self.selectOperatingSystem()

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
                LIMIT 1 '''

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
        # sql to retrieve details of the product based on product id
        sql = ''' SELECT product.product_id as id, product_name, capacity, memory_speed, ram_type, price
                FROM product
                INNER JOIN ram ON product.product_id = ram.product_id
                ORDER BY id DESC
                LIMIT 1; '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.ramID = product[0]
        self.ramName = product[1]
        self.ramCapacity = product[2]
        self.ramMemorySpeed = product[3]
        self.ramType = product[4]
        self.ramPrice = product[5]

        self.labelRAMName = QLabel()
        self.labelRAMName.setText(str(self.ramName))

        self.labelRAMCapacity = QLabel()
        self.labelRAMCapacity.setText(str(self.ramCapacity))

        self.labelRAMMemorySpeed = QLabel()
        self.labelRAMMemorySpeed.setText(str(self.ramMemorySpeed))

        self.labelRAMType = QLabel()
        self.labelRAMType.setText(str(self.ramType))

        self.labelRAMPrice = QLabel()
        self.labelRAMPrice.setText(str(self.ramPrice))

        # add rows and on each row add the labels
        self.formLayoutMemory.addRow(
            QLabel("Product Name:"), self.labelRAMName)

        self.formLayoutMemory.addRow(
            QLabel("Price in USD:"), self.labelRAMPrice)

        self.formLayoutMemory.addRow(
            QLabel("Capacity:"), self.labelRAMCapacity)

        self.formLayoutMemory.addRow(
            QLabel("Memory Speed:"), self.labelRAMMemorySpeed)

        self.formLayoutMemory.addRow(
            QLabel("RAM Type:"), self.labelRAMType)

    # select Video Cards
    def selectVideoCards(self):
        # sql to retrieve details of the product based on product id
        sql = '''  SELECT product.product_id as id, product_name, memory_size, memory_speed, price
                FROM product
                INNER JOIN gpu ON product.product_id = gpu.product_id
                ORDER BY id DESC
                LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.gpuID = product[0]
        self.gpuName = product[1]
        self.gpuMemorySize = product[2]
        self.gpuMemorySpeed = product[3]
        self.gpuPrice = product[4]

        self.labelGPUName = QLabel()
        self.labelGPUName.setText(str(self.gpuName))

        self.labelGPUMemorySize = QLabel()
        self.labelGPUMemorySize.setText(str(self.gpuMemorySize))

        self.labelGPUMemorySpeed = QLabel()
        self.labelGPUMemorySpeed.setText(str(self.gpuMemorySpeed))

        self.labelGPUPrice = QLabel()
        self.labelGPUPrice.setText(str(self.gpuPrice))

        # add rows and on each row add the labels
        self.formLayoutVideoCards.addRow(
            QLabel("Product Name:"), self.labelGPUName)

        self.formLayoutVideoCards.addRow(
            QLabel("Price in USD:"), self.labelGPUPrice)

        self.formLayoutVideoCards.addRow(
            QLabel("Memory Size:"), self.labelGPUMemorySize)

        self.formLayoutVideoCards.addRow(
            QLabel("Memory Speed:"), self.labelGPUMemorySpeed)

    # select the  Case
    def selectCase(self):
        # sql to retrieve details of the product based on product id
        sql = '''  SELECT product.product_id as id, product_name, dimensions, weight, motherboard_support, io_ports, fan_support, hdd_support, psu_support,  price
                FROM product
                INNER JOIN pc_case ON product.product_id = pc_case.product_id
                ORDER BY id DESC
                LIMIT 1; '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.caseID = product[0]
        self.caseName = product[1]
        self.caseDimensions = product[2]
        self.caseWeight = product[3]
        self.caseMotherboardSupport = product[4]
        self.caseIOPorts = product[5]
        self.caseFanSupport = product[6]
        self.caseHDDSupport = product[7]
        self.casePSUSupport = product[8]
        self.casePrice = product[9]

        self.labelCaseName = QLabel()
        self.labelCaseName.setText(str(self.caseName))

        self.labelCasePrice = QLabel()
        self.labelCasePrice.setText(str(self.casePrice))

        self.labelCaseDimensions = QLabel()
        self.labelCaseDimensions.setText(str(self.caseDimensions))

        self.labelCaseWeight = QLabel()
        self.labelCaseWeight.setText(str(self.caseWeight))

        self.labelCaseMotherboardSupport = QLabel()
        self.labelCaseMotherboardSupport.setText(
            str(self.caseMotherboardSupport))

        self.labelCaseIOPorts = QLabel()
        self.labelCaseIOPorts.setText(str(self.caseIOPorts))

        self.labelCaseFanSupport = QLabel()
        self.labelCaseFanSupport.setText(str(self.caseFanSupport))

        self.labelCaseHDDSupport = QLabel()
        self.labelCaseHDDSupport.setText(str(self.caseHDDSupport))

        self.labelCasePSUSupport = QLabel()
        self.labelCasePSUSupport.setText(str(self.casePSUSupport))

        # add rows and on each row add the labels
        self.formLayoutCase.addRow(
            QLabel("Product Name:"), self.labelCaseName)

        self.formLayoutCase.addRow(
            QLabel("Price in USD:"), self.labelCasePrice)

        self.formLayoutCase.addRow(
            QLabel("Motherboard Support:"), self.labelCaseMotherboardSupport)

        self.formLayoutCase.addRow(
            QLabel("IO Ports:"), self.labelCaseIOPorts)

        self.formLayoutCase.addRow(
            QLabel("Fan Support:"), self.labelCaseFanSupport)

        self.formLayoutCase.addRow(
            QLabel("HDD Support:"), self.labelCaseHDDSupport)

        self.formLayoutCase.addRow(
            QLabel("PSU Support:"), self.labelCasePSUSupport)

        self.formLayoutCase.addRow(
            QLabel("Dimensions:"), self.labelCaseDimensions)

        self.formLayoutCase.addRow(
            QLabel("Weight:"), self.labelCaseWeight)

    # select Power Supply
    def selectPowerSupply(self):
        # sql to retrieve details of the product based on product id
        sql = '''  SELECT product.product_id as id, product_name,dimensions, weight, power, psu_type,  price
                    FROM product
                    INNER JOIN psu ON product.product_id = psu.product_id
                    ORDER BY id DESC
                    LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.psuID = product[0]
        self.psuName = product[1]
        self.psuDimensions = product[2]
        self.psuWeight = product[3]
        self.psuPower = product[4]
        self.psuType = product[5]
        self.psuPrice = product[6]

        self.labelPSUName = QLabel()
        self.labelPSUName.setText(str(self.psuName))

        self.labelPSUDimensions = QLabel()
        self.labelPSUDimensions.setText(str(self.psuDimensions))

        self.labelPSUWeight = QLabel()
        self.labelPSUWeight.setText(str(self.psuWeight))

        self.labelPSUPower = QLabel()
        self.labelPSUPower.setText(str(self.psuPower))

        self.labelPSUType = QLabel()
        self.labelPSUType.setText(str(self.psuType))

        self.labelPSUPrice = QLabel()
        self.labelPSUPrice.setText(str(self.psuPrice))

        # add rows and on each row add the labels
        self.formLayoutPowerSupply.addRow(
            QLabel("Product Name:"), self.labelPSUName)

        self.formLayoutPowerSupply.addRow(
            QLabel("Price in USD:"), self.labelPSUPrice)

        self.formLayoutPowerSupply.addRow(
            QLabel("Maximum Power:"), self.labelPSUPower)

        self.formLayoutPowerSupply.addRow(
            QLabel("Type:"), self.labelPSUType)

        self.formLayoutPowerSupply.addRow(
            QLabel("Dimensions:"), self.labelPSUDimensions)

        self.formLayoutPowerSupply.addRow(
            QLabel("Weight:"), self.labelPSUWeight)

    # select the  Storage
    def selectStorage(self):
        # sql to retrieve details of the product based on product id
        sql = '''  SELECT product.product_id as id, product_name, dimensions, weight, type, capacity, rotation_speed, price
                FROM product
                INNER JOIN storage ON product.product_id = storage.product_id
                ORDER BY id DESC
                LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.storageID = product[0]
        self.storageName = product[1]
        self.storageDimensions = product[2]
        self.storageWeight = product[3]
        self.storageType = product[4]
        self.storageCapacity = product[5]
        self.storageRotationSpeed = product[6]
        self.storagePrice = product[7]

        self.labelStorageName = QLabel()
        self.labelStorageName.setText(str(self.storageName))

        self.labelStorageDimensions = QLabel()
        self.labelStorageDimensions.setText(str(self.storageDimensions))

        self.labelStorageWeight = QLabel()
        self.labelStorageWeight.setText(str(self.storageWeight))

        self.labelStorageType = QLabel()
        self.labelStorageType.setText(str(self.storageType))

        self.labelStorageCapacity = QLabel()
        self.labelStorageCapacity.setText(str(self.storageCapacity))

        self.labelStorageRotationSpeed = QLabel()
        self.labelStorageRotationSpeed.setText(str(self.storageRotationSpeed))

        self.labelStoragePrice = QLabel()
        self.labelStoragePrice.setText(str(self.storagePrice))

        # add rows and on each row add the labels
        self.formLayoutStorage.addRow(
            QLabel("Product Name:"), self.labelStorageName)

        self.formLayoutStorage.addRow(
            QLabel("Price in USD:"), self.labelStoragePrice)

        self.formLayoutStorage.addRow(
            QLabel("Type:"), self.labelStorageType)

        self.formLayoutStorage.addRow(
            QLabel("Capacity:"), self.labelStorageCapacity)

        self.formLayoutStorage.addRow(
            QLabel("Rotation Speed:"), self.labelStorageRotationSpeed)

        self.formLayoutStorage.addRow(
            QLabel("Dimensions:"), self.labelStorageDimensions)

        self.formLayoutStorage.addRow(
            QLabel("Weight:"), self.labelStorageWeight)

    # select CPU cooler
    def selectCPUCooler(self):
        # sql to retrieve details of the product based on product id
        sql = '''   SELECT product.product_id as id, product_name, cpu_socket,heatsink_dimensions, fan_dimensions, rotation_speed, power, price
                FROM product
                INNER JOIN pc_cooler ON product.product_id = pc_cooler.product_id
                ORDER BY id DESC
                LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.coolerID = product[0]
        self.coolerName = product[1]
        self.coolerCPUSocket = product[2]
        self.coolerHeatsinkDimensions = product[3]
        self.coolerFanDimensions = product[4]
        self.coolerRotationSpeed = product[5]
        self.coolerPower = product[6]
        self.coolerPrice = product[7]

        self.labelCoolerName = QLabel()
        self.labelCoolerName.setText(str(self.coolerName))

        self.labelCoolerCPUSocket = QLabel()
        self.labelCPUSocket.setText(str(self.coolerCPUSocket))

        self.labelCoolerHeatsinkDimensions = QLabel()
        self.labelCoolerHeatsinkDimensions.setText(
            str(self.coolerHeatsinkDimensions))

        self.labelCoolerFanDimensions = QLabel()
        self.labelCoolerFanDimensions.setText(str(self.coolerFanDimensions))

        self.labelCoolerRotationSpeed = QLabel()
        self.labelCoolerRotationSpeed.setText(str(self.coolerRotationSpeed))

        self.labelCoolerPower = QLabel()
        self.labelCoolerPower.setText(str(self.coolerPower))

        self.labelCoolerPrice = QLabel()
        self.labelCoolerPrice.setText(str(self.coolerPrice))

        # add rows and on each row add the labels
        self.formLayoutCPUCooler.addRow(
            QLabel("Product Name:"), self.labelCoolerName)

        self.formLayoutCPUCooler.addRow(
            QLabel("Price in USD:"), self.labelCoolerPrice)

        self.formLayoutCPUCooler.addRow(
            QLabel("CPU Socket:"), self.labelCoolerCPUSocket)

        self.formLayoutCPUCooler.addRow(
            QLabel("Rotation Speed:"), self.labelCoolerRotationSpeed)

        self.formLayoutCPUCooler.addRow(
            QLabel("Max Power:"), self.labelCoolerPower)

        self.formLayoutCPUCooler.addRow(
            QLabel("Heatsink Dimensions:"), self.labelCoolerHeatsinkDimensions)

        self.formLayoutCPUCooler.addRow(
            QLabel("Fan Dimensions:"), self.labelCoolerFanDimensions)

    # select Operating System
    def selectOperatingSystem(self):
        # sql to retrieve details of the product based on product id
        sql = ''' SELECT product.product_id as id, product_name, version, bit_version, price
                FROM product
                INNER JOIN os ON product.product_id = os.product_id		
			    ORDER BY id DESC
                LIMIT 1 '''

        # form the sql query
        query = (sql)
        # single item tuple=(1,)
        # retrieve the product from the database
        product = cur.execute(query,).fetchone()

        # store product attribute values into variables
        self.osID = product[0]
        self.osName = product[1]
        self.osVersion = product[2]
        self.OSBitVersion = product[3]
        self.OSPrice = product[4]

        self.labelOSName = QLabel()
        self.labelOSName.setText(str(self.osName))

        self.labelOSVersion = QLabel()
        self.labelOSVersion.setText(str(self.osVersion))

        self.labelOSBitVersion = QLabel()
        self.labelOSBitVersion.setText(str(self.OSBitVersion))

        self.labelOSPrice = QLabel()
        self.labelOSPrice.setText(str(self.OSPrice))

        # add rows and on each row add the labels
        self.formLayoutOperatingSystem.addRow(
            QLabel("Product Name:"), self.labelOSName)

        self.formLayoutOperatingSystem.addRow(
            QLabel("Price in USD:"), self.labelOSPrice)

        self.formLayoutOperatingSystem.addRow(
            QLabel("Version:"), self.labelOSVersion)

        self.formLayoutOperatingSystem.addRow(
            QLabel("Bit Version:"), self.labelOSBitVersion)

    # calculate total price
    def totalPrice(self):
        # calculate total price
        self.totalPrice = 0
        self.totalPrice = self.totalPrice + self.cpuPrice + \
            self.motherboardPrice + self.ramPrice + \
            self.gpuPrice + self.casePrice + self.psuPrice + \
            self.storagePrice + self.coolerPrice + self.OSPrice

        self.labelTotalPrice = QLabel()
        self.labelTotalPrice.setText(str(self.totalPrice))

        self.formLayoutTotalPrice.addRow(
            QLabel("Total Price: $"), self.labelTotalPrice)

    # add all the products to the cart
    def addAllToCart(self):
        pass
