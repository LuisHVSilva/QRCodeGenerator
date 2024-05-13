import qrcode
import qrcode.image.svg
import os
from qrcode.image.styledpil import StyledPilImage

# -----------------------------------------------
# Constants

IMAGE_GLOBAL_PATH = 'images'
IMAGE_TYPE = 'svg'
WIFI = 'WIFI'
WIFI_ICON = './images/icons/wifi.svg'
WIFI_SECURITY_DIC = {1: "WPA", 2: "WPA2", 3: "WEP", 4: "no_password_needed"}
PIX = "PIX"
PIX_PATTERN = "br.gov.bcb.pix:01/"


# -----------------------------------------------
# External Functions
def path_check(company):
    path = os.path.join(os.getcwd(), f'{IMAGE_GLOBAL_PATH}/{company}')

    if not os.path.exists(path):
        os.makedirs(path)

    return path


# -----------------------------------------------
# Class
class QrcodeGenerate:
    # Constructor
    def __init__(self, company):
        self.company = company
        self._wifi_security = None
        self._wifi_ssid = None
        self._wifi_password = None
        self._hidden = None
        self._qrcode_data = None
        self._qrcode_filename = None

    # -----------------------------------------------
    # Getter and Setters
    @property
    def qrcode_data(self):
        return self._qrcode_data

    @qrcode_data.setter
    def qrcode_data(self, new_data):
        self._qrcode_data = new_data

    @property
    def qrcode_filename(self):
        return self._qrcode_filename

    @qrcode_filename.setter
    def qrcode_filename(self, new_filename):
        self._qrcode_filename = new_filename

    @property
    def wifi_security(self):
        return self._wifi_security

    @wifi_security.setter
    def wifi_security(self, security):
        try:
            self._wifi_security = WIFI_SECURITY_DIC[security]
        except TypeError:
            print("Wifi security code not registered.")

    @property
    def wifi_ssid(self):
        return self._wifi_ssid

    @wifi_ssid.setter
    def wifi_ssid(self, ssid):
        self._wifi_ssid = ssid

    @property
    def wifi_password(self):
        return self._wifi_password

    @wifi_password.setter
    def wifi_password(self, password):
        self._wifi_password = password

    # -----------------------------------------------
    # Methods
    def wifi(self):
        if self.wifi_security:
            if self.wifi_password is None:
                print("Entrou")
                raise TypeError("For WPA, WPA2, and WEP Wi-Fi authentication, the password cannot be null.")
            self.qrcode_data = f'{WIFI}:T:{self.wifi_security};S:{self.wifi_ssid};P:{self.wifi_password};;'
            print(self.qrcode_data)
        else:
            if self.wifi_password is not None:
                raise TypeError("For no password, the password may be null.")
            self.qrcode_data = f'{WIFI}:T:{self.wifi_security};S:{self.wifi_ssid};;'

        self.qrcode_filename = f"{WIFI}.{IMAGE_TYPE}"

    def generate_qr(self):
        path = path_check(self.company)
        factory = qrcode.image.svg.SvgPathImage
        qr_img = qrcode.make(self.qrcode_data, image_factory=factory)
        qr_img.save(os.path.join(path, self.qrcode_filename))
        # Future changes
        # qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        # qr.add_data(wifi)
        # img_3 = qr.make_image(image_factory=StyledPilImage, embeded_image_path="./images/icons/wifi.png")
