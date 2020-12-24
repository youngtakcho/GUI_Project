from PyQt5 import QtCore
from numpy import ndarray
from PreDefineValues import ID_QR_CODE_AUTH, ID_QR_CODE_DOWNLOAD, ID_QR_CODE_SCAN
import os

""" Do not change this thread WifiAttemptThread"""


class WifiAttemptThread(QtCore.QThread):
    wifi_result_temp = QtCore.pyqtSignal(bool, str)

    def __init__(self, SSID, key, parent=None, address=("", 8080)):
        QtCore.QThread.__init__(self, parent)
        self.address = address
        self.SSID = SSID
        self.key = key

    def run(self) -> None:
        self.sleep(3)
        command = "nmcli dev wifi connect '" + self.SSID + "' password '" + self.key + "'"
        os.system(command)
        self.wifi_result_temp.emit(True, "Incorrect Credentials")

    def __del__(self):
        """socket should be free in this step"""
        pass


""" Do not change this thread WifiAttemptThread"""


class LoadingProcess(QtCore.QThread):
    loadingPrograssUpdated = QtCore.pyqtSignal(int)
    loadingFinished = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent=parent)

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

    def __init__(self, parent=None, address=("", 8080), id_pass=(None, None)):
        QtCore.QThread.__init__(self, parent)
        self.address = address
        self.id = id_pass[0]
        self.passwd = id_pass[1]

    def run(self) -> None:
        self.sleep(1)
        if self.id != "test":
            self.login_result.emit(False, "id is not correct")
        else:
            self.login_result.emit(True, "success")

    def __del__(self):
        """socket should be free in this step"""
        pass


class RequestQrCodeImage(QtCore.QThread):
    imageReceived = QtCore.pyqtSignal(bool, int, ndarray)

    def __init__(self, parent=None, address=("", 8080), request_msg=None, qr_type=ID_QR_CODE_AUTH):
        QtCore.QThread.__init__(self, parent)
        self.address = address
        self.to_serer_msg = request_msg
        self.qr_type = qr_type

    def run(self) -> None:
        self.sleep(1)
        fortest = ndarray((0, 0, 0))
        self.imageReceived.emit(True, self.qr_type, fortest)

    def __del__(self):
        """socket should be free in this step"""
        pass


class WaitForServerAuthWithQR(QtCore.QThread):
    authenticatedReceived = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None, address=("", 8080), request_msg=None):
        QtCore.QThread.__init__(self, parent)
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
        <p>
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFoElEQVR4Xu2bW2wUVRjHt9t2Zs7srERjYgkxRkNIgyYmXrioL75UBWKQQivQQgsaL1XQFgRaoC1QNaS0paU1qEADdLdu6UrQBx5sQktBEI1PalC8xXgJiYlCjDEK+H2l0eXf3c6ZObO00+wv+Yd2O+f/nW/m7LkOgUCGDBkyZEgvWVlZd046d6WH9L6kYsFgcDr6+BYrdiJCSV1xIqv31AH08S1mc9dJTNBOoZ3dA+jjW0RN84+YoJ3E5tbv0Mev5FrR/kuYoJ2s7uN/U9kgmvkO6szuwORklZ2dPQX9fAfdgIcxMVlR2dno5zsoiTJMTFY0fBah35hCTXKyte/oEWP5qg5K7G78O0LXzNTnLDqOicmK4u0hmxvQF6E404yy1e36opVR+tXEv3uGvviZzsQKmi2RQQq+mP6kJV5HT+4+s6P3A0zIjcLvnrkgKjY2BJLcCIozW1+wLJ7YyRprXq3G6zyBgs2yIsdGVJAlqnf8YrywaStdM9VYUbnTivRfxmtUJWqafqKbPZfrQv8+TvOEpC3Lip++SC0nD+uvjNl08EMMdr3FD2Ba494Rn6P0kuffwvorQXe8GIOMZ3ELpDrfg3m4xRSbWn7AIONdpldTaWN1fS2a+0XUChZgPo4ggynWoVN/oLFfJGrbvqU0DMxLGn3Js/vQVFViQ+N56qn3a5q2hkaNpSz6eS0vf8X6xvN4varE2tc2YF5SUMVmUK/r2XBmbun4klqU3cwulztcs779KyzvVlb8I3fDYqpx1o30FZUtZKljjFEwjPKXW9HHrfTSit0YwBZej6ORG9ETrUJvWajsK+jnRua23V+gty05OTk36fNLj6CZEw0/eSWM8pfa0NeJRO2ub+grMBN9peGnYHUP/IPGdqLv/NmAs2afCsOsaz+H/jLiTjyQZA3hGLoJD4WPfuZoW0uiw5OGF1zoP5rChz/+bXiR5h3UjG7R5hX3YbBk4qEOyyuiiXXbf8U4yaQ9tpBXqLehgWeYr+/9FIOieJzHcqpYsUHbrXVx9WuXXswtb5zFwCie5GA5VfLy8uowDoomPRewnOeIym1/YWAUz+6wnCoFBQW2N4DWLZexnOek2hQZDzdAVDX8ieU85+aaxhGBUTy3x3KqyHwFaMLzOZbznLvaDo4IjErHuZ71jn0naG7v/ATLeQYNLbdrjxZKbYvxqo6K5KKHAvLD4NziPh6y0UAJSr6Ud2cx2GjiVR36uIW8lqD/aOJJG0/e0McNk/Qnn96PAWTES9qAN1NhYdbt+hr97cTTd2o169BMGmpGD6iuCHlJi75OMZavakdfJ9Lnl7xHC7sb0dcWs77Dk00JXkyhtyw0nK5HPzfSi1ZG0NsWvaTiTTRyK17SBpztzQnVJ5+o0IG+Xgxgy9A5YPz0RTRzK17SDq/QrjlGAzTu8ISL73wq8RkBtaR7MZAURlVDDRqqioczXtjwxIZndyz+mcd52aHOifSlz72NeTnBUO0Ix1JW79A54WRMyhHUJAvR2C/iFoz5uMJsiXq2Q3y9NPySlZOONzV83p+OI+90ilruQsxDCe5MMAgqv7lz6AgbP/dK7J3f1Dnic1SoJTqI9VdmaFjsTT4shtpix4L/v7wwh19mwGtURU36e/J+ZDjGvFBrrB+vYfFpFrfYa2vvEaKyYeN/gaIDl/TC8h6qzP14HREWL27eGj585nesoFOJ6h0/B68erggMQp/P0AvLDiW+IkMtld8rShshveipLprZtQbldl7DdN0eTEpW1Or4SMt2QUUxpvJsU3tiWdzzpbAqVCFHe/qJGnevybmBns6DmJisqOws9PMdlMStmJisJsSrskS2m7PFCfOyNOPmJauJ9Lp8wGyOnMAE7TSh/sOE1XOyCxO0Uzq21scM6ginU1LdJH7hQkZRKpOPPhkyZMiQwWP+BaMgm4DVIMspAAAAAElFTkSuQmCC">
        </p>
        <h1>Welcome, Miss Li!</h1>
        <p>Your scan authentication has passed. </p>
        <p>Please follow further instruction in the screen to proceed to next step.</p>
        <p>If you have any question, please don't hesitate to contact us.</p>
        <html>"""
        self.authenticatedReceived.emit(True, str_)

    def __del__(self):
        """socket should be free in this step"""
        pass


class WaitForServerScanResultWithQR(QtCore.QThread):
    ScanningDone = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None, address=("", 8080), request_msg=None):
        QtCore.QThread.__init__(self, parent)
        self.address = address
        self.to_serer_msg = request_msg

    def run(self) -> None:
        self.sleep(2)
        str_ = """Success."""
        self.ScanningDone.emit(True, str_)

    def __del__(self):
        """socket should be free in this step"""
        pass


class WaitHardwarePreparation(QtCore.QThread):
    hardware_msg_received = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent=None, address=("", 8080), request_msg=None):
        QtCore.QThread.__init__(self, parent)
        self.address = address
        self.to_serer_msg = request_msg

    def run(self) -> None:
        self.sleep(2)
        str_ = """Fail to init"""
        self.hardware_msg_received.emit(True,str_)

    def __del__(self):
        """socket should be free in this step"""
        pass

def updatePatientInformation(sex, is_new):
    """update this to pass information to backend"""
    pass


def updateLocation(location_list):
    """update this to pass location information to backend"""
    pass


def startTreatment():
    pass


def updateTreatmentApplicator(val_a, val_b):
    pass


def finishTreatment():
    pass
