from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AnimationShadowEffect(QGraphicsDropShadowEffect):

    def __init__(self, color, *args, **kwargs):
        super(AnimationShadowEffect, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.setOffset(0, 0)
        self.setBlurRadius(0)
        self._radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setDuration(2500)
        self.animation.setLoopCount(-1)
        self.animation.setPropertyName(b'radius')
        self.animation.setStartValue(0)
        self.animation.setEndValue(1000)

        self.animation.setKeyValueAt(0, 0)
        self.animation.setKeyValueAt(0.1, 10 * 4)
        self.animation.setKeyValueAt(0.2, 20 * 4)
        self.animation.setKeyValueAt(0.3, 30 * 4)
        self.animation.setKeyValueAt(0.4, 40 * 4)
        self.animation.setKeyValueAt(0.5, 50 * 4)
        self.animation.setKeyValueAt(0.6, 40 * 4)
        self.animation.setKeyValueAt(0.7, 30 * 4)
        self.animation.setKeyValueAt(0.8, 20 * 4)
        self.animation.setKeyValueAt(0.9, 10)

        self.animation.setKeyValueAt(1, 0)
        self._is_started = False

    def start(self):
        self.animation.start()
        self._is_started = True

    def stop(self, r=0):
        self.animation.stop()
        self.radius = r
        self._is_started = False

    @pyqtProperty(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.setBlurRadius(r)

    def is_started(self):
        return self._is_started
