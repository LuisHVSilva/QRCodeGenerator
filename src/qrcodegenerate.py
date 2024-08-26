import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
import qrcode.image.styles.moduledrawers as moduledrawers
import cv2
import subprocess
from io import BytesIO
import numpy as np
import crcmod
from utils.helper import input_check

# -----------------------------------------------
# Constants

IMAGE_GLOBAL_PATH = 'images'
MODULE_DRAWER_IMAGE_TYPE = 'png'
FINAL_IMAGE_TYPE = 'svg'
WIFI = 'WIFI'
WIFI_ICON = './images/icons/wifi.svg'
WIFI_SECURITY_DIC = {1: "WPA", 2: "WPA2", 3: "WEP", 4: "no_password_needed"}
PIX = "PIX"
PIX_PATTERN = "br.gov.bcb.pix:01/"
COMPANY = 'COMPANY'
SSID = 'SSID'
PASSWORD = 'PASSWORD'
SECURITY = 'SECURITY'
MERCHANT_ACCOUNT_GUI = "br.gov.bcb.pix"
CHAVE = "CHAVE"
MERCHANT_NAME = "NOME DO RECEBEDOR"
MERCHANT_CITY = "CIDADE DO RECEBEDOR"

# -----------------------------------------------
# External Functions
def path_check(company):
    path = os.path.join(os.getcwd(), f'{IMAGE_GLOBAL_PATH}\\{company}')

    if not os.path.exists(path):
        os.makedirs(path)

    return path

# -----------------------------------------------
# Class
class QrcodeGenerate:
    # Constructor
    def __init__(self, company):
        self.company = company
        self._hidden = None
        self._qrcode_data = None
        self._qrcode_filename = None
        self._module_drawer = None

    # -----------------------------------------------
    # Getter and Setters
    @property
    def qrcode_data(self):
        return self._qrcode_data

    @qrcode_data.setter
    def qrcode_data(self, value):
        self._qrcode_data = value

    @property
    def qrcode_filename(self):
        return self._qrcode_filename

    @qrcode_filename.setter
    def qrcode_filename(self, value):
        self._qrcode_filename = f"{value}.{FINAL_IMAGE_TYPE}"

    @property
    def module_drawer(self):
        return self._module_drawer

    @module_drawer.setter
    def module_drawer(self, value):
        self._module_drawer = value

    # -----------------------------------------------
    # QRCode methods
    def _png_to_svg(self, img):
        path = path_check(self.company)
        output_path = os.path.join(path, self.qrcode_filename)

        with BytesIO() as output:
            img.save(output, format="PNG")
            image_bytes = output.getvalue()

        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        pbm_path = 'temp.pbm'
        cv2.imwrite(pbm_path, binary_image)
        subprocess.run(['potrace', pbm_path, '--svg', '-o', output_path])

        os.remove(pbm_path)

    def _module_drawer_choice(self, qr):
        if self.module_drawer == 1:
            return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.CircleModuleDrawer())
        elif self.module_drawer == 2:
            return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.GappedSquareModuleDrawer())
        elif self.module_drawer == 3:
            return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.HorizontalBarsDrawer())
        elif self.module_drawer == 4:
            return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.RoundedModuleDrawer())
        elif self.module_drawer == 5:
            return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.SquareModuleDrawer())

        return qr.make_image(image_factory=StyledPilImage, module_drawer=moduledrawers.VerticalBarsDrawer())

    def _generate_qr(self):
        print("Qual tipo do qr code?")
        print("1 - CircleModuleDrawer")
        print("2 - GappedSquareModuleDrawer")
        print("3 - HorizontalBarsDrawer")
        print("4 - RoundedModuleDrawer")
        print("5 - SquareModuleDrawer")
        print("6 - VerticalBarsDrawer")
        self.module_drawer = int(input())

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Adicionar dados ao QR Code
        qr.add_data(self.qrcode_data)
        qr.make(fit=True)

        # Gerar a imagem do QR Code com módulos personalizados
        img = self._module_drawer_choice(qr)
        self._png_to_svg(img)

    # -----------------------------------------------
    # Wifi Methods
    def _wifi_security_option(self, wifi_security):
        if wifi_security == 1:
            return "WPA"
        elif wifi_security == 2:
            return "WPA2"
        elif wifi_security == 3:
            return "WEP"

        return None

    def _wifi_data(self, wifi_security, wifi_password, wifi_ssid):
        if wifi_security:
            if wifi_password is None:
                raise TypeError("For WPA, WPA2, and WEP Wi-Fi authentication, the password cannot be null.")
            self.qrcode_data = f'{WIFI}:T:{wifi_security};S:{wifi_ssid};P:{wifi_password};;'
        else:
            if wifi_password is not None:
                raise TypeError("For no password, the password may be null.")
            self.qrcode_data = f'{WIFI}:T:{wifi_security};S:{wifi_ssid};;'

        print(self.qrcode_data)
        self.qrcode_filename = WIFI

    def wifi(self, ssid, security, password):
        input_check(ssid, SSID)
        input_check(security, SECURITY)

        security = self._wifi_security_option(security)

        if security is not None and password is None:
            input_check(password, PASSWORD)

        self._wifi_data(security, password, ssid)
        self._generate_qr()

    # -----------------------------------------------
    # PIX Methods
    def _calculate_crc16(self, payload):
        crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        crc = crc16(bytes(payload, 'utf-8'))
        return format(crc, '04X')

    def pix(self, key, merchant_name, merchant_city):
        input_check(key, CHAVE)
        input_check(merchant_name, MERCHANT_NAME)
        input_check(merchant_city, MERCHANT_CITY)
        merchant_city = merchant_city.upper()

        payload = (
            f"000201"
            "010211"
            f"26{len(key) + len(MERCHANT_ACCOUNT_GUI) + 8}00{len(MERCHANT_ACCOUNT_GUI)}{MERCHANT_ACCOUNT_GUI}01{len(key)}{key}"
            f"52040000"
            f"5303986"
            f"5802BR"
            f"59{len(merchant_name)}{merchant_name}"
            f"6008{merchant_city}"
            f"62070503***"
            f"6304"
        )
        payload += self._calculate_crc16(payload)
        self.qrcode_data = payload
        self.qrcode_filename = PIX
        self._generate_qr()
        #qr = qrcode.make(payload)
        #qr.save("qrcode_pix.png")


