from PyQt5 import QtCore, QtWidgets, QtGui, uic,Qt
from PyQt5.QtCore import pyqtSlot
import sys
import subprocess
import re
import BackEndCommunicator
from PreDefineValues import *


class MainWindow(QtWidgets.QMainWindow,BackEndCommunicator.BackEndCommunicator):
    screen_changed_stack = []

    def __init__(self):
        super(MainWindow,self).__init__()
        self.screens = {}
        uic.loadUi(STRING_UI_FILE_MAIN_WINDOW, self)
        self.init_screens_dic()
        self.timer_counter = TIMER_START_VALUE # for test
        """register page changing signals"""
        self.stck_wnd.currentChanged.connect(self.page_changed)

        """set frameless window"""
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.init_loading_screen()
        self.init_login_screen()
        self.init_qrcode_screens()
        self.register_bottombar_button_signals()
        self.init_patient_information_screen()
        self.init_select_treatment_area()
        self.init_position_electrodes_screen()
        self.init_timer_screen()
        self.init_setting_pages()

        """test values"""
        self.btn_test_male_clicked(True)
        self.btn_test_male_pos_clicked(True)


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

    def register_bottombar_button_signals(self):
        """register signals for bottom bar buttons"""
        self.btn_btmbar_next.released.connect(self.btn_next_released)
        self.btn_btmbar_back.released.connect(self.btn_back_released)
        self.btn_btmbar_next.hide()
        self.btn_btmbar_back.hide()

    @pyqtSlot()
    def btn_back_released(self):
        print(self.screen_changed_stack.pop(),self.screens)
        self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()-1)

    @pyqtSlot()
    def btn_next_released(self):
        self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()+1)


    #for login screen
    def init_login_screen(self):
        self.btn_login.released.connect(self.btn_login_released)
        self.txtedit_username.focus_in_signal.connect(self.id_lineedit_has_focus)

    @pyqtSlot()
    def btn_login_released(self):
        self.txtedit_username:QtWidgets.QLineEdit

        id = self.txtedit_username.text()
        passwd= self.txtedit_passwd.text()
        if id == "nintyning":
            self.stck_wnd.setCurrentIndex(self.stck_wnd.currentIndex()+1)
        else:
            self.show_login_fail_dialog()
        # self.txtedit_username.setStyleSheet("QLineEdit#txtedit_username{color:rgb(155,0,0);}")
        # self.txtedit_username.setText("Incorrect id or Password...")

    @pyqtSlot()
    def id_lineedit_has_focus(self):
        self.txtedit_username.setText("")
        self.txtedit_passwd.setText("")

    def show_login_fail_dialog(self):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.setModal(True);
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        w = self.geometry().width()
        h = self.geometry().height()
        dw = dialog.geometry().width()
        dh = dialog.geometry().height()
        rw = w/2 - dw/2
        rh = h/2 - dh/2 -5
        dialog.setGeometry(rw,rh,dialog.width(),dialog.height())
        dialog.exec()

    def init_loading_screen(self):
        """loading screen"""
        self.splash_screen_process()
        self.stck_wnd.setCurrentIndex(0)
        self.prog_loading.setMinimum(0)
        self.prog_loading.setMaximum(100)
        self.prog_loading.setValue(0)
        self.test_loading_screen()

    def test_loading_screen(self):
        """ for test loading screen """
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animation)
        self.timer.start(TIMER_INTERVAL_IN_MSEC)

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
        self.prog_loading.setValue(self.prog_loading.value()+20)
        if self.prog_loading.value() >= 100:
            self.stck_wnd.setCurrentIndex(1)
            self.timer.stop()

    # for auth qrcode screen
    def init_qrcode_screens(self):
        """set test button for QRcode screens"""
        self.btn_test.released.connect(self.btn_next_released)
        self.btn_test_2.released.connect(self.btn_next_released)

    # for patient infomation screen
    def init_patient_information_screen(self):
        """register button signals for patient information screen"""
        self.btn_female.clicked.connect(self.btn_female_clicked)
        self.btn_male.clicked.connect(self.btn_male_clicked)
        self.btn_yes.released.connect(self.btn_yes_clicked)
        self.btn_no.released.connect(self.btn_no_clicked)


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

    # for select treatment screen
    def init_select_treatment_area(self):
        """for Select Treatment Area screen"""
        self.txt_shoulder.hide()
        self.txt_arm.hide()
        self.txt_thigh.hide()
        self.line_shoulder.hide()
        self.line_arm.hide()
        self.line_thigh.hide()

    # for position electrodes screen
    def init_position_electrodes_screen(self):
        """for Position Electrodes screen"""
        self.line_shoulder_pos_l.hide()
        self.line_shoulder_pos_r.hide()
        self.txt_shoulder_pos_r.hide()
        self.txt_shoulder_pos_r.hide()

    # for timer screen
    def init_timer_screen(self):
        """for Timer Screen"""
        self.btn_timer_stop.released.connect(self.btn_stop_timer_released)
        self.btn_timer_stop.hide()
        self.lcd_timer.display("00:00:00")
        self.slider_a.valueChanged.connect(self.slider_a_changed)
        self.slider_b.valueChanged.connect(self.slider_b_changed)
        self.device_timer = None  # timer is killed initially

    @pyqtSlot(int)
    def slider_a_changed(self,value):
        self.txt_app_a_indicator.setText(STRING_APPLICATOR_VALUE_FORMAT.format(value=value))
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.timer_process)
            self.device_timer.start()

    @pyqtSlot(int)
    def slider_b_changed(self,value):
        self.txt_app_b_indicator.setText(STRING_APPLICATOR_VALUE_FORMAT.format(value=value))
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.timer_process)
            self.device_timer.start()

    @pyqtSlot()
    def timer_process(self):
        self.timer_counter -= 1
        if self.timer_counter <= 0:
            #add designed dialog when dialog design is complite
            self.show_dialog_with_message("Treatment is done go to Scan screen.")
            self.stck_wnd.setCurrentIndex(self.screens[ID_SCAN_SCREEN])
            self.btn_stop_timer_released()
        self.display_timer()

    def display_timer(self):
        HH = int(self.timer_counter / 3600)
        MM = int(self.timer_counter % 3600 / 60)
        SS = int(self.timer_counter % 60)
        display_str = STRING_TIMER_NUMBER_FORMAT%(HH,MM,SS)
        self.lcd_timer.display(display_str)

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


    # for general control for screens
    @pyqtSlot(int)
    def page_changed(self,page_number):
        self.screen_changed_stack.append(page_number)
        self.bottom_bar_conrtol(page_number)
        if page_number == self.screens[ID_TIMER_SCREEN]:
            self.display_timer()

    def bottom_bar_conrtol(self,page_number):
        if BottomBar_showing_info[page_number][ID_BTN_BOTTOM_BAR_NEXT] is True:
            self.btn_btmbar_next.show()
        else:
            self.btn_btmbar_next.hide()

        if BottomBar_showing_info[page_number][ID_BTN_BOTTOM_BAR_BACK] is True:
            self.btn_btmbar_back.show()
        else:
            self.btn_btmbar_back.hide()

    # for setting pages
    def init_setting_pages(self):
        """for setting pages"""
        self.btn_setting.released.connect(self.btn_setting_released)
        self.btn_advanced_services.released.connect(self.btn_advanced_services_released)
        self.btn_restore_default.released.connect(self.btn_restore_default_released)
        self.btn_language.released.connect(self.btn_language_released)
        self.btn_internet.released.connect(self.btn_internet_released)
        self.btn_internet.released.connect(self.btn_internet_released)
        self.btn_system_info.released.connect(self.btn_system_info_released)
        self.btn_others.released.connect(self.btn_others_released)

        self.btn_ok_language.released.connect(self.btn_ok_language_released)

        self.btn_wifi_search.released.connect(self.btn_wifi_search_released)
        self.wifi_listWidget:QtWidgets.QListWidget
        self.wifi_listWidget.itemClicked.connect(self.wifi_listWidget_item_clicked)

        self.btn_ok_wifi_passwd.released.connect(self.btn_ok_wifi_passwd_released)
        self.btn_net_conn_ok.released.connect(self.btn_net_conn_ok_released)

    @pyqtSlot()
    def btn_setting_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_SETTING_SCREEN])

    @pyqtSlot()
    def btn_others_released(self):
        print("Not implemented")

    @pyqtSlot()
    def btn_system_info_released(self):
        print("Not implemented")

    @pyqtSlot()
    def btn_internet_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_WIFI_SELECT_SCREEN])

    @pyqtSlot()
    def btn_language_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_SELECT_LANG_SCREEN])

    @pyqtSlot()
    def btn_restore_default_released(self):
        print("Not implemented")

    @pyqtSlot()
    def btn_advanced_services_released(self):
        print("Not implemented")

    @pyqtSlot()
    def btn_net_conn_ok_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_SETTING_SCREEN])

    @pyqtSlot()
    def btn_ok_wifi_passwd_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_NET_CNT_SCREEN])

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def wifi_listWidget_item_clicked(self,item:QtWidgets.QListWidgetItem):
        print(item.text())
        self.stck_wnd.setCurrentIndex(self.screens[ID_WIFI_PASSWD_SCREEN])

    @pyqtSlot()
    def btn_wifi_search_released(self):
        self.search_wifi()
        # self.stck_wnd.setCurrentIndex(self.screens[ID_WIFI_PASSWD_SCREEN])

    @pyqtSlot()
    def btn_ok_language_released(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_SETTING_SCREEN])



    def search_wifi(self): #function to search and display all the available Wifi networks
        self.wifi_listWidget.clear()
        devices = subprocess.check_output(['netsh','wlan','show','network'])
        devices = devices.decode()
        devices= devices.replace("\r","")

        ls = devices.split("\n")
        ls = ls[4:]

        ssid = []
        x = 0
        y = 0
        while x < len(ls):
            if x % 5 == 0:
                ssid.append(ls[x])
            x += 1
        for line in ssid:
            y = re.findall('^SSID [0-9]* : (.+)', line)
            if len(y) > 0:
                # print("".join(y))
                self.wifi_listWidget.addItem("".join(y))


# dialog for general message
    def show_dialog_with_message(self,msg):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        dialog.setText(msg)
        dialog.setWindowTitle("Information")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w = self.geometry().width()
        h = self.geometry().height()
        dw = dialog.geometry().width()
        dh = dialog.geometry().height()
        rw = w/2 - dw/2
        rh = h/2 - dh/2 -5
        dialog.setGeometry(rw,rh,dialog.width(),dialog.height())
        dialog.exec()

# for test will be removed
#     @pyqtSlot(bool)
    def btn_test_male_clicked(self,clicked):
        if clicked is not True:
            return
        self.scene_male = QtWidgets.QGraphicsScene()
        self.image_male = QtGui.QPixmap(IMAGE_FOR_MALE)
        self.scene_male.addPixmap(self.image_male)
        self.gv_humanbody.setScene(self.scene_male)
        self.gv_humanbody.setRenderHint(QtGui.QPainter.Antialiasing)

        self.txt_shoulder.show()
        self.txt_arm.show()
        self.txt_thigh.show()
        self.line_shoulder.show()
        self.line_arm.show()
        self.line_thigh.show()

    # @pyqtSlot(bool)
    # def btn_test_female_clicked(self,clicked):
    #     if clicked is not True:
    #         return
    #
    #     self.scene_female = QtWidgets.QGraphicsScene()
    #     self.image_female = QtGui.QPixmap(IMAGE_FOR_FEMALE)
    #     self.scene_female.addPixmap(self.image_female)
    #     self.gv_humanbody.setScene(self.scene_female)
    #     self.gv_humanbody.setRenderHint(QtGui.QPainter.Antialiasing)
    #     self.txt_shoulder.show()
    #     self.txt_arm.show()
    #     self.txt_thigh.show()
    #     self.line_shoulder.show()
    #     self.line_arm.show()
    #     self.line_thigh.show()
    #
    # @pyqtSlot(bool)
    def btn_test_male_pos_clicked(self,clicked):
        if clicked is not True:
            return
        self.scene_male = QtWidgets.QGraphicsScene()
        self.image_male = QtGui.QPixmap(IMAGE_FOR_MALE)
        self.scene_male.addPixmap(self.image_male)
        self.gv_humanbody_pos.setScene(self.scene_male)
        self.gv_humanbody_pos.setRenderHint(QtGui.QPainter.Antialiasing)

        self.line_shoulder_pos_l.show()
        self.line_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()
    #
    # @pyqtSlot(bool)
    # def btn_test_female_pos_clicked(self,clicked):
    #     if clicked is not True:
    #         return
    #     self.scene_female = QtWidgets.QGraphicsScene()
    #     self.image_female = QtGui.QPixmap(IMAGE_FOR_FEMALE)
    #     self.scene_female.addPixmap(self.image_female)
    #     self.gv_humanbody_pos.setScene(self.scene_female)
    #     self.gv_humanbody_pos.setRenderHint(QtGui.QPainter.Antialiasing)
    #
    #     self.line_shoulder_pos_l.show()
    #     self.line_shoulder_pos_r.show()
    #     self.txt_shoulder_pos_r.show()
    #     self.txt_shoulder_pos_r.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.showFullScreen()
    window.show()
    app.exec_()

