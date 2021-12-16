import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from gui import TaskList
from backend import SQL
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QHBoxLayout,
                             QDesktopWidget, QScrollArea)

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.setFixedSize(1250, 650)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.sql = SQL("notes.db")
        
        self.initUI()
    

    def initUI(self):
        
        hbox = QHBoxLayout()
        
        for tag in self.sql.get_tags():
            taskList = TaskList(self.sql, tag)
            hbox.addWidget(taskList)

        self.widget = QWidget()
        self.widget.setLayout(hbox)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.show()


    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def update_window(self):
        
        self.initUI()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
