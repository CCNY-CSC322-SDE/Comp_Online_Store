import sqlite3
from sqlite3 import Error
from Models.Products import Product
from Models.Products import System

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

def getProducts():
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM product'''
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            results.append(Product(*row))
    return results

def searchProducts(product_name):
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM product WHERE product_name LIKE  %?%'''
        cur.execute(sql,(product_name,))
        rows = cur.fetchall()
        for row in rows:
            results.append(Product(*row))
    return results

def getAllSystems():
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM system'''
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            results.append(System(*row))
    return results