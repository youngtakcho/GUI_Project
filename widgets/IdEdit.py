from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit

class IdEdit(QLineEdit):
    focus_in_signal = QtCore.pyqtSignal()
    focus_out_signal = QtCore.pyqtSignal()

    def focusInEvent(self, event):
        self.focus_in_signal.emit()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focus_out_signal.emit()