import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, QMdiSubWindow,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QScrollBar,
                             QLabel, QScrollArea, QMainWindow, QMdiArea, QTextEdit)


class Edit_Window(QMdiSubWindow):

    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):

        self.setFixedSize(400, 400)
        self.center()
        self.setWindowTitle('Life Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        textWidget = QTextEdit()
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(textWidget)

        button = QPushButton('Save note', self)
        button.resize(button.sizeHint())
        button.move(150, 250)

        vbox.addWidget(button)

        totalWidget = QMdiSubWindow()
        totalWidget.setLayout(vbox)

        return totalWidget

        #self.show()
        

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Save before closing?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


'''
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Edit_Window()
    sys.exit(app.exec_())
'''
