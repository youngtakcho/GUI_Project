from PyQt5 import QtCore


class LoginAttemptThread(QtCore.QThread):
    result = QtCore.pyqtSignal(bool,str)
    def __init__(self,parent = None,address = ("",8080)):
        QtCore.QThread.__init__(self,parent)
        self.address = address
    def run(self) -> None:
        self.sleep(5)

        self.result.emit(True,"id is not correct")
    def __del__(self):
        """socket should be free in this step"""
        pass