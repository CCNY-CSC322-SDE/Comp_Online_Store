import RegisteredAccount
import csv
import sqlite3
import datetime
from sqlite3 import Error

def menu_nav(selection):
	if(selection == 1):
		view_cart()
	elif(selection == 2):
		view_history()
	elif(selection == 3):
		view_information()
	else: print('Try again\n')
	
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
	
def view_cart():
	subtotal = 0
	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT product_name, price, amount FROM cart INNER JOIN product ON cart.product_id = product.product_id WHERE account_id = 1'''
		cur.execute(sql)
			
		rows = cur.fetchall()	
		
		for row in rows:
			print('Item Name: ', row[0], '\nPrice: ', row[1], '\nAmount: ', row[2], '\n')
			subtotal += (row[1] * row[2])
			
		print('Subtotal:', subtotal, '\n')
		j = input('Checkout? (Y):')
		
		if (j == 'Y'):
			k = input('Pay with balance (1) or credit card (2)?:')
			if (subtotal > int(user.get_balance()) and int(k) == 1):
				print('Insufficient balance. Transaction halted.\n')
			elif (user.get_credit_card() == "none" and int(k) == 2):
				print('No credit card on file. Transaction halted.\n')
			else:
				if(int(k) == 1): 
					user.reduce_balance(subtotal)
				
				#add transaction to transaction db
				sql = '''INSERT INTO user_orders(account_id, subtotal, purchase_date, date_shipped, tracking_no, order_status) VALUES (?,?,?,?,?,?)'''
				params = (1, subtotal, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "NULL", "NULL", 0)
				cur.execute(sql, params)
				transaction_id = cur.lastrowid
				
				#add purchased items to purchased items db
				for row in rows:
					sql = '''INSERT INTO purchased_items(transaction_id, item_name, amount, item_price, vote_score) VALUES (?,?,?,?,?)'''
					params = (transaction_id, row[0], row[2], row[1], "NULL")
					cur.execute(sql, params)
					
					sql = '''UPDATE product SET quantity_sold = quantity_sold + ? WHERE item_name = ?'''
					params = (row[2], row[0])
					cur.execute(sql, params)
				
				#clear user cart
				sql = '''DELETE FROM cart WHERE account_id = 1'''
				cur.execute(sql)
				
				#update user balance
				sql = '''UPDATE personal_acc SET balance = ? WHERE account_id = 1'''
				params = [user.get_balance()]
				cur.execute(sql, params)
				
				print('Transaction Successful\n')
			else:
				print('Insufficient balance or no credit card on file. Transaction halted.\n')
				
def view_history():
	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT transaction_id, subtotal, purchase_date, order_status, date_shipped, tracking_no, shipper FROM user_orders WHERE account_id = 1'''
		cur.execute(sql)
			
		rows = cur.fetchall()	
		
		for row in rows:
			status = "Status unknown."
			if(row[3] == 0):
				status = "Looking for shipper."
			elif(row[3] == 1):
				status = "Processing shipment."
			elif(row[3] == 2):
				status = "Order shipped."
			elif(row[3] == 3):
				status = "Order delivered."
			print('Transaction Id: ', row[0], '\nSubtotal: ', row[1], '\nDate purchased: ', row[2], '\nOrder Status: ', status, '\nDate Shipped: ', row[4], '\nTracking No.: ', row[5], '\nShipped By: ', row[6], '\n')
		
		j = input('View transaction details?:')
		
		if(int(j) == 3):
			sql = '''SELECT item_name, amount, item_price, vote_score FROM purchased_items WHERE transaction_id = 3'''
			cur.execute(sql)
			
			rows = cur.fetchall()
			
			for row in rows:
				if (row[3] == "NULL"):
					row[3] == "None"
				print('Item: ', row[0], '\nAmount Purchased: ', row[1], '\nPrice: ', row[2], '\nUser Score: ', row[3], '\n')
		
			k = input('Pick item to vote on:')
			
			if(int(k) == 1):
				l = input('Enter score between 1 to 5: ')
				
				sql = '''UPDATE purchased_items SET vote_score = ? WHERE transaction_id = 3 AND item_name = ?'''
				params = (int(l), row[0])
				cur.execute(sql, params)
				
				print('Vote cast successfully.\n')
				
def view_information():
	with store_db:
		cur = store_db.cursor()
		sql = '''SELECT email, acc_status, warnings, first_name, last_name, address, balance, credit_card FROM account INNER JOIN personal_acc ON account.account_id = personal_acc.account_id WHERE account.account_id = 1'''
		cur.execute(sql)
			
		rows = cur.fetchall()	
		
		status = ""
		for row in rows:
			if(row[1] == 0):
				status = "Good standing."
			elif(row[1] == 1):
				status = "Last chance."
			elif(row[1] == 2):
				status = "Permanently banned."
				
		print('Name: ', row[3], row[4], '\nAddress: ', row[5], '\nEmail: ', row[0], '\nBalance: ', row[6], '\nCredit Card: ', row[7], '\nWarnings: ', row[2], '\nAccount Status: ', status, '\n')

user = RegisteredAccount.RegisteredAccount(1, 'First', 'Name', '4321 street', 50000, '1111-1111-1111-1111', 0, 'e@mail.com')
i = 0

database = r"store_system.db"
store_db = create_connection(database)

while i > -1:
	print('Main Menu\n')
	print('1. View Cart.\n')
	print('2. View Purchasing History.\n')
	print('3. View Account Information.\n')
	print('4. Select Default Payment Option.\n')
	i = int(input('Enter a number:'))
	menu_nav(i)