import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QTextEdit,
                             QLineEdit, QLabel)



class Signal(QObject):

    closed = pyqtSignal()
    


class Edit_Window(QWidget):

    def __init__(self, action, sql, ID = None):
        super().__init__()
        
        self.action = action
        self.sql = sql
        self.ID = ID
        self.initUI()
        
        if self.action == 'edit':
            note = self.sql.get_note(ID)
            print(note)
            self.titleWidget.setText(note[1])
            self.textWidget.setPlainText(note[2])
            self.startDate.setText(note[3])
            self.dueDate.setText(note[4])
            self.tagInput.setText(note[5])

        
        """
        try:
            print(self.sql.get_note(ID))
        except:
            print('ERROR')
        """
        """
        if self.action == 'edit':
            self.textWidget.setPlainText(self.sql.get_note(ID)[1])
        """    


    def initUI(self):

        self.setFixedSize(600, 410)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.textWidget = QTextEdit()
        self.titleWidget = QLineEdit()
        self.textWidget.setPlainText('Put your text here...')
        self.titleWidget.setText('Title')
        
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

        formatLabel = QLabel("\nDate & time format:\n01.01.2021 00:00")

        startLabel = QLabel("\nstart date:")
        self.startDate = QLineEdit()
        dueLabel = QLabel("\ndue date:")
        self.dueDate = QLineEdit()
        tagLabel = QLabel("\ntag:")
        self.tagInput = QLineEdit()
        emptyLabel = QLabel("\n")
        
        vbox2 = QVBoxLayout(rightWidget)
        vbox2.addWidget(deleteButton)
        vbox2.addWidget(formatLabel)
        vbox2.addWidget(startLabel)
        vbox2.addWidget(self.startDate)
        vbox2.addWidget(dueLabel)
        vbox2.addWidget(self.dueDate)
        vbox2.addWidget(tagLabel)
        vbox2.addWidget(self.tagInput)
        vbox2.addWidget(emptyLabel)
        vbox2.addWidget(saveButton)

        rightWidget.setFixedWidth(160)
        
    
        self.signal = Signal()
        
        return self
    

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def get_values(self):

        title = self.titleWidget.text()
        text = self.textWidget.toPlainText()
        start = self.startDate.text()
        due = self.dueDate.text()
        tag = self.tagInput.text()

        return (title, text, start, due, tag)
        

    def save(self):
        (title, text, start, due, tag) = self.get_values()
        
        if self.action == 'edit':
            self.sql.edit_note(self.ID, title, text, start, due, tag)

        elif self.action == 'new':
            self.sql.add_note(title, text, start, due, tag)

        else:
            print("Invalid value of edit_window.action")


    def delete(self):
        
        (title, text, start, due, tag) = self.get_values()
        self.sql.delete_note(self.ID)
        

    
    def closeEvent(self, event):

        try:
            sending_button = self.sender()
            text = sending_button.objectName()

            if text == 'save':
                self.save()
            elif text == 'delete' and self.action == 'edit':
                self.delete()
            elif text == 'delete' and self.action == 'new':
                pass
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
