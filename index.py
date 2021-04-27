import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# load the UIs
mainUI, _ = loadUiType("./ui/mainwindow.ui")
loginUI, _ = loadUiType("./ui/login.ui")
registerUI, _ = loadUiType("./ui/register.ui")
searchUI, _ = loadUiType("./ui/product-search.ui")


# SearchWindow class will initialize the register.ui
class SearchWindow(QWidget, searchUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)


# RegistrationWindow class will initialize the register.ui
class RegistrationWindow(QWidget, registerUI):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)


class LoginWindow(QWidget, loginUI):  # LoginWindow class will initialize the login.ui
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)


class MainApp(QMainWindow, mainUI):  # MainApp class will initialize the mainwindow.ui
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.loginWindow = None  # No external login window yet.
        self.registrationWindow = None  # No external registration window yet.
        self.searchWindow = None  # No external search window yet.
        self.handleButtons()

    # handle button clicks
    def handleButtons(self):
        self.pushButtonHome.clicked.connect(self.openHomeTab)
        self.pushButtonMac.clicked.connect(self.openMacTab)
        self.pushButtonWindows.clicked.connect(self.openWindowsTab)
        self.pushButtonLinux.clicked.connect(self.openLinuxTab)
        self.pushButtonPCBuilder.clicked.connect(self.openPCBuilderTab)
        self.pushButtonComponents.clicked.connect(self.openComponentsTab)
        self.pushButtonDiscussion.clicked.connect(self.openDiscussionTab)

        # open login window on button clicked
        self.pushButtonLogin.clicked.connect(self.openLoginWindow)
        # open registration window on button clicked
        self.pushButtonRegister.clicked.connect(self.openRegistrationWindow)
        # open search window on button clicked
        self.pushButtonSearch.clicked.connect(self.openSearchWindow)

    def openHomeTab(self):  # open home tab when Home pushButton is clicked
        self.tabWidget.setCurrentIndex(0)

    def openMacTab(self):  # open mac tab when Mac pushButton is clicked
        self.tabWidget.setCurrentIndex(1)

    def openWindowsTab(self):  # open windows tab when Windows pushButton is clicked
        self.tabWidget.setCurrentIndex(2)

    def openLinuxTab(self):  # open linux tab when Linux pushButton is clicked
        self.tabWidget.setCurrentIndex(3)

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
            self.searchWindow = SearchWindow()
        self.searchWindow.show()


# this main method is not inside the class, it is in the class level
# this method shows the main window
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
