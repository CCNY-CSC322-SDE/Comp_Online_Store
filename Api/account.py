import sqlite3
from sqlite3 import Error

from Models.Accounts import PersonalAccount
database = r"store_system.db"
store_db = None


def initialize():
    store_db = create_connection(database)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
# Todo: Finish account api
def updateAccountStatus(account_id):
    yield

def suspendAccount(account_id):
    yield

def getPersonalAccount(account_id):
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM personal_acc WHERE account_id = ?'''
        cur.execute(sql,(account_id))

        rows = cur.fetchall()
        for row in rows:
            results.append(PersonalAccount(*row))
    return results