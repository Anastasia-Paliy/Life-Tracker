import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QTextEdit,
                             QLineEdit, QLabel)
from backend import add_note, edit_note


class Signal(QObject):

    closed = pyqtSignal()
    


class Edit_Window(QWidget):

    def __init__(self, action, notes, prev_text = None):
        super().__init__()
    
        self.action = action
        self.notes = notes
        self.prev = prev_text
        self.initUI()



    def initUI(self):

        self.setFixedSize(400, 400)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.textWidget = QTextEdit()
        self.titleWidget = QLineEdit()
        
        hbox = QHBoxLayout(self)
        leftWidget = QWidget()
        hbox.addWidget(leftWidget)
        rightWidget = QWidget()
        hbox.addWidget(rightWidget)
        
        vbox1 = QVBoxLayout(leftWidget)
        vbox1.addWidget(self.titleWidget)
        vbox1.addWidget(self.textWidget)
        
        saveButton = QPushButton('Save', self)
        saveButton.resize(saveButton.sizeHint())
        #saveButton.move(150, 250)
        saveButton.setObjectName('save')
        saveButton.clicked.connect(self.close)

        deleteButton = QPushButton('Delete', self)
        deleteButton.resize(deleteButton.sizeHint())
        #deleteButton.move(150, 250)
        deleteButton.setObjectName('delete')
        deleteButton.clicked.connect(self.close)

        startLabel = QLabel("start date")
        startDate = QLineEdit()
        dueLabel = QLabel("due date")
        dueDate = QLineEdit()
        tagLabel = QLabel("tag")
        tagInput = QLineEdit()
        
        vbox2 = QVBoxLayout(rightWidget)
        vbox2.addWidget(deleteButton)
        vbox2.addWidget(startLabel)
        vbox2.addWidget(startDate)
        vbox2.addWidget(dueLabel)
        vbox2.addWidget(dueDate)
        vbox2.addWidget(tagLabel)
        vbox2.addWidget(tagInput)
        vbox2.addWidget(saveButton)
        
        


        self.signal = Signal()
        
        return self
    

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

    def save(self):
        
        text = self.textWidget.toPlainText()
        
        if self.action == 'edit':
            self.notes == edit_note(self.notes, self.prev, text)

        elif self.action == 'new':
            self.notes = add_note(self.notes, text)

        else:
            raise ValueError("Invalid value of edit_window.action")

    
    def closeEvent(self, event):

        try:
            sending_button = self.sender()
            text = sending_button.objectName()
            if text == 'save':
                self.save()
            else:
                raise Exception
            
        except:
            
            reply = QMessageBox.question(self, 'Message',
                "Save before closing?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.save()

        self.signal.closed.emit()
        
        event.accept()



    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Edit_Window('new', [])
    ex.show()
    sys.exit(app.exec_())
