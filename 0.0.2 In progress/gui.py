import sys
import json
from edit import Edit_Window
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea, QMainWindow)



class Main_Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        try:
            with open("notes.json", 'r') as file:
                notes = json.load(file)
        except FileNotFoundError:
            notes = []
            

        self.setFixedSize(400, 600)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        notesBox = QVBoxLayout()
        notesWidget = QWidget()

        for note in notes:
            my_notes = note.values()
            for item in my_notes:
                noteB = QPushButton(f'{item}', self)
                #noteB.setStyleSheet("QPushButton { text-align: left; }")
                #note.setMinimumSize(300, 40)
                notesBox.addWidget(noteB)
            
        notesWidget.setLayout(notesBox)
        scroll = QScrollArea()
        scroll.setWidget(notesWidget)
        scroll.setWidgetResizable(True)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)

        button = QPushButton('New note', self)
        button.resize(button.sizeHint())
        button.move(150, 250)
        button.clicked.connect(self.new_note)

        vbox.addWidget(button) 

        self.show()
        

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def new_note(self):
        edit_window = Edit_Window()
        edit_window.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
