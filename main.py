import sys
from gui import TaskList
from sql import SQL
from edit import Edit_Window
from statistics import Statistics
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout,
                             QDesktopWidget, QScrollArea, QPushButton)

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.sql = SQL("notes.db")
        self.tag = "Any"
        self.view = 'All tasks'
        
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        self.newNoteB = QPushButton('New task')
        self.newNoteB.setStyleSheet('background-color: rgb(153,247,191);')
        self.newNoteB.clicked.connect(self.new_note)
        self.allTasksB = QPushButton('All tasks')
        self.allTasksB.setStyleSheet('background-color: #E5A6EF')
        self.allTasksB.clicked.connect(self.showAll)
        self.statisticsB = QPushButton('Statistics')
        self.statisticsB.setStyleSheet('background-color: #FDFFA5')
        self.statisticsB.clicked.connect(self.showStat)
        self.taskboardB = QPushButton('TaskBoard')
        self.taskboardB.setStyleSheet('background-color: #ABA5FF')
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
            self.setFixedSize(min(325*len(tags), 950), 565)
            
        elif self.view == 'All tasks':
            tags = [None]
            self.button = self.allTasksB
            self.setFixedSize(340, 550)
            
        else:
            print('Mistake')   

        index = 0
        for tag in tags:
            taskList = TaskList(self, self.sql, tag, index)
            hbox.addWidget(taskList)
            index += 1
            
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


    def initStatistics(self):
        
        stat = Statistics(self.sql)

        self.setFixedSize(600, 350)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(stat)
        vbox.addStretch()
        vbox.addWidget(self.buttonsW)

        self.button.setEnabled(True)
        self.button = self.statisticsB
        self.button.setEnabled(False)

        self.widget = QWidget()
        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)
        

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def update_window(self):

        if self.view == 'Statistics':
            self.initStatistics()
        else:
            self.initUI()


    def showAll(self):
        
        self.view = 'All tasks'
        self.update_window()
        

    def showBoard(self):
        
        self.view = 'TaskBoard'
        self.update_window()
        

    def showStat(self):
        
        self.view = 'Statistics'
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
