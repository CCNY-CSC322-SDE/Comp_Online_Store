class RegisteredAccount:
	def __init__(self, a_id, first_name, last_name, address, balance, credit_card, warnings, email):
		self.account_id = a_id
		self.first_name = first_name
		self.last_name = last_name
		self.address = address
		self.balance = balance
		self.credit_card = credit_card
		self.warnings = warnings
		self.email = email
		
	def add_balance(self, balance_added):
		self.balance += balance_added
	
	def reduce_balance(self, balance_reduced):
		self.balance -= balance_reduced
		
	def set_credit_card(self, cc_number):
		self.credit_card = cc_number
		
	def get_account_id(self):
		return self.account_id
	
	def get_first_name (self):
		return self.first_name
		
	def get_last_name (self):
		return self.last_name
		
	def get_address(self):
		return self.address
		
	def get_balance(self):
		return self.balance
		
	def get_credit_card(self):
		return self.credit_card
		
	def get_warnings(self):
		return warnings
	
	def get_email(self):
		return email
		
	