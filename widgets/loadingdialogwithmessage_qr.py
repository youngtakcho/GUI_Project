from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot
from PreDefineValues import STRING_UI_FILE_LOADING
from PreDefineValues import IMAGE_FOR_LOADING


class LoadingDialogWithMessage_qr(QtWidgets.QDialog):
    def __init__(self, parent, data):
        QtWidgets.QDialog.__init__(self,parent)
        uic.loadUi(STRING_UI_FILE_LOADING , self)
        self.lbl_loading_gif:QtWidgets.QLabel
        self.lbl_msg:QtWidgets.QLabel
        self.data = data
        self.trans = QtCore.QTranslator(self)

        self.loading_movie = QtGui.QMovie(IMAGE_FOR_LOADING)
        self.loading_movie.setScaledSize(QtCore.QSize(self.lbl_loading_gif.width(),self.lbl_loading_gif.height()))
        self.lbl_loading_gif.setMovie(self.loading_movie)
        self.lbl_loading_gif.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.loading_movie.start()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.retranslateUi()
        QtCore.QCoreApplication.instance().removeTranslator(self.trans)
        if self.trans.load(data):
            QtCore.QCoreApplication.instance().installTranslator(self.trans)

    def setMessage(self,msg):
        self.lbl_msg.setText(msg)

    def retranslateUi(self):
        self.lbl_msg.setText(QtWidgets.QApplication.translate('load-server-qr',"Receiving QR Code for Scan from Server"))

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(LoadingDialogWithMessage_qr, self).changeEvent(event)

