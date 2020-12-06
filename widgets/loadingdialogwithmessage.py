from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot
from PreDefineValues import STRING_UI_FILE_LOADING
from PreDefineValues import IMAGE_FOR_LOADING


class LoadingDialogWithMessage(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self,parent)
        uic.loadUi(STRING_UI_FILE_LOADING , self)
        self.lbl_loading_gif:QtWidgets.QLabel
        self.lbl_msg:QtWidgets.QLabel

        self.loading_movie = QtGui.QMovie(IMAGE_FOR_LOADING)
        self.loading_movie.setScaledSize(QtCore.QSize(self.lbl_loading_gif.width(),self.lbl_loading_gif.height()))
        self.lbl_loading_gif.setMovie(self.loading_movie)
        self.lbl_loading_gif.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.loading_movie.start()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def setMessage(self,msg):
        self.lbl_msg.setText(msg)
