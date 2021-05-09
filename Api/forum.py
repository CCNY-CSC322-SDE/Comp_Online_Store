import sqlite3
from sqlite3 import Error

from Api import account
from Models.Forums import ForumThread
from Models.Forums import ForumReply

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


# Return a list of all threads in database as a list of ForumThread objects
def getThreads():
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM forum_thread'''
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            results.append(ForumThread(row[0], row[1]))
    return results


def createThread(product_name):
    if store_db == None:
        initialize()
    with store_db:
        cur = store_db.cursor()
        sql = '''INSERT INTO forum_thread (product_name) VALUES(''' + product_name + ''')'''
        cur.execute(sql)


def getThreadReplies(thread_no):
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM forum_reply'''
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            results.append(ForumReply(row[0], row[1], row[2], row[3]))
    return results


def createReply(thread_no, account_id, post):
    if store_db == None:
        initialize()
    with store_db:
        cur = store_db.cursor()
        sql = '''SELECT * FROM taboo_phrases'''
        cur.execute(sql)
        rows = cur.fetchall()

        # Look for taboo words and redact if anything.
        words = post.lower().trim().split(" ")
        newPost = ""
        foundTaboo = False
        for row in rows:
            for word in words:
                if row[0] in word:
                    newPost = newPost + " * "
                    foundTaboo = True
                else:
                    newPost = newPost + " " + word + " "
        if foundTaboo:
            createWarning(offender_id=account_id, reason="Taboo word found in post")
        # Finally insert reply to database
        sql = '''INSERT INTO forum_reply (thread_no,account_id,post) VALUES(?, ?, ?)'''
        cur.execute(sql, (thread_no, account_id, newPost))


# Creates a warning for offender_id. Also updates account status
def createWarning(offender_id, reason):
    if store_db == None:
        initialize()
    results = []
    with store_db:
        cur = store_db.cursor()
        sql = '''INSERT INTO warning(offender_id,reason) VALUES(?,?)'''
        cur.execute(sql, (offender_id, reason))

        # Check if they have 3 warnings. If so ban account
        sql = '''SELECT * FROM warning WHERE offender_id=?'''
        cur.execute(sql, (offender_id))
        if cur.rows() >= 3:
            account.suspendAccount(offender_id)
        account.updateAccountStatus(offender_id)
