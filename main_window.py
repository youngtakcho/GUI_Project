from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot
from collections import defaultdict
import sys
from widgets import *

TIMER_INTERVAL_IN_MSEC = 1000
TIMER_START_VALUE = 12*3600+34*60+56

ID_SPLASH_SCREEN = "splash_screen"
ID_LOGIN_SCREEN = "login_screen"
ID_AUTH_SCREEN = "auth_screen"
ID_SCAN_SCREEN = "scan_screen"
ID_PAIT_INFO_SCREEN = "pait_info_screen"
ID_SLCT_TRT_SCREEN = "slct_trt_screen"
ID_POS_SCREEN = "pos_screen"
ID_TIMER_SCREEN = "timer_screen"
ID_SETTING_SCREEN= "setting_screen"
ID_SELECT_LANG_SCREEN = "select_lang_screen"
ID_WIFI_SELECT_SCREEN = "wifi_select_screen"
ID_WIFI_PASSWD_SCREEN = "wifi_passwd_screen"
ID_NET_CNT_SCREEN = "net_cnt_screen"

BottomBar_showing_info   =   [ ## Back , Stop , Next
    (False,False,False),## for "splash_screen"
    (False,False,False),## for "login_screen"
    (False,False,False),## for "auth_screen"
    (False,False,False),## for "scan_screen"
    ( True,False, True),## for "pait_info_screen"
    ( True,False, True),## for "slct_trt_screen"
    ( True,False, True),## for "pos_screen"
    (False, True,False),## for "timer_screen"
    ( True,False,False),## for "setting_screen"
    (False,False,False),## for "select_lang_screen"
    ( True,False,False),## for "wifi_select_screen"
    ( True,False,False),## for "wifi_passwd_screen"
    ( True,False,False),## for "net_cnt_screen"
]


class MainWindow(QtWidgets.QMainWindow):



    def __init__(self):
        super(MainWindow,self).__init__()
        self.screens = {}
        uic.loadUi("main_window.ui",self)
        self.init_screens_dic()
        self.timer_counter = TIMER_START_VALUE # for test
        self.stck_wnd:QtWidgets.QStackedWidget
        self.prog_loading:QtWidgets.QProgressBar
        self.lcd_timer:QtWidgets.QLCDNumber

        self.splash_screen_process()
        self.stck_wnd.setCurrentIndex(0)
        self.stck_wnd.currentChanged.connect(self.page_changed)

        self.prog_loading.setMinimum(0)
        self.prog_loading.setMaximum(100)
        self.prog_loading.setValue(0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animation)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.timer.start(TIMER_INTERVAL_IN_MSEC)
        self.btn_test.released.connect(self.btn_next_released)
        self.btn_test_2.released.connect(self.btn_next_released)

        self.btn_btmbar_next.released.connect(self.btn_next_released)
        self.btn_btmbar_back.released.connect(self.btn_back_released)
        self.btn_btmbar_stop.released.connect(self.btn_stop_timer_released)

        self.btn_female.clicked.connect(self.btn_female_clicked)
        self.btn_male.clicked.connect(self.btn_male_clicked)

        self.btn_yes.released.connect(self.btn_yes_clicked)
        self.btn_no.released.connect(self.btn_no_clicked)

        self.btn_btmbar_next.hide()
        self.btn_btmbar_back.hide()
        self.btn_btmbar_stop.hide()


        self.txt_shoulder.hide()
        self.txt_arm.hide()
        self.txt_thigh.hide()

        self.line_shoulder.hide()
        self.line_arm.hide()
        self.line_thigh.hide()

        self.line_shoulder_pos_l.hide()
        self.line_shoulder_pos_r.hide()
        self.txt_shoulder_pos_r.hide()
        self.txt_shoulder_pos_r.hide()


        self.lcd_timer.display("00:00:00")
        self.slider_a.valueChanged.connect(self.slider_a_changed)
        self.slider_b.valueChanged.connect(self.slider_b_changed)
        self.device_timer = None

        self.btn_setting.released.connect(self.btn_setting_released)



        self.btn_test_male_clicked(True)
        self.btn_test_male_pos_clicked(True)

        self.txtedit_username.focus_in_signal.connect(self.id_lineedit_has_focus)



    def init_screens_dic(self):
        SCREENS = [
            ID_SPLASH_SCREEN,
            ID_LOGIN_SCREEN,
            ID_AUTH_SCREEN,
            ID_SCAN_SCREEN,
            ID_PAIT_INFO_SCREEN,
            ID_SLCT_TRT_SCREEN,
            ID_POS_SCREEN,
            ID_TIMER_SCREEN,
            ID_SETTING_SCREEN,
            ID_SELECT_LANG_SCREEN,
            ID_WIFI_SELECT_SCREEN,
            ID_WIFI_PASSWD_SCREEN,
            ID_NET_CNT_SCREEN
        ]

        counter = 0
        for item in SCREENS:
            self.screens[item] = counter
            counter += 1

    def splash_screen_process(self):
        scene = QtWidgets.QGraphicsScene()
        self.image = QtGui.QPixmap("images/logo2.png")
        self.image = self.image.scaledToWidth(500)
        scene.addPixmap(self.image)
        gv:QtWidgets.QGraphicsView = self.gv_image
        gv.setScene(scene)
        gv.setStyleSheet("background-color: transparent;")
        self.scene = scene
        gv.setRenderHint(QtGui.QPainter.Antialiasing)


    def animation(self):
        self.prog_loading.setValue(self.prog_loading.value()+50)
        if self.prog_loading.value() >= 100:
            self.stck_wnd.setCurrentIndex(1)
            self.btn_login.released.connect(self.btn_login_released)

            self.timer.stop()

    @pyqtSlot()
    def id_lineedit_has_focus(self):
        self.txtedit_username.setStyleSheet("")
        self.txtedit_username.setText("")
        self.txtedit_passwd.setText("")

    @pyqtSlot()
    def btn_login_released(self):
        self.txtedit_username:QtWidgets.QLineEdit

        id = self.txtedit_username.text()
        passwd= self.txtedit_passwd.text()
        print(id,passwd)
        if id == "nintyning":
            self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()-1)
        else:
            self.txtedit_username.setStyleSheet("QLineEdit#txtedit_username{color:rgb(155,0,0);}")
            self.txtedit_username.setText("Incorrect id or Password...")

    @pyqtSlot()
    def btn_back_released(self):
        self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()-1)

    @pyqtSlot()
    def btn_next_released(self):
        self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()+1)


    @pyqtSlot(bool)
    def btn_female_clicked(self,checked):
        if checked is False and self.btn_male.isChecked() is False:
            self.btn_female.setChecked(True)
        self.btn_male.setChecked(False)

    @pyqtSlot(bool)
    def btn_male_clicked(self,checked):
        if checked is False and self.btn_female.isChecked() is False:
            self.btn_male.setChecked(True)
        self.btn_female.setChecked(False)

    @pyqtSlot()
    def btn_yes_clicked(self):
        self.btn_next_released()

    @pyqtSlot()
    def btn_no_clicked(self):
        self.btn_next_released()



    @pyqtSlot()
    def btn_test(self):
        print("test works")

    @pyqtSlot(bool)
    def btn_test_male_clicked(self,clicked):
        if clicked is not True:
            return

        self.scene_male = QtWidgets.QGraphicsScene()
        self.image_male = QtGui.QPixmap("images/male.png")
        self.scene_male.addPixmap(self.image_male)
        self.gv_humanbody.setScene(self.scene_male)
        self.gv_humanbody.setRenderHint(QtGui.QPainter.Antialiasing)

        self.txt_shoulder.show()
        self.txt_arm.show()
        self.txt_thigh.show()
        self.line_shoulder.show()
        self.line_arm.show()
        self.line_thigh.show()


    @pyqtSlot(bool)
    def btn_test_female_clicked(self,clicked):
        if clicked is not True:
            return

        self.scene_female = QtWidgets.QGraphicsScene()
        self.image_female = QtGui.QPixmap("images/female.png")
        self.scene_female.addPixmap(self.image_female)
        self.gv_humanbody.setScene(self.scene_female)
        self.gv_humanbody.setRenderHint(QtGui.QPainter.Antialiasing)
        self.txt_shoulder.show()
        self.txt_arm.show()
        self.txt_thigh.show()
        self.line_shoulder.show()
        self.line_arm.show()
        self.line_thigh.show()

    @pyqtSlot(bool)
    def btn_test_male_pos_clicked(self,clicked):
        if clicked is not True:
            return
        self.scene_male = QtWidgets.QGraphicsScene()
        self.image_male = QtGui.QPixmap("images/male.png")
        self.scene_male.addPixmap(self.image_male)
        self.gv_humanbody_pos.setScene(self.scene_male)
        self.gv_humanbody_pos.setRenderHint(QtGui.QPainter.Antialiasing)

        self.line_shoulder_pos_l.show()
        self.line_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()

    @pyqtSlot(bool)
    def btn_test_female_pos_clicked(self,clicked):
        if clicked is not True:
            return
        self.scene_female = QtWidgets.QGraphicsScene()
        self.image_female = QtGui.QPixmap("images/female.png")
        self.scene_female.addPixmap(self.image_female)
        self.gv_humanbody_pos.setScene(self.scene_female)
        self.gv_humanbody_pos.setRenderHint(QtGui.QPainter.Antialiasing)

        self.line_shoulder_pos_l.show()
        self.line_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()

    @pyqtSlot(int)
    def slider_a_changed(self,value):
        self.txt_app_a_indicator.setText("{value}%".format(value=value))
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.increase_timer)
            self.device_timer.start()

    @pyqtSlot(int)
    def slider_b_changed(self,value):
        self.txt_app_b_indicator.setText("{value}%".format(value=value))
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.increase_timer)
            self.device_timer.start()

    @pyqtSlot(int)
    def page_changed(self,page_number):
        self.bottom_bar_conrtol(page_number)
        if page_number == self.screens[ID_TIMER_SCREEN]:
            self.display_timer()


    def bottom_bar_conrtol(self,page_number):
        if BottomBar_showing_info[page_number][2] is True:
            self.btn_btmbar_next.show()
        else:
            self.btn_btmbar_next.hide()

        if BottomBar_showing_info[page_number][1] is True:
            self.btn_btmbar_stop.show()
        else:
            self.btn_btmbar_stop.hide()

        if BottomBar_showing_info[page_number][0] is True:
            self.btn_btmbar_back.show()
        else:
            self.btn_btmbar_back.hide()



    @pyqtSlot()
    def increase_timer(self):
        self.timer_counter+=1
        self.display_timer()

    @pyqtSlot()
    def btn_stop_timer_released(self):
        if self.device_timer is None:
            return
        self.timer_counter = TIMER_START_VALUE
        self.device_timer.stop()
        self.device_timer = None
        self.display_timer()
        self.slider_a.setValue(0)
        self.slider_b.setValue(0)

    @pyqtSlot()
    def btn_setting_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_SETTING_SCREEN])

    def display_timer(self):
        HH = int(self.timer_counter / 3600)
        MM = int(self.timer_counter % 3600 / 60)
        SS = int(self.timer_counter % 60)
        display_str = "%02d:%02d:%02d"%(HH,MM,SS)
        self.lcd_timer.display(display_str)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

