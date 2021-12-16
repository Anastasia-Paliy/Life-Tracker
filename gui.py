import sys
from edit import Edit_Window
from backend import SQL
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea)


class Signal(QObject):

    updated = pyqtSignal()
    edit_window_opened = pyqtSignal()
    


class TaskList(QWidget):

    def __init__(self, sql, tag):

        super().__init__()

        self.setFixedSize(400, 600)
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.sql = sql
        self.tag = tag
        
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

        button = QPushButton('New note', self)
        button.resize(button.sizeHint())
        button.clicked.connect(self.new_note)
        
        vbox = QVBoxLayout(self)

        if self.tag != None:
            tagButton = QPushButton(self.tag, self)
            tagButton.resize(tagButton.sizeHint())
            tagButton.setEnabled(False)
            vbox.addWidget(tagButton)
            
        vbox.addWidget(scroll)
        vbox.addWidget(button)

        #self.signal = Signal()
        

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def display_notes(self):
        
        for note in reversed(self.sql.select_notes_by_tag(self.tag)):
            noteButton = QPushButton(f'{note[1]}', self)
            noteButton.setObjectName(str(note[0]))
            noteButton.clicked.connect(self.open_note)
            self.notesBox.addWidget(noteButton)


    def update_window(self):
        
        self.initUI()
        self.show()
                

    def edit_window_processing(self):
        
        self.edit_window.show()
        loop = QEventLoop()
        self.edit_window.signal.closed.connect(loop.quit)
        loop.exec()
        self.update_window()
        #self.signal.updated.emit()


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
    sql = SQL("notes.db")
    ex = TaskList(sql, None)
    ex.show()
    res = app.exec_()
    ex.sql.cursor.close()
    ex.sql.conn.close()
    sys.exit(res)

    
