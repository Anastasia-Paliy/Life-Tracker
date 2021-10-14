import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea)


class Main_Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setFixedSize(400, 600)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        notesBox = QVBoxLayout()
        notesWidget = QWidget()
        
        for i in range(25):
            note = QPushButton('Some note', self)
            #note.setMinimumSize(300, 40)
            notesBox.addWidget(note)
            
        notesWidget.setLayout(notesBox)
        scroll = QScrollArea()
        scroll.setWidget(notesWidget)
        scroll.setWidgetResizable(True)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(scroll)

        button = QPushButton('New note', self)
        button.resize(button.sizeHint())
        button.move(150, 250)

        vbox.addWidget(button) 

        self.show()
        

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())