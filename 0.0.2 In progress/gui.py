import sys
import json
from edit import Edit_Window
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea, QMainWindow, QMdiArea)



class Main_Window(QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.initUI()


    def initUI(self):

        try:
            with open("notes.json", 'r') as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = []
        
        
        self.setFixedSize(400, 600)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        notesBox = QVBoxLayout()
        notesWidget = QWidget()

        for note in self.notes:
            my_notes = note.values()
            for item in my_notes:
                noteB = QPushButton(f'{item}', self)
                noteB.setObjectName(item)
                noteB.clicked.connect(self.open_note)
                notesBox.addWidget(noteB)
            
        notesWidget.setLayout(notesBox)
        scroll = QScrollArea()
        scroll.setWidget(notesWidget)
        scroll.setWidgetResizable(True)
        scroll.adjustSize()

        button = QPushButton('New note', self)
        button.resize(button.sizeHint())
        button.move(150, 250)
        button.clicked.connect(self.new_note)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)
        vbox.addWidget(button)

        self.mdi = QMdiArea()
        self.mdi.setLayout(vbox)
        self.setCentralWidget(self.mdi)
        
        self.show()
        

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def new_note(self):
        
        self.edit_window = Edit_Window()
        self.edit_window.show()


    def open_note(self):
    
        sending_button = self.sender()
        text = sending_button.objectName()
        self.edit_window = Edit_Window()
        self.edit_window.textWidget.setPlainText(text)
        self.edit_window.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
