class Taboo:
    def __init__(self, phrase):
        self.phrase = phrase


class ForumThread:
    def __init__(self, thread_no, product_name):
        self.thread_no = thread_no
        self.product_name = product_name


class ForumReply:
    def __init__(self, post_no, thread_no, account_id, post):
        self.post_no = post_no
        self.thread_no = thread_no
        self.account_id = account_id
        self.post = post
