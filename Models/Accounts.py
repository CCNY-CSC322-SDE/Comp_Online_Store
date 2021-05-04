class BaseAccount:
    def __init__(self, account_id, first_name, last_name):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name


class Account(BaseAccount):
    def __init__(self, account_id, email, acc_status, password):
        self.account_id = account_id
        self.email = email
        self.acc_status = acc_status
        self.password = password


class PersonalAccount(BaseAccount):
    def __init__(self, account_id, first_name, last_name, address, balance, credit_card):
        BaseAccount.__init__(self, account_id, first_name, last_name)
        self.address = address
        self.balance = balance
        self.credit_card = credit_card


class DeliveryAccount:
    def __init__(self, account_id, company_name):
        self.company_name = company_name


class ClerkAccount(BaseAccount):
    def __init__(self, account_id, first_name, last_name):
        BaseAccount.__init__(self, account_id, first_name, last_name)


class ManagerAccount(BaseAccount):
    def __init__(self,account_id,first_name,last_name):
        BaseAccount.__init__(self,account_id,first_name,last_name)


class SupplierAccount:
    def __init__(self,account_id,company_name):
        self.account_id = account_id
        self.company_name = company_name