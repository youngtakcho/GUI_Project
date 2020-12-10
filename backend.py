from PyQt5 import QtCore
from numpy import ndarray
from PreDefineValues import ID_QR_CODE_AUTH,ID_QR_CODE_DOWNLOAD,ID_QR_CODE_SCAN
import os

""" Do not change this thread WifiAttemptThread"""
class WifiAttemptThread(QtCore.QThread):
    wifi_result_temp = QtCore.pyqtSignal(bool,str)
    def __init__(self,SSID,key,parent = None,address = ("",8080)):
        QtCore.QThread.__init__(self,parent)
        self.address = address
        self.SSID = SSID
        self.key = key

    def run(self) -> None:
        self.sleep(3)
        command = "nmcli dev wifi connect '"+self.SSID+"' password '"+self.key+"'"
        os.system(command)
        self.wifi_result_temp.emit(True,"Incorrect Credentials")
    def __del__(self):
        """socket should be free in this step"""
        pass
""" Do not change this thread WifiAttemptThread"""

class LoadingProcess(QtCore.QThread):
    loadingPrograssUpdated = QtCore.pyqtSignal(int)
    loadingFinished = QtCore.pyqtSignal()

    def __init__(self,parent):
        QtCore.QThread.__init__(self,parent=parent)
    def run(self) -> None:
        self.msleep(500)
        self.loadingPrograssUpdated.emit(20)
        self.msleep(500)
        self.loadingPrograssUpdated.emit(40)
        self.msleep(500)
        self.loadingPrograssUpdated.emit(60)
        self.msleep(500)
        self.loadingPrograssUpdated.emit(80)
        self.msleep(500)
        self.loadingPrograssUpdated.emit(99)
        self.msleep(500)
        self.loadingFinished.emit()

class LoginAttemptThread(QtCore.QThread):
    login_result = QtCore.pyqtSignal(bool, str)
    def __init__(self,parent = None,address = ("",8080)):
        QtCore.QThread.__init__(self,parent)
        self.address = address
    def run(self) -> None:
        self.sleep(1)

        self.login_result.emit(True, "id is not correct")
    def __del__(self):
        """socket should be free in this step"""
        pass


class RequestQrCodeImage(QtCore.QThread):
    imageReceived = QtCore.pyqtSignal(bool,int,ndarray)
    def __init__(self,parent = None,address = ("",8080),request_msg = None,qr_type = ID_QR_CODE_AUTH):
        QtCore.QThread.__init__(self,parent)
        self.address = address
        self.to_serer_msg = request_msg
        self.qr_type = qr_type

    def run(self) -> None:
        self.sleep(1)
        fortest = ndarray((0,0,0))
        self.imageReceived.emit(True,self.qr_type,fortest)

    def __del__(self):
        """socket should be free in this step"""
        pass


class WaitForServerAuthWithQR(QtCore.QThread):
    authenticatedReceived = QtCore.pyqtSignal(bool,str)
    def __init__(self,parent = None,address = ("",8080),request_msg = None):
        QtCore.QThread.__init__(self,parent)
        self.address = address
        self.to_serer_msg = request_msg

    def run(self) -> None:
        self.sleep(2)
        str_ = """
        <html>
        <style>
        h1 {text-align: center;}
        p {text-align: center;}
        div {text-align: center;}
        </style>
        <h1>Welcome, Miss Li!</h1>
        <p>Your scan authentication has passed. </p>
        <p>Please follow further instruction in the screen to proceed to next step.</p>
        <p>If you have any question, please don't hesitate to contact us.</p>
        <html>"""
        self.authenticatedReceived.emit(True,str_)

    def __del__(self):
        """socket should be free in this step"""
        pass


class WaitForServerScanResultWithQR(QtCore.QThread):
    ScanningDone = QtCore.pyqtSignal(bool,str)
    def __init__(self,parent = None,address = ("",8080),request_msg = None):
        QtCore.QThread.__init__(self,parent)
        self.address = address
        self.to_serer_msg = request_msg

    def run(self) -> None:
        self.sleep(2)
        str_ = """Success."""
        self.ScanningDone.emit(True,str_)

    def __del__(self):
        """socket should be free in this step"""
        pass

def updatePatientInformation(sex,is_new):
    """update this to pass information to backend"""
    pass

def updateLocation(location_list):
    """update this to pass location information to backend"""
    pass

def startTreatment():
    pass

def updateTreatmentApplicator(val_a,val_b):
    pass

def finishTreatment():
    pass