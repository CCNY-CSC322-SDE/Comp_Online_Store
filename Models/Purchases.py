class UserOrder:
    def __init__(self, transaction_id, account_id, subtotal, purchase_date, date_shipped, tracking_no, order_status,
                 shipper):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.subtotal = subtotal
        self.purchase_date = purchase_date
        self.date_shipped = date_shipped
        self.tracking_no = tracking_no
        self.order_status = order_status
        self.shipper = shipper
        self.transaction_id = transaction_id


class PurchasedItem:
    def __init__(self,transaction_id,item_name,amount,item_price,vote_score):
        self.transaction_id = transaction_id
        self.item_name = item_name
        self.amount = amount
        self.item_price = item_price
        self.vote_score = vote_score


class BidOffer:
    def __init__(self,account_id,transaction_id,bid_amount):
        self.account_id = account_id
        self.transaction_id = transaction_id
        self.bid_amount = bid_amount


class Cart:
    def __init__(self,account_id,product_id,amount):
        self.account_id = account_id
        self.product_id = product_id
        self.amount = amount

