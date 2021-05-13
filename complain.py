from PyQt5.QtWidgets import QPushButton, QTextEdit, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QMainWindow, QLabel
from Api import forum


class ComplainWindow(QMainWindow):
    def __init__(self, parent=None, account_id=0, offender_id=0):
        super(ComplainWindow, self).__init__(parent)
        self.complainTextEdit = QTextEdit()
        self.account_id = account_id
        self.offender_id = offender_id
        self.cancelButton = QPushButton("Cancel")
        self.complainButton = QPushButton("Post Complaint")
        self.label = QLabel("Enter the reason for your complaint")
        self.setWindowTitle("Complain window")
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.cancelButton.clicked.connect(self.cancel)
        self.complainButton.clicked.connect(self.makeComplain)
        self.complainTextEdit.setPlaceholderText("Complaint Reason...")

        widget = QWidget()
        layout = QVBoxLayout()

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.complainButton)

        layout.addWidget(self.label)
        layout.addWidget(self.complainTextEdit)
        layout.addLayout(self.buttonLayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def makeComplain(self):
        text = str(self.complainTextEdit.toPlainText()).strip()
        forum.createComplaint(self.account_id, self.offender_id, text)
        self.close()

    def cancel(self):
        self.close()
