import DeliveryAccount
import csv
import sqlite3
import datetime
from sqlite3 import Error

def menu_nav(selection):
	if(selection == 1):
		view_bids()
	elif(selection == 2):
		ship_items()
	else: print('Try again\n')
	
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
	
def view_bids():

	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT transaction_id, first_name, last_name, address, subtotal, purchase_date FROM user_orders INNER JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE order_status = 0'''
		cur.execute(sql)
		
		rows = cur.fetchall()
		
		for row in rows:
			print('Transaction ID: ', row[0], '\nName: ', row[1], row[2], '\nAddress: ', row[3], '\nSubtotal: ', row[4], '\nPurchase Date: ', row[5], '\n')

		j = input('Bid? (Y):')
		
		if (j == 'Y'):
			bid_amount = int(input('Enter Bid Amount: '))
			
			#add amount to offers
			sql = '''INSERT INTO bid_offers (account_id, transaction_id, bid_amount) VALUES (?,?,?)'''
			params = (2, row[0], bid_amount)
			cur.execute(sql, params)
			
			print('Bid successful.\n')
										 
def ship_items():
	
	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT transaction_id, first_name, last_name, address, subtotal, purchase_date FROM user_orders INNER JOIN personal_acc ON user_orders.account_id = personal_acc.account_id WHERE shipper = "Shippers"'''
		cur.execute(sql)
		
		rows = cur.fetchall()
		
		for row in rows:
			print('Transaction ID: ', row[0], '\nName: ', row[1], row[2], '\nAddress: ', row[3], '\nSubtotal: ', row[4], '\nPurchase Date: ', row[5], '\n')
			
		k = input('Enter tracking number:')
			
		if(k != ''):
			sql = '''UPDATE user_orders SET date_shipped = ?, tracking_no = ?, order_status = 2 WHERE transaction_id = 3'''
			params = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), k)
			cur.execute(sql, params)
			print('Item sent\n')
	
			
i = 0

database = r"store_system.db"
store_db = create_connection(database)

while i > -1:
	print('Main Menu\n')
	print('1. View Bids.\n')
	print('2. Ship Items.')
	i = int(input('Enter a number:'))
	menu_nav(i)