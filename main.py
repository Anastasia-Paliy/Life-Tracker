import sys
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QIcon
from gui import TaskList
from backend import SQL
from edit import Edit_Window
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout,
                             QDesktopWidget, QScrollArea, QPushButton)

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.sql = SQL("notes.db")
        self.tag = "Any"
        self.view = 'TaskBoard'

        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        self.newNoteB = QPushButton('New note')
        self.newNoteB.clicked.connect(self.new_note)
        self.allTasksB = QPushButton('All tasks')
        self.allTasksB.clicked.connect(self.showAll)
        self.statisticsB = QPushButton('Statistics')
        self.taskboardB = QPushButton('TaskBoard')
        self.taskboardB.clicked.connect(self.showBoard)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.statisticsB)
        hbox1.addWidget(self.allTasksB)
        hbox1.addWidget(self.taskboardB)
        hbox1.addStretch()
        hbox1.addWidget(self.newNoteB)
        
        self.buttonsW = QWidget()
        self.buttonsW.setLayout(hbox1)
        
        self.button = self.taskboardB
                
        self.initUI()
    

    def initUI(self):
        
        hbox = QHBoxLayout()
        self.button.setEnabled(True)
        
        if self.view == 'TaskBoard':
            tags = self.sql.get_tags()
            self.button = self.taskboardB
            self.setFixedSize(min(400*len(tags)+60,1260), 710)
        elif self.view == 'All tasks':
            tags = [None]
            self.button = self.allTasksB
            self.setFixedSize(450, 700)
        else:
            print('Mistake')   

        for tag in tags:
            taskList = TaskList(self, self.sql, tag)
            hbox.addWidget(taskList)
            
        taskboard = QWidget()
        taskboard.setLayout(hbox)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(taskboard)

        self.button.setEnabled(False)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)
        vbox.addWidget(self.buttonsW)

        self.widget = QWidget()
        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)

        self.show()


    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def update_window(self):
        
        self.initUI()


    def showAll(self):
        self.view = 'All tasks'
        self.update_window()
        

    def showBoard(self):
        self.view = 'TaskBoard'
        self.update_window()


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
    ex = MainWindow()
    sys.exit(app.exec_())
