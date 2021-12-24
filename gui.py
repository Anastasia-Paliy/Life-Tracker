import sys
from edit import Edit_Window
from sql import SQL
from backend import auto_transfer
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea)
 


class TaskList(QWidget):

    def __init__(self, parent, sql, tag, index):

        super().__init__()

        self.setFixedSize(300, 462)
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        self.parent = parent
        self.sql = sql
        self.tag = tag
        self.index = index

        self.colors = ['#ABA5FF', '#D5B5FF', '#F1B5FF', '#FFC4FE', '#FFFEC4', '#E2FFB5', '#CDFFDC', '#D2F7FF']
        self.Tcolors = ['#8B84EB', '#B084EB', '#E398F6', '#F698F3', '#FFFC95', '#CEFF86', '#9DFFBA', '#ACEFFF']
        
        self.initUI()


    def initUI(self):      
        
        self.notesBox = QVBoxLayout()
        self.notesWidget = QWidget()
        
        self.display_notes()
            
        self.notesBox.addStretch()
            
        self.notesWidget.setLayout(self.notesBox)
        scroll = QScrollArea()
        scroll.setWidget(self.notesWidget)
        scroll.setWidgetResizable(True)
        scroll.adjustSize()
        vbox = QVBoxLayout(self)

        n = len(self.colors)

        if self.tag != None:
            tagButton = QPushButton(self.tag, self)
            tagButton.setStyleSheet('background-color: '+self.Tcolors[self.index % n])
            vbox.addWidget(tagButton)
            
        vbox.addWidget(scroll)

        self.setStyleSheet('background-color: #E1E1E1')
        

    def display_notes(self):

        n = len(self.colors)
        
        for note in reversed(self.sql.select_notes_by_tag(self.tag)):
            noteButton = QPushButton(f'{auto_transfer(note[1])}', self)
            noteButton.setObjectName(str(note[0]))
            noteButton.clicked.connect(self.parent.open_note)
            noteButton.setStyleSheet('background-color: '+self.colors[self.index % n])
            self.notesBox.addWidget(noteButton)
                


if __name__ == '__main__':

    app = QApplication(sys.argv)
    sql = SQL("notes.db")
    ex = TaskList(sql, None)
    ex.show()
    res = app.exec_()
    ex.sql.cursor.close()
    ex.sql.conn.close()
    sys.exit(res)

    
