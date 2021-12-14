import sys
import json
from edit import Edit_Window
from backend import SQL
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea, QMainWindow)



class Main_Window(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setFixedSize(400, 600)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        self.sql = SQL("notes.db")
        
        self.initUI()


    def initUI(self):      
        
        self.notesBox = QVBoxLayout()
        self.notesWidget = QWidget()

        self.display_notes()
            
        self.notesWidget.setLayout(self.notesBox)
        scroll = QScrollArea()
        scroll.setWidget(self.notesWidget)
        scroll.setWidgetResizable(True)
        scroll.adjustSize()

        button = QPushButton('New note', self)
        button.resize(button.sizeHint())
        button.move(150, 250)
        button.clicked.connect(self.new_note)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)
        vbox.addWidget(button)

        self.widget = QWidget()
        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)
        
        self.show()
        

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def display_notes(self):
        
        for note in reversed(self.sql.show_notes()):
            noteButton = QPushButton(f'{note[1]}', self)
            noteButton.setObjectName(str(note[0]))
            noteButton.clicked.connect(self.open_note)
            self.notesBox.addWidget(noteButton)

    def update_window(self):
        
        self.initUI()
                

    def edit_window_processing(self):
        
        self.edit_window.show()
        loop = QEventLoop()
        self.edit_window.signal.closed.connect(loop.quit)
        loop.exec()
        self.update_window()


    def new_note(self):
        
        self.edit_window = Edit_Window('new', self.sql)
        self.edit_window_processing()
        


    def open_note(self):
    
        sending_button = self.sender()
        ID = int(sending_button.objectName())
        self.edit_window = Edit_Window('edit', self.sql, ID)
        self.edit_window_processing()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
    ex.sql.cursor.close()
    ex.sql.conn.close()
    print('final')
