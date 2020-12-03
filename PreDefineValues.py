TIMER_INTERVAL_IN_MSEC = 1000
TIMER_START_VALUE = 0*3600+0*60+10

"""IMAGE_RESOURCES"""
IMAGE_FOR_MALE = "images/male.png"
IMAGE_FOR_FEMALE = "images/female.png"
IMAGE_FOR_LOADING = "images/loading22.gif"

"""STRING RESOURCES"""
STRING_TIMER_NUMBER_FORMAT = "%02d:%02d:%02d"
STRING_APPLICATOR_VALUE_FORMAT = "{value}%"
STRING_UI_FILE_MAIN_WINDOW = "./main_window.ui"
STRING_UI_FILE_LOGIN_FAIL = "./login_fail_dialog.ui"
STRING_UI_FILE_LOADING = "./loading_with_msg.ui"
STRING_UI_FILE_HTML_DIALOG = "./html_dialog.ui"

"""STRING RESOURCES FOR MESSAGES"""
UNKNOWN_ERROR = "Unknown error occurred\nGo to Start Page"

STRING_LOGIN_ON_PROCESSING = "Logging in...."
STRING_RECEIVING_FROM_SERVER = "Receiving Data from Server"
STRING_ERROR_RECEIVING_QRCODE = """Error\nCould not receive QR Code"""

STRING_RECV_QR_SCAN_FROM_SERVER = "Receiving QR Code for Scan from Server"
STRING_SCAN_QRCODE_FAIL = """Scan Error\nPlease try again."""
STRING_SCAN_QRCODE_SUCCESS = """Scan Success!"""


STRING_LOGIN_FAIL = """\nId or password is incorrect    \nPlease Check\n"""
STRING_LOGIN_SUCCESS = """\nLogin Success!\n"""
STRING_TREATMENT_DONE = """Treatment is done go to Scan screen."""
STRING_UI_FILE_NET_FAIL = "./net_fail_dialog.ui"
#STRING_UI_FILE_CONNECTING = "./connecting_dialog.ui"

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




ID_QR_CODE_AUTH = 0
ID_QR_CODE_DOWNLOAD = 1
ID_QR_CODE_SCAN = 2

ID_BTN_BOTTOM_BAR_NEXT = 1
ID_BTN_BOTTOM_BAR_BACK = 0
BottomBar_showing_info   =   [ ## Back, Next
    (False,False),## for "splash_screen"
    (False,False),## for "login_screen"
    (False,False),## for "auth_screen"
    (False,False),## for "scan_screen"
    ( True, True),## for "pait_info_screen"
    ( True, True),## for "slct_trt_screen"
    ( True, True),## for "pos_screen"
    (False,False),## for "timer_screen"
    ( True,False),## for "setting_screen"
    (False,False),## for "select_lang_screen"
    ( True,False),## for "wifi_select_screen"
    ( True,False),## for "wifi_passwd_screen"
    ( True,False),## for "net_cnt_screen"
]