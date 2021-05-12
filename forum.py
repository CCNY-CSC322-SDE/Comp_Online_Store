import sys

from PyQt5.uic.properties import QtGui
from Api import forum
from Api import account
from PyQt5.QtWidgets import *


class ForumListItem(QWidget):
    def __init__(self, parent=None, forum_thread=None):
        super(ForumListItem, self).__init__(parent)
        print("Testing purposes {title} - {productName}".format(title=forum_thread.title,
                                                                productName=forum_thread.product_name))
        self.forumThread = forum_thread
        self.threadItemBoxLayout = QHBoxLayout()
        self.titleLabel = QLabel(forum_thread.title)
        self.productNameLabel = QLabel(forum_thread.product_name)
        self.dateLabel = QLabel(forum_thread.date)

        self.threadItemBoxLayout.addWidget(self.titleLabel)
        self.threadItemBoxLayout.addWidget(self.productNameLabel)
        self.threadItemBoxLayout.addWidget(self.dateLabel)

        self.setLayout(self.threadItemBoxLayout)


class ReplyListItem(QWidget):
    def __init__(self, parent=None, forumReply=None, personalAccount=None):
        super(ReplyListItem, self).__init__(parent)
        self.forumReply = forumReply
        self.personalAccount = personalAccount
        self.threadItemBoxLayout = QHBoxLayout()
        self.authorLabel = QLabel()
        self.postLabel = QLabel()

        self.authorLabel.setText(self.personalAccount.first_name)
        self.postLabel.setText(self.forumReply.post)

        self.threadItemBoxLayout.addWidget(self.authorLabel)
        self.threadItemBoxLayout.addWidget(self.postLabel)

        self.setLayout(self.threadItemBoxLayout)


class ForumThread(QMainWindow):
    def __init__(self, parent=None, thread_no=0):
        super(ForumThread, self).__init__(parent)
        self.thread_no = thread_no
        self.postTextEdit = QTextEdit()
        self.forumRepliesListWidget = QListWidget()
        self.createReplyButton = QPushButton()

        widget = QWidget()
        layout = QVBoxLayout()

        self.createReplyButton.setText("Create Reply")
        self.createReplyButton.clicked.connect(self.createReply)

        layout.addWidget(self.forumRepliesListWidget)
        self.formLayout = QFormLayout()
        self.formLayout.addRow(QLabel("Text"), self.postTextEdit)
        layout.addChildLayout(self.formLayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def getThreadReplies(self):
        replies = forum.getThreadReplies(self.thread_no)
        for reply in replies:
            personalAccount = account.getPersonalAccount(reply.account_id)
            replyItem = ReplyListItem(parent=None, forumReply=reply, personalAccount=personalAccount)
            qListWidgetItem = QListWidgetItem(self.forumRepliesListWidget)
            qListWidgetItem.setSizeHint(replyItem.sizeHint())
            self.forumRepliesListWidget.addItem(qListWidgetItem)
            self.forumRepliesListWidget.setItemWidget(qListWidgetItem, replyItem)

    def createReply(self):
        if len(self.postTextEdit.text()) > 0:
            forum.createReply(self.thread_no, 0, self.postTextEdit.text())
            self.postTextEdit.setText("...")


class ForumApp(QMainWindow):
    def __init__(self):
        super(ForumApp, self).__init__(None)
        self.setWindowTitle("Forum")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        widget = QWidget()
        layout = QVBoxLayout()

        self.productLineEdit = QLineEdit()
        self.forumTextEdit = QLineEdit()
        self.createThreadButton = QPushButton()
        self.forumListWidget = QListWidget()
        self.setUpForumList()

        self.topRowLayout = QHBoxLayout()
        self.topRowLayout.addWidget(QLabel("Title"))
        self.topRowLayout.addWidget(QLabel("Product"))
        self.topRowLayout.addWidget(QLabel("Date"))

        self.forumTextEdit.setPlaceholderText("Enter thread title...")
        self.productLineEdit.setPlaceholderText("Enter product name...")
        self.createThreadButton.setText("Create Thread")
        self.createThreadButton.clicked.connect(self.createThread)
        self.forumListWidget.itemClicked.connect(self.forumClick)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(QLabel("Product Name"), self.productLineEdit)
        self.formLayout.addRow(QLabel("Title"), self.forumTextEdit)
        self.formLayout.addWidget(self.createThreadButton)

        layout.addLayout(self.topRowLayout)
        layout.addWidget(self.forumListWidget)
        layout.addLayout(self.formLayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setUpForumList(self):
        threads = forum.getThreads()
        self.forumListWidget.clear()
        for thread in threads:
            print(thread.product_name)
            listItem = ForumListItem(parent=None, forum_thread=thread)
            qListWidgetItem = QListWidgetItem(self.forumListWidget)
            qListWidgetItem.setSizeHint(listItem.sizeHint())
            self.forumListWidget.addItem(qListWidgetItem)
            self.forumListWidget.setItemWidget(qListWidgetItem, listItem)

    def forumClick(self, forumItem):
        print(forumItem)
        thread = ForumThread(parent=self, thread_no=forumItem.forumThread.thread_no)
        thread.show()

    def createThread(self):
        forumText = str(self.forumTextEdit.text())
        productText = str(self.productLineEdit.text())
        if len(forumText) > 0 and len(productText) > 0:
            forum.createThread(productText, 0, forumText)
            self.forumTextEdit.setText("")
            self.productLineEdit.setText("")
            self.setUpForumList()


def main():
    app = QApplication(sys.argv)
    window = ForumApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
