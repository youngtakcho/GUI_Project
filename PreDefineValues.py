TIMER_INTERVAL_IN_MSEC = 1000
TIMER_START_VALUE = 0*3600+0*60+10
SEC_AUTO_DIALOG_CLOSE = 5000
GLOWING_EFFECT_COLOR_R = 15
GLOWING_EFFECT_COLOR_G = 220
GLOWING_EFFECT_COLOR_B = 232
FONT_COLOR_DISABLED_R = 10
FONT_COLOR_DISABLED_G = 90
FONT_COLOR_DISABLED_B = 90

STR_COLOR_STYLE_FOR_LABEL = """.QLabel{color:rgb(%d,%d,%d);}"""

"""IMAGE_RESOURCES"""
IMAGE_FOR_MALE = "images/male.png"
IMAGE_FOR_FEMALE = "images/female.png"
IMAGE_FOR_LOADING = "images/loading22.gif"
IMAGE_FOR_WIFI_CONN = "images/wifi-loading.gif"

"""STRING RESOURCES"""
STRING_TIMER_NUMBER_FORMAT = "%02d:%02d:%02d"
STRING_APPLICATOR_VALUE_FORMAT = "{value}%"
STRING_UI_FILE_MAIN_WINDOW = "main_window.ui"
STRING_UI_FILE_LOGIN_FAIL = "./login_fail_dialog.ui"
STRING_UI_FILE_LOADING = "./loading_with_msg.ui"
STRING_UI_FILE_HTML_DIALOG = "./html_dialog.ui"
STRING_UI_FILE_NET_FAIL = "./net_fail_dialog.ui"

"""STRING RESOURCES FOR MESSAGES"""
UNKNOWN_ERROR = "Unknown error occurred\nGo to Start Page"

STRING_LOGIN_ON_PROCESSING = "Logging in...."
STRING_RECEIVING_FROM_SERVER = "Receiving Data from Server"
STRING_ERROR_RECEIVING_QRCODE = """Error\nCould not receive QR Code"""

STRING_WIFI_CONN_ON_PROCESSING = "Connecting...."
STRING_WIFI_CONN_SUCCESS = "Network Connected"
STRING_WIFI_CONN_FAIL = "Password Incorrect\nPlease try again"

STRING_RECV_QR_SCAN_FROM_SERVER = "Receiving QR Code for Scan from Server"
STRING_SCAN_QRCODE_FAIL = """Scan Error\nPlease try again."""
STRING_SCAN_QRCODE_SUCCESS = """Scan Success!"""


STRING_LOGIN_FAIL = """\nId or password is incorrect    \nPlease Check\n"""
STRING_LOGIN_SUCCESS = """\nLogin Success!\n"""
STRING_TREATMENT_DONE = """Treatment is done go to Scan screen."""

ID_SPLASH_SCREEN = "splash_screen"
ID_LOGIN_SCREEN = "login_screen"
ID_AUTH_SCREEN = "auth_screen"
# ID_SCAN_SCREEN = "scan_screen"
ID_PAIT_INFO_SCREEN = "pait_info_screen"
ID_SLCT_TRT_SCREEN = "slct_trt_screen"
ID_POS_SCREEN = "pos_screen"
ID_TIMER_SCREEN = "timer_screen"
ID_SETTING_SCREEN= "setting_screen"
ID_SELECT_LANG_SCREEN = "select_lang_screen"
ID_WIFI_SELECT_SCREEN = "wifi_select_screen"
ID_WIFI_PASSWD_SCREEN = "wifi_passwd_screen"
ID_NET_CNT_SCREEN = "net_cnt_screen"

class SEX:
    FEMALE = True
    MALE = False



ID_QR_CODE_AUTH = 0
ID_QR_CODE_DOWNLOAD = 1
ID_QR_CODE_SCAN = 2

ID_BTN_BOTTOM_BAR_NEXT = 1
ID_BTN_BOTTOM_BAR_BACK = 0
BottomBar_showing_info   =   [ ## Back, Next
    (False,False),## for "splash_screen"
    (False,False),## for "login_screen"
    (False,False),## for "auth_screen"
    # (False,False),## for "scan_screen"
    ( True, False),## for "pait_info_screen"
    ( True, True),## for "slct_trt_screen"
    ( True, True),## for "pos_screen"
    (False,False),## for "timer_screen"
    ( True,False),## for "setting_screen"
    (False,False),## for "select_lang_screen"
    ( True,False),## for "wifi_select_screen"
    ( True,False),## for "wifi_passwd_screen"
    ( True,False),## for "net_cnt_screen"
]

SCREENS = [
    ID_SPLASH_SCREEN,
    ID_LOGIN_SCREEN,
    ID_AUTH_SCREEN,
    # ID_SCAN_SCREEN,
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