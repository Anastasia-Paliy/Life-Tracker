import sys
from sql import SQL
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout,
                             QDesktopWidget, QScrollArea, QPushButton, QLabel)



class Statistics(QWidget):

    def __init__(self, sql):
        super().__init__()
        
        self.sql = sql
      
        self.initUI()


    def initUI(self):

        #self.setFixedSize(400, 200)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))

        vbox = QVBoxLayout(self)

        stat = self.sql.get_total()

        l1 = QLabel(f'<font color="black">* Open tasks: </font>'
                    f'<font color="#3D3DCA">{stat[0]}</font>')
        vbox.addWidget(l1)
        
        l2 = QLabel(f'<font color="black">* Closed tasks: </font>'
                    f'<font color="#3D3DCA">{stat[1]}</font>')
        vbox.addWidget(l2)
        
        l3 = QLabel(f'<font color="black">* Deleted tasks: </font>'
                    f'<font color="#3D3DCA">{stat[2]}</font>')
        vbox.addWidget(l3)
        
        l4 = QLabel(f'<font color="black">* All tasks: </font>'
                    f'<font color="#3D3DCA">{stat[3]}</font>')
        vbox.addWidget(l4)

        vbox.addWidget(QLabel(''))

        l5 = QLabel(f'<font color="black">* Average number of changing tasks: </font>'
                    f'<font color="#3D3DCA">{stat[4]}</font>')
        vbox.addWidget(l5)

        l6 = QLabel(f'<font color="black">* Average number of changing due date: </font>'
                    f'<font color="#3D3DCA">{stat[5]}</font>')
        vbox.addWidget(l6)

        vbox.addWidget(QLabel(''))

        if stat[6] != '-':
            if '-' in stat[6]:
                stat[6] = stat[6].replace('-', '')
                BA = 'after'
            else:
                BA = 'before'

            l7 = QLabel(f'<font color="black">* Planning </font>'
                        f'<font color="#3D3DCA">{stat[6]}</font>'
                        f'<font color="black"> {BA} start date')
            vbox.addWidget(l7)

        if stat[7] != '-':
            if '-' in stat[7]:
                stat[7] = stat[7].replace('-', '')
                BA = 'after'
            else:
                BA = 'before'
            l8 = QLabel(f'<font color="black">* Closing </font>'
                        f'<font color="#3D3DCA">{stat[7]}</font>'
                        f'<font color="black"> {BA} due date')
            vbox.addWidget(l8)

        if stat[8] != '-':
            if '-' in stat[8]:
                stat[8] = stat[8].replace('-', '')

                l9 = QLabel(f'<font color="black">* Postponing deadline for </font>'
                            f'<font color="#3D3DCA">{stat[8]}</font>')
            else:
                l9 = QLabel(f'<font color="black">* Moving deadline </font>'
                            f'<font color="#3D3DCA">{stat[8]}</font>'
                            f'<font color="black"> forward')
            
            vbox.addWidget(l9)

        #print(stat)


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Statistics(SQL("notes.db"))
    ex.show()
    sys.exit(app.exec_())
