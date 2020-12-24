from PyQt5 import QtWidgets
from PyQt5 import QtCore , QtGui
from AnimationShadowEffect import AnimationShadowEffect
from PreDefineValues import *

class GlowLabel(QtWidgets.QLabel):
    selected = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(GlowLabel, self).__init__(*args, **kwargs)
        self.effect = AnimationShadowEffect(QtGui.QColor(GLOWING_EFFECT_COLOR_R,GLOWING_EFFECT_COLOR_G,GLOWING_EFFECT_COLOR_B),parent=self)
        self.setGraphicsEffect(self.effect)
        self.show()
        self.is_selected = False
        self.setTextColor()
        self.effect.start()
        print(self.objectName())

    def setTextColor(self,color = (80,80,80)):
        self.setStyleSheet(".GlowLabel{\ncolor:rgb(%d,%d,%d);\n}\n"%color)

    def setSelected(self,is_selected):
        selected_color = (15, 220, 232)
        unselected_color = (80,80,80)
        color = None
        if is_selected:
            color = selected_color
            self.effect.stop()
        else:
            color = unselected_color
            self.effect.start()
        self.is_selected = is_selected
        self.setStyleSheet(".GlowLabel{\ncolor:rgb(%d,%d,%d);\n}\n"%color)

    def event(self, e: QtCore.QEvent) -> bool:
        if not self.isEnabled():
            return super(GlowLabel, self).event(e)
        if e.type() == QtCore.QEvent.MouseButtonRelease:
            self.setSelected(not self.is_selected)
            self.selected.emit()
            return False
        return super(GlowLabel, self).event(e)

    def isSelected(self):
        return self.is_selected