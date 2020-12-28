from PyQt5 import QtCore, QtWidgets, QtGui, uic,Qt
from PyQt5.QtCore import pyqtSlot
import sys
import subprocess
import re
from PreDefineValues import *
import os
import platform
import time
import socket
from widgets.loadingdialogwithmessage import LoadingDialogWithMessage
from widgets.wifiloadingdialogmsg import WifiLoadingDialogWithMessage
from widgets.loadingdialogwithmessage_login import LoadingDialogWithMessage_login
from widgets.loadingdialogwithmessage_server import LoadingDialogWithMessage_server
from widgets.loadingdialogwithmessage_qr import LoadingDialogWithMessage_qr
from AnimationShadowEffect import AnimationShadowEffect

from numpy import ndarray
import numpy as np
from backend import *

class MainWindow(QtWidgets.QMainWindow):
    screen_changed_stack = []

    def __init__(self):
        super(MainWindow,self).__init__()
        self.screens = {}
        uic.loadUi(STRING_UI_FILE_MAIN_WINDOW, self)
        self.init_screens_dic()
        self.trans = QtCore.QTranslator(self)
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
        # self.init_position_electrodes_screen()
        self.init_timer_screen()
        self.init_setting_pages()

        self.btn_female_clicked(True)
        """test values"""
        self.set_graphic(self.selected_sex)
        # self.btn_test_male_pos_clicked(True)
        self.qr_dic = {}
        
        options = ([('English', 'eng-eng'), ('Español','eng-esp'), ('Netherlands','eng-dut'), ('Italiano','eng-ita'), ('français', 'eng-fr' ), ('中文', 'eng-chs'), ('日本人','eng-jap'), ('한국어','eng-kor'), ])
        for i, (text, lang) in enumerate(options):
            self.lang_combo.addItem(text)
            self.lang_combo.setItemData(i, lang)
        self.retranslateUi()

        self.lang_combo.currentIndexChanged.connect(self.change_func)
        self.langfile = 'eng-eng'

    def init_screens_dic(self):
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
        self.screen_changed_stack.pop()
        move_to = self.screen_changed_stack.pop()
        self.stck_wnd.setCurrentIndex(move_to)

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
        self.txtedit_username:QtWidgets.QLineEdit

        id = self.txtedit_username.text()
        passwd= self.txtedit_passwd.text()

        loginthread = LoginAttemptThread(self,id_pass=(id,passwd))
        loginthread.login_result.connect(self.login_results)
        loginthread.start()
        self.show_loading_dialog_with_message_login(STRING_LOGIN_ON_PROCESSING)

    @pyqtSlot(bool,str)
    def login_results(self,is_success,msg_from_server):
        print(msg_from_server)
        self.close_current_dialog()
        self.show_login_result_dialog(is_success)
        if is_success:
            thread = RequestQrCodeImage(self, address=("", 8080), request_msg="request=QR_AUTH")
            thread.imageReceived.connect(self.auth_qrcode_received)
            thread.start()
            self.show_loading_dialog_with_message_server(STRING_RECEIVING_FROM_SERVER)

    @pyqtSlot()
    def id_lineedit_has_focus(self):
        self.txtedit_username.setText("")
        self.txtedit_passwd.setText("")

    def show_login_result_dialog(self,result = False):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        if result:
            dialog.txt_msg.setText(QtWidgets.QApplication.translate('login-success','\nLogin Success!\n'))
            dialog.btn_ok.setText(QtWidgets.QApplication.translate('login-success','OK'))
        else:
            dialog.txt_msg.setText(QtWidgets.QApplication.translate('login-fail','\nId or password is incorrect    \nPlease Check\n'))
            dialog.btn_ok.setText(QtWidgets.QApplication.translate('login-success','OK'))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()

    def init_loading_screen(self):
        """loading screen"""
        self.splash_screen_process()
        self.stck_wnd.setCurrentIndex(0)
        self.prog_loading.setMinimum(0)
        self.prog_loading.setMaximum(100)
        self.prog_loading.setValue(0)
        loading_thread = LoadingProcess(self)
        loading_thread.loadingPrograssUpdated.connect(self.loading_update)
        loading_thread.loadingFinished.connect(self.loading_finished)
        loading_thread.start()

    def splash_screen_process(self):
        scene = QtWidgets.QGraphicsScene()
        self.image = QtGui.QPixmap("images/logo2.png")
        self.image = self.image.scaledToWidth(500)
        scene.addPixmap(self.image)
        gv = self.gv_image
        gv.setScene(scene)
        gv.setStyleSheet("background-color: transparent;")
        self.scene = scene
        gv.setRenderHint(QtGui.QPainter.Antialiasing)

    @pyqtSlot(int)
    def loading_update(self,progress):
        self.prog_loading.setValue(progress)

    @pyqtSlot()
    def loading_finished(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_LOGIN_SCREEN])

    # for auth qrcode screen
    def init_qrcode_screens(self):
        """set test button for QRcode screens"""
        # self.scan_auth_btn_test.released.connect(self.btn_next_released)
        # self.scan_check_btn_test.released.connect(self.btn_next_released)

    @pyqtSlot(bool,int,ndarray)
    def auth_qrcode_received(self,is_success,qrcode_id,image):
        if is_success and image is not None:
            self.qr_dic[qrcode_id] = np.transpose(image,(1,0,2)).copy()
            self.close_current_dialog()
            self.btn_next_released()
            thread = WaitForServerAuthWithQR(self)
            thread.authenticatedReceived.connect(self.authenticated_received_from_server)
            thread.start()
        else:
            self.close_current_dialog()
            self.show_dialog_with_message_qr_msg(STRING_ERROR_RECEIVING_QRCODE)
            self.reset_values()
            self.go_to_start_screen()

    def goto_AuthScreen(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_AUTH_SCREEN])
        thread = WaitForServerAuthWithQR(self)
        thread.authenticatedReceived.connect(self.authenticated_received_from_server)
        thread.start()

    @pyqtSlot(bool,str)
    def authenticated_received_from_server(self,result,html):
        if self.dialog_on_screen is not None:
            self.dialog_on_screen.close()
        if result:
            # QtCore.QTimer.singleShot(SEC_AUTO_DIALOG_CLOSE,self.close_dialog_go_next)
            QtCore.QTimer.singleShot(SEC_AUTO_DIALOG_CLOSE,self.ready_for_hardware)
            self.show_dialog_with_html_message(html)
        else:
            self.show_dialog_with_message_unk_error(UNKNOWN_ERROR)
            self.reset_values()
            QtCore.QTimer.singleShot(SEC_AUTO_DIALOG_CLOSE,self.go_to_start_screen)

    def ready_for_hardware(self):
        self.close_current_dialog()
        t = WaitHardwarePreparation(parent=self)
        t.hardware_msg_received.connect(self.hardware_msg_received)
        t.start()
        self.show_loading_dialog_with_message("""Treatment will be started.\nPlease wait for Hardware to be ready""")

    def close_dialog_go_next(self):
        self.dialog_on_screen.close()
        self.btn_next_released()

    def request_scan_qr_code(self):
        self.dialog_on_screen.close()
        thread = RequestQrCodeImage(self)
        thread.imageReceived.connect(self.scan_qrcode_received)
        thread.start()
        self.show_loading_dialog_with_message_qr(STRING_RECV_QR_SCAN_FROM_SERVER)

    @pyqtSlot(bool,int,ndarray)
    def scan_qrcode_received(self,is_success,qrcode_id,image):
        if is_success and image is not None:
            self.qr_dic[qrcode_id] = np.transpose(image,(1,0,2)).copy()
            self.close_current_dialog()
            self.btn_next_released()
            thread = WaitForServerScanResultWithQR(self)
            thread.ScanningDone.connect(self.scan_done)
            thread.start()
        else:
            self.close_current_dialog()
            self.show_dialog_with_message_qr_msg(STRING_ERROR_RECEIVING_QRCODE)
            self.reset_values()
            self.go_to_start_screen()

    @pyqtSlot(bool,str)
    def scan_done(self,is_success,msg):
        print(msg)
        if is_success:
            self.show_dialog_with_message_qr_success(STRING_SCAN_QRCODE_SUCCESS)
            self.btn_next_released()
        else:
            self.show_dialog_with_message_qr_fail(STRING_SCAN_QRCODE_FAIL)

    def close_dialog_and_proceed_next(self):
        self.dialog_on_screen.close()
        self.btn_next_released()

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
        self.selected_sex = SEX.FEMALE

    @pyqtSlot(bool)
    def btn_male_clicked(self,checked):
        if checked is False and self.btn_female.isChecked() is False:
            self.btn_male.setChecked(True)
        self.btn_female.setChecked(False)
        self.selected_sex = SEX.MALE

    @pyqtSlot()
    def btn_yes_clicked(self):
        if self.selected_sex is None:
            return
        self.set_graphic(self.selected_sex)
        updatePatientInformation(self.selected_sex, True)
        self.btn_next_released()

    @pyqtSlot()
    def btn_no_clicked(self):
        if self.selected_sex is None:
            return
        self.set_graphic(self.selected_sex)
        updatePatientInformation(self.selected_sex, True)
        self.btn_next_released()

    # for select treatment screen
    def init_select_treatment_area(self):
        """for Select Treatment Area screen"""
        self.txt_shoulder_L.hide()
        self.txt_shoulder_R.hide()
        self.txt_arm_L.hide()
        self.txt_thigh_L.hide()
        self.txt_arm_R.hide()
        self.txt_thigh_R.hide()
        self.line_shoulder_R.hide()
        self.line_shoulder_L.hide()
        self.line_arm_L.hide()
        self.line_thigh_L.hide()
        self.line_arm_R.hide()
        self.line_thigh_R.hide()
        self.txt_label_list = [self.txt_shoulder_L,self.txt_shoulder_R,self.txt_arm_L,self.txt_arm_R,self.txt_thigh_L,self.txt_thigh_R]
        for label in self.txt_label_list:
            label.selected.connect(self.check_select_limit)

    def check_select_limit(self):
        count = 0
        for label in self.txt_label_list:
            if label.isSelected():
                count += 1
        if count >= 2:
            for label in self.txt_label_list:
                if not label.isSelected():
                    label.setEnabled(False)
                else:
                    label.setEnabled(True)
        else:
            for label in self.txt_label_list:
                label.setEnabled(True)

    # for position electrodes screen
    def init_position_electrodes_screen(self):
        """for Position Electrodes screen"""
        pos_frame_list = [self.line_shoulder_pos_l,self.line_shoulder_pos_r,self.frame_arm_L_2,self.frame_arm_R_2,self.frame_thigh_L_2,self.frame_thigh_R_2]
        pos_label_list = [self.txt_shoulder_pos_l,self.txt_shoulder_pos_r,self.txt_arm_L_2,self.txt_arm_R_2,self.txt_thigh_L_2,self.txt_thigh_R_2]
        list_area = []
        for i in range(0,len(self.txt_label_list)):
            pos_label_list[i].setSelected(True)
            if self.txt_label_list[i].isSelected():
                pos_frame_list[i].show()
                list_area.append(i)
            else:
                pos_frame_list[i].hide()
        updateLocation(list_area)


    # for timer screen
    def init_timer_screen(self):
        """for Timer Screen"""
        self.btn_timer_stop.released.connect(self.btn_stop_timer_released)
        # self.btn_timer_stop.hide()
        self.lcd_timer.display("00:00:00")
        self.slider_a.valueChanged.connect(self.slider_a_changed)
        self.slider_b.valueChanged.connect(self.slider_b_changed)
        self.device_timer = None  # timer is killed initially
        self.btn_timer_lock.released.connect(self.btn_timer_lock_released)

    @pyqtSlot(int)
    def slider_a_changed(self,value):
        self.txt_app_a_indicator.setText(STRING_APPLICATOR_VALUE_FORMAT.format(value=value))
        value_b = self.slider_b.value()
        updateTreatmentApplicator(value, value_b)
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.timer_process)
            self.device_timer.start()
            startTreatment()

    @pyqtSlot(int)
    def slider_b_changed(self,value):
        self.txt_app_b_indicator.setText(STRING_APPLICATOR_VALUE_FORMAT.format(value=value))
        value_a = self.slider_a.value()
        updateTreatmentApplicator(value_a, value)
        if self.device_timer is None and value != 0:
            self.device_timer = QtCore.QTimer()
            self.device_timer.setInterval(TIMER_INTERVAL_IN_MSEC)
            self.device_timer.timeout.connect(self.timer_process)
            self.device_timer.start()
            startTreatment()

    @pyqtSlot()
    def timer_process(self):
        self.timer_counter -= 1
        if self.timer_counter <= 0:
            #add designed dialog when dialog design is complite
            self.show_dialog_with_message_trmt_done(STRING_TREATMENT_DONE)
            if not self.btn_timer_stop.isEnabled():
                self.set_lock_gui_btns_timer(False)
            self.goto_AuthScreen()
            self.btn_stop_timer_released()
            finishTreatment()
        self.display_timer()


    @pyqtSlot()
    def btn_timer_lock_released(self):
        self.set_lock_gui_btns_timer(self.btn_timer_stop.isEnabled())

    def set_lock_gui_btns_timer(self,is_lock):
        if is_lock:
            self.btn_timer_stop.setEnabled(False)
            self.slider_b.setEnabled(False)
            self.slider_a.setEnabled(False)
        else:
            self.btn_timer_stop.setEnabled(True)
            self.slider_b.setEnabled(True)
            self.slider_a.setEnabled(True)

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
        self.bottom_bar_conrtol(page_number)
        # if page_number > self.screens[ID_SETTING_SCREEN]:
        #     return
        # if len(self.screen_changed_stack) > 0 and page_number == self.screen_changed_stack[-1]:
        #     return
        self.screen_changed_stack.append(page_number)
        if page_number == self.screens[ID_TIMER_SCREEN]:
            self.display_timer()
            # t = WaitHardwarePreparation(parent=self)
            # t.hardware_msg_received.connect(self.hardware_msg_received)
            # t.start()
            # self.show_loading_dialog_with_message("""Treatment will be started.\nPlease wait for Hardware to be ready""")
        elif page_number == self.screens[ID_POS_SCREEN]:
            self.init_position_electrodes_screen()
        # elif page_number == self.screens[ID_PAIT_INFO_SCREEN]:
        #     t = WaitHardwarePreparation(parent=self)
        #     t.hardware_msg_received.connect(self.hardware_msg_received)
        #     t.start()
        #     self.show_loading_dialog_with_message("""Treatment will be started.\nPlease wait for Hardware to be ready""")

    @pyqtSlot(bool,str)
    def hardware_msg_received(self, is_ready, msg):
        print(msg)
        self.close_current_dialog()
        if is_ready:
            self.show_dialog_with_message("Hardware is ready!")
            self.btn_next_released()
        else:
            self.show_dialog_with_message("Hardware Error\nGo to Authentication Screen")
            self.goto_AuthScreen()



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
        self.stck_wnd.setCurrentIndex(self.screens[ID_LOGIN_SCREEN])

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
        self.wifi_pass_lineEdit:QtWidgets.QLineEdit
        #self.wifi_status_label.setText("Connecting")
        self.wifi_password = self.wifi_pass_lineEdit.text()
        #self.show_connecting_dialog()

        wifithread = WifiAttemptThread(self.wifi_username,self.wifi_password)
        wifithread.wifi_result_temp.connect(self.wifi_results)
        wifithread.start()
        self.show_wifi_loading_dialog_with_message(STRING_WIFI_CONN_ON_PROCESSING)
        #self.show_wifi_result_dialog()
        #self.createNewConnection(self.wifi_username, self.wifi_username, self.wifi_password)
        try:
            socket.create_connection(("1.1.1.1", 53))
            wifi_status = True
        except Exception as e:
            wifi_status = False

        if wifi_status == True:
            self.stck_wnd.setCurrentIndex(self.screens[ID_NET_CNT_SCREEN])
            #dialog.txt_msg.setText(STRING_WIFI_CONN_SUCCESS)
        else:
            self.show_net_fail_dialog()
            #dialog.txt_msg.setText(STRING_WIFI_CONN_FAIL)
            self.wifi_status_label.setText("")

    @pyqtSlot(bool,str)
    def wifi_results(self):
        self.close_current_dialog()
        self.show_wifi_result_dialog()

    def show_wifi_result_dialog(self):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_NET_FAIL,dialog)
        #self.createNewConnection(self.wifi_username, self.wifi_username, self.wifi_password)
        try:
            socket.create_connection(("1.1.1.1", 53))
            wifi_status = True
        except Exception as e:
            wifi_status = False

        if wifi_status == True:
            #self.stck_wnd.setCurrentIndex(self.screens[ID_NET_CNT_SCREEN])
            dialog.txt_msg.setText(STRING_WIFI_CONN_SUCCESS)
        else:
            #self.show_net_fail_dialog()
            dialog.txt_msg.setText(STRING_WIFI_CONN_FAIL)
            self.wifi_status_label.setText("")

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def wifi_listWidget_item_clicked(self,item:QtWidgets.QListWidgetItem):
        self.wifi_username = item.text()
        self.wifi_status_label.setText("")
        self.wifi_pass_lineEdit.clear()
        self.stck_wnd.setCurrentIndex(self.screens[ID_WIFI_PASSWD_SCREEN])

    @pyqtSlot()
    def btn_wifi_search_released(self):
        self.search_wifi()
        # self.stck_wnd.setCurrentIndex(self.screens[ID_WIFI_PASSWD_SCREEN])

    @pyqtSlot()
    def btn_ok_language_released(self):
        #self.change_func()
        # self.stck_wnd.setCurrentIndex(self.screens[ID_SETTING_SCREEN])
        self.btn_back_released()


    def search_wifi(self): #function to search and display all the available Wifi networks
        self.wifi_listWidget.clear()
        device_ssid = []
        devices =  subprocess.run(['nmcli','-f','SSID','dev','wifi','list'], capture_output=True, text=True).stdout
        devices = devices.split("\n")
        for ssid in devices[1:]:
            if len(ssid) < 1 or ssid.startswith('--'):
                continue
            device_ssid.append(ssid.strip())
        for ssid in device_ssid:
            self.wifi_listWidget.addItem(ssid)

    def createNewConnection(self,name, SSID, key):
        self.wifi_status_label.setText("Connecting")
        command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
        os.system(command)
        #time.sleep(2)
        try:
            socket.create_connection(("1.1.1.1", 53))
            wifi_status = True
        except Exception as e:
            wifi_status = False

        if wifi_status == True:
            self.stck_wnd.setCurrentIndex(self.screens[ID_NET_CNT_SCREEN])
        else:
            self.show_net_fail_dialog()
            self.wifi_status_label.setText("")

    def show_net_fail_dialog(self):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_NET_FAIL,dialog)
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        w = self.geometry().width()
        h = self.geometry().height()
        dw = dialog.geometry().width()
        dh = dialog.geometry().height()
        rw = w/2 - dw/2
        rh = h/2 - dh/2 -5
        dialog.setGeometry(rw,rh,dialog.width(),dialog.height())
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('wifi-fail','Password Incorrect\nPlease try again'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('wifi-fail','OK'))
        dialog.open()

    def retranslateUi(self):
        self.btn_btmbar_back.setText(QtWidgets.QApplication.translate('Test','Back'))
        self.btn_btmbar_next.setText(QtWidgets.QApplication.translate('Test','Next'))

        self.label_welcom.setText(QtWidgets.QApplication.translate('Test','Welcome to UTA'))
        self.lbl_login_title.setText(QtWidgets.QApplication.translate('Test','Practice Login'))
        self.lbl_username.setText(QtWidgets.QApplication.translate('Test','User Name'))
        self.lbl_password.setText(QtWidgets.QApplication.translate('Test','Password'))
        self.btn_login.setText(QtWidgets.QApplication.translate('Test','Login'))
        
        self.label_3.setText(QtWidgets.QApplication.translate('Test','Scan to Authenticate'))
        self.label_2.setText(QtWidgets.QApplication.translate('Test','Scan to download app'))


        self.label_5.setText(QtWidgets.QApplication.translate('Test','Patient Information'))
        self.btn_female.setText(QtWidgets.QApplication.translate('Test','Female'))
        self.btn_male.setText(QtWidgets.QApplication.translate('Test','Male'))
        self.label_6.setText(QtWidgets.QApplication.translate('Test','New patient?'))
        self.btn_yes.setText(QtWidgets.QApplication.translate('Test','Yes'))
        self.btn_no.setText(QtWidgets.QApplication.translate('Test','No'))
        
        self.label_7.setText(QtWidgets.QApplication.translate('Test','Select Treatment Area'))
        self.txt_shoulder_L.setText(QtWidgets.QApplication.translate('Treatment','Shoulder'))
        self.txt_shoulder_R.setText(QtWidgets.QApplication.translate('Treatment','Shoulder'))
        self.txt_arm_L.setText(QtWidgets.QApplication.translate('Treatment','Arm'))
        self.txt_arm_R.setText(QtWidgets.QApplication.translate('Treatment','Arm'))
        self.txt_thigh_L.setText(QtWidgets.QApplication.translate('Treatment','Thigh'))
        self.txt_thigh_R.setText(QtWidgets.QApplication.translate('Treatment','Thigh'))
        # self.txt_arm.setText(QtWidgets.QApplication.translate('Test','Arm'))
        # self.txt_thigh.setText(QtWidgets.QApplication.translate('Test','Thigh'))

        self.label_8.setText(QtWidgets.QApplication.translate('Test','Position Electrodes'))
        self.txt_shoulder_pos_l.setText(QtWidgets.QApplication.translate('Test','Shoulder'))
        self.txt_shoulder_pos_r.setText(QtWidgets.QApplication.translate('Test','Shoulder'))

        self.label_11.setText(QtWidgets.QApplication.translate('Test','Timer'))
        self.label_9.setText(QtWidgets.QApplication.translate('Test','Applicator A'))
        self.label_10.setText(QtWidgets.QApplication.translate('Test','Applicator B'))
        self.btn_timer_stop.setText(QtWidgets.QApplication.translate('Test','STOP'))

        self.label_15.setText(QtWidgets.QApplication.translate('Test','SETTINGS'))
        self.btn_restore_default.setText(QtWidgets.QApplication.translate('Test','RESTORE DEFAULTS'))
        self.btn_language.setText(QtWidgets.QApplication.translate('Test','LANGUAGE'))
        self.btn_system_info.setText(QtWidgets.QApplication.translate('Test','SYSTEM INFO'))
        self.btn_advanced_services.setText(QtWidgets.QApplication.translate('Test','ADVANCED SERVICES'))
        self.btn_internet.setText(QtWidgets.QApplication.translate('Test','INTERNET'))
        self.btn_others.setText(QtWidgets.QApplication.translate('Test','OTHERS'))

        self.label_12.setText(QtWidgets.QApplication.translate('Test','Select Your Language'))
        self.btn_ok_language.setText(QtWidgets.QApplication.translate('Test','OK'))

        self.label_17.setText(QtWidgets.QApplication.translate('Test','Choose a network'))
        self.btn_wifi_search.setText(QtWidgets.QApplication.translate('Test','SEARCH'))

        self.label_19.setText(QtWidgets.QApplication.translate('Test','Input Password'))
        self.btn_cancel_wifi_passwd.setText(QtWidgets.QApplication.translate('Test','CANCEL'))
        self.btn_ok_wifi_passwd.setText(QtWidgets.QApplication.translate('Test','OK'))

        self.label_14.setText(QtWidgets.QApplication.translate('Test','NETWORK CONNECTED'))
        self.btn_net_conn_ok.setText(QtWidgets.QApplication.translate('Test','OK'))

    @QtCore.pyqtSlot(int)
    def change_func(self, index):
        data = self.lang_combo.itemData(index)
        self.langfile = data
        QtWidgets.QApplication.instance().removeTranslator(self.trans)
        if data:
            self.trans.load(data)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

# dialog for general message
    def show_dialog_with_message(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(msg)
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


    # dialog for general message - QR Error message
    def show_dialog_with_message_qr_msg(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('qr-error','Error\nCould not receive QR Code'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('qr-error',"OK"))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


    # dialog for general message - Unknown Error
    def show_dialog_with_message_unk_error(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('unknown-error','Unknown error occurred\nGo to Start Page'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('unknown-error',"OK"))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


    # dialog for general message - QR Scan Success
    def show_dialog_with_message_qr_success(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('qr-scan-success','Scan Success!'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('qr-scan-success',"OK"))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


        # dialog for general message - QR Scan Fail
    def show_dialog_with_message_qr_fail(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('qr-scan-fail','Scan Error\nPlease try again.'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('qr-scan-fail',"OK"))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


    # dialog for general message - Treatment Done
    def show_dialog_with_message_trmt_done(self,msg):
        dialog = QtWidgets.QDialog(self)
        uic.loadUi(STRING_UI_FILE_LOGIN_FAIL,dialog)
        dialog.txt_msg.setText(QtWidgets.QApplication.translate('treatment-done','Treatment is done go to Scan screen.'))
        dialog.btn_ok.setText(QtWidgets.QApplication.translate('treatment-done',"OK"))
        dialog.setModal(True)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.positing_dialog_on_center(dialog)
        dialog.exec()


    # dialog for loading with message
    def show_loading_dialog_with_message(self, msg):
        dialog = LoadingDialogWithMessage(self)
        dialog.setMessage(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()

    #for login loading dialog box (TESTING PURPOSE)
    def show_loading_dialog_with_message_login(self, msg):
        dialog = LoadingDialogWithMessage_login(self, self.langfile)
        dialog.setMessage(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()

    #for login loading dialog box - Server (TESTING PURPOSE)
    def show_loading_dialog_with_message_server(self, msg):
        dialog = LoadingDialogWithMessage_server(self, self.langfile)
        dialog.setMessage(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()

    #for login loading dialog box - QR (TESTING PURPOSE)
    def show_loading_dialog_with_message_qr(self, msg):
        dialog = LoadingDialogWithMessage_qr(self, self.langfile)
        dialog.setMessage(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()


    # dialog for wifi loading message
    def show_wifi_loading_dialog_with_message(self, msg):
        dialog = WifiLoadingDialogWithMessage(self, self.langfile)
        dialog.setMessage(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()

    # dialog for loading with message
    def show_dialog_with_html_message(self, msg):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        uic.loadUi(STRING_UI_FILE_HTML_DIALOG,dialog)
        dialog.html_view.setText(msg)
        self.positing_dialog_on_center(dialog)
        self.dialog_on_screen = dialog
        dialog.exec()

#for positing dialog on center
    def positing_dialog_on_center(self,dialog):
        w = self.geometry().width()
        h = self.geometry().height()
        dw = dialog.geometry().width()
        dh = dialog.geometry().height()
        rw = w/2 - dw/2
        rh = h/2 - dh/2 -5
        dialog.setGeometry(rw,rh,dialog.width(),dialog.height())


    def set_graphic(self,sex):
        self.scene_patient = QtWidgets.QGraphicsScene()
        if sex == SEX.MALE:
            self.image_patient = QtGui.QPixmap(IMAGE_FOR_MALE)
        else:
            self.image_patient = QtGui.QPixmap(IMAGE_FOR_FEMALE)
        self.scene_patient.addPixmap(self.image_patient)
        self.gv_humanbody.setScene(self.scene_patient)
        self.gv_humanbody.setRenderHint(QtGui.QPainter.Antialiasing)


        # for lbl in txt_label_list:
        #     lbl.setStyleSheet(STR_COLOR_STYLE_FOR_LABEL%(FONT_COLOR_DISABLED_R,FONT_COLOR_DISABLED_G,FONT_COLOR_DISABLED_B))

        self.txt_shoulder_L.show()
        self.txt_shoulder_R.show()
        self.txt_arm_L.show()
        self.txt_thigh_L.show()
        self.txt_arm_R.show()
        self.txt_thigh_R.show()

        self.line_shoulder_L.show()
        self.line_shoulder_R.show()

        self.line_arm_L.show()
        self.line_thigh_L.show()
        self.line_arm_R.show()
        self.line_thigh_R.show()

        self.gv_humanbody_pos.setScene(self.scene_patient)
        self.gv_humanbody_pos.setRenderHint(QtGui.QPainter.Antialiasing)

        self.line_shoulder_pos_l.show()
        self.line_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()
        self.txt_shoulder_pos_r.show()


    def close_current_dialog(self):
        self.dialog_on_screen.close()

    def reset_values(self):
        self.timer = None

    def go_to_start_screen(self):
        self.stck_wnd.setCurrentIndex(self.screens[ID_LOGIN_SCREEN])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.showFullScreen()
    window.show()
    app.exec_()

