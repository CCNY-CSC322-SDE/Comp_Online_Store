import sqlite3
from sqlite3 import Error

from Models.Accounts import PersonalAccount
from Models.Accounts import Account

database = r"./Database/store_system.db"
store_db = None


def initialize():
    global store_db
    store_db = create_connection(database)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def updateAccountStatus(account_id):
    if store_db == None:
        initialize()
    account = getAccount(account_id)
    with store_db:
        cur = store_db.cursor()
        sql = '''UPDATE account SET acc_status=? WHERE account_id = ?'''
        cur.execute(sql, (account.acc_status + 1, account_id))


def addWarningCount(account_id):
    if store_db == None:
        initialize()
    account = getAccount(account_id)
    with store_db:
        cur = store_db.cursor()
        sql = '''UPDATE account SET warnings=? WHERE account_id = ?'''
        cur.execute(sql, (account.acc_status + 1, account_id))


def suspendAccount(account_id):
    if store_db == None:
        initialize()
    account = getAccount(account_id)
    with store_db:
        cur = store_db.cursor()
        sql = '''INSERT INTO avoid_list(banned_emails,send_notif) VALUES(?,?)'''
        cur.execute(sql, (account.warnings + 1))


def getPersonalAccount(account_id):
    if store_db == None:
        initialize()
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM personal_acc WHERE account_id = ?'''
        cur.execute(sql, (account_id,))

        row = cur.fetchone()
        return PersonalAccount(*row)
    return None


def getAccount(account_id):
    if store_db == None:
        initialize()
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM account WHERE account_id = ?'''
        cur.execute(sql, (account_id,))

        row = cur.fetchone()
        return Account(*row)
    return None
