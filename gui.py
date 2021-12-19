import sys
from edit import Edit_Window
from backend import SQL
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop, pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea)
 


class TaskList(QWidget):

    def __init__(self, parent, sql, tag):

        super().__init__()

        self.setFixedSize(400, 595)
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        self.parent = parent
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
        vbox = QVBoxLayout(self)

        if self.tag != None:
            tagButton = QPushButton(self.tag, self)
            tagButton.resize(tagButton.sizeHint())
            tagButton.setEnabled(False)
            vbox.addWidget(tagButton)
            
        vbox.addWidget(scroll)
        

    def display_notes(self):
        
        for note in reversed(self.sql.select_notes_by_tag(self.tag)):
            noteButton = QPushButton(f'{note[1]}', self)
            noteButton.setObjectName(str(note[0]))
            noteButton.clicked.connect(self.parent.open_note)
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

    
