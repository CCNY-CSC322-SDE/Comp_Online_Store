import ClerkAccount
import csv
import sqlite3
import datetime
from sqlite3 import Error

def menu_nav(selection):
	if(selection == 1):
		view_offers()
	else: print('Try again\n')
	
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
	
def view_offers():
	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT transaction_id, first_name, last_name, address, subtotal, purchase_date FROM user_orders INNER JOIN personal_acc ON user_order.account_id = personal_acc.account_id WHERE order_status = 0'''
		cur.execute(sql)
		
		rows = cur.fetchall()
		
		for row in rows:
			print('Transaction ID: ', row[0], '\nName: ', row[1], row[2], '\nAddress: ', row[3], '\nSubtotal: ', row[4], '\nPurchase Date: ', row[5], '\n')
			
		j = int(input('Select Transaction Number:'))
		
		if (j == 3):
			transaction_id = 3
			sql = '''SELECT company_name, bid_amount FROM bid_offers INNER JOIN delivery_acc ON bid_offers.account_id = delivery_acc.account_id WHERE transaction_id = 3'''
			cur.execute(sql)
			rows = cur.fetchall()
			
			for row in rows:
				print('Company: ', row[0], '\nBid Amount: ', row[1], '\n')
			
			k = int(input('Select Bid:'))
				
			if(k == 1):
				
				#update transactions
				sql = '''UPDATE order_status SET shipper = ?, order_status = 1 WHERE transaction_id = 3'''
				params = (row[0],)
				cur.execute(sql, params)
				
				#delete bids for transaction id
				sql = '''DELETE FROM bid_offers WHERE transaction_id = 3'''
				cur.execute(sql)
				
				print('Offer sent to delivery company\n')

i = 0

database = r"store_system.db"
store_db = create_connection(database)

while i > -1:
	print('Main Menu\n')
	print('1. View Bid Offers.')
	i = int(input('Enter a number:'))
	menu_nav(i)