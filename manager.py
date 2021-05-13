import sys
import sqlite3

from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sqlite3 import Error

managerUI, _ = loadUiType("./ui/manager.ui")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

database = r"./Database/store_system.db"
store_db = create_connection(database)

class ManagerApp(QMainWindow, managerUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.cur = store_db.cursor()
        self.acc_edit.setVisible(False)
        self.add_acc.clicked.connect(self.acc_edit.show)
        self.add_acc.clicked.connect(self.acc_edit.hide)
        self.back.clicked.connect(self.acc_info.show)
        #self.radioButton_1.clicked.connect(self.choose_user())
        #self.radioButton_2.clicked.connect(self.choose_clerk())
        #self.pushButton_3.clicked.connect(self.choose_delivery())
        self.lineEdit_username.text()
        self.view_users.clicked.connect(self.viewUsers)
        self.view_clerks.clicked.connect(self.viewClerks)
        self.view_avoid.clicked.connect(self.viewAvoid)
        self.view_compl.clicked.connect(self.viewComplaints)
        self.edit_acc.clicked.connect(self.acc_edit.show)

    def viewUsers(self):
        sql = '''SELECT * FROM personal_acc'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.model = QtSql.QSqlTableModel()
        row = len(rows)
        model = QtGui.QStandardItemModel(row, len(rows[0]))
        col = len(rows[0])
        for i in range(row):
            for j in range(col):
                if j == 1 or j == 2 or j == 4:
                    model.setItem(i, j, QtGui.QStandardItem(rows[i][j]))
                elif j == 0 or j == 3 or j == 5:
                    if rows[i][j] == None:
                        model.setItem(i, j, QtGui.QStandardItem(str(0)))
                    else:
                        model.setItem(i, j, QtGui.QStandardItem(str(rows[i][j])))
        model.setHorizontalHeaderLabels(['Account_id', 'First Name', 'Last Name', 'Address', 'Balance', 'Credit Card'])
        self.tableView.setModel(model)

    def viewClerks(self):
        sql = '''SELECT * FROM clerk_acc'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.model = QtSql.QSqlTableModel()
        row = len(rows)
        if row == 0:
            self.showMessage("Error: No records.")
        else:
            model = QtGui.QStandardItemModel(row, len(rows[0]))
            col = len(rows[0])
            for i in range(row):
                for j in range(col):
                    if j == 1 or j == 2 or j == 4:
                        model.setItem(i, j, QtGui.QStandardItem(rows[i][j]))
                    elif j == 0 or j == 3 or j == 5:
                        if rows[i][j] == None:
                            model.setItem(i, j, QtGui.QStandardItem(str(0)))
                        else:
                            model.setItem(i, j, QtGui.QStandardItem(str(rows[i][j])))

            model.setHorizontalHeaderLabels(
                ['Account_id', 'First Name', 'Last Name', 'Notification Sent'])
            self.tableView.setModel(model)

    def viewAvoid(self):
        sql = '''SELECT * FROM avoid_list'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.model = QtSql.QSqlTableModel()
        row = len(rows)
        if row == 0:
            self.showMessage("Error: No records.")
        else:
            model = QtGui.QStandardItemModel(row, len(rows[0]))
            col = len(rows[0])
            for i in range(row):
                for j in range(col):
                    if j == 1 or j == 2 or j == 4:
                        model.setItem(i, j, QtGui.QStandardItem(rows[i][j]))
                    elif j == 0 or j == 3 or j == 5:
                        if rows[i][j] == None:
                            model.setItem(i, j, QtGui.QStandardItem(str(0)))
                        else:
                            model.setItem(i, j, QtGui.QStandardItem(str(rows[i][j])))

            model.setHorizontalHeaderLabels(
                ['Emails', 'Banned Permanently', 'Notification Sent'])
            self.tableView.setModel(model)

    def viewComplaints(self):
        sql = '''SELECT * FROM complaint'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.model = QtSql.QSqlTableModel()
        row = len(rows)
        if row == 0:
            self.showMessage("Error: No records.")
        else:
            model = QtGui.QStandardItemModel(row, len(rows[0]))
            col = len(rows[0])
            for i in range(row):
                for j in range(col):
                    if j == 1 or j == 2 or j == 4:
                        model.setItem(i, j, QtGui.QStandardItem(rows[i][j]))
                    elif j == 0 or j == 3 or j == 5:
                        if rows[i][j] == None:
                            model.setItem(i, j, QtGui.QStandardItem(str(0)))
                        else:
                            model.setItem(i, j, QtGui.QStandardItem(str(rows[i][j])))

            model.setHorizontalHeaderLabels(
                ['Comlaint No.', 'Complainant Id', 'Offender_id','Filed_on','Claim'])
            self.tableView.setModel(model)

    # Display error messages
    def showMessage(self, msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

def main():
    app = QApplication(sys.argv)
    window = ManagerApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
