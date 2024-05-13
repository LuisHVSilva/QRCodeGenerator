from src import qrcodegenerate

# -----------------------------------------------
# Constants
COMPANY = 'COMPANY'
SSID = 'SSID'
PASSWORD = 'PASSWORD'
SECURITY = 'SECURITY'


# -----------------------------------------------
# Functions
def input_check(field, field_name):
    if field is None or len(field) == 0:
        raise TypeError(f"The {field_name} cannot be null.")


# -----------------------------------------------
# Main

print("Qual tipo de QR Code gostaria de criar?")
print("1 - Wifi")

qrcode_type = int(input())

company = input('Qual o nome da empresa?\n').strip()
input_check(company, COMPANY)
qrcode = qrcodegenerate.QrcodeGenerate(company)

if qrcode_type == 1:
    print("-----------------------")
    print("Wifi QRCODE")
    print("-----------------------")
    ssid = input("Nome da rede (SSID): ").strip()
    input_check(ssid, SSID)
    qrcode.wifi_ssid = ssid

    print("Qual o tipo de segurança da rede?")
    print("1 - WPA")
    print("2 - WPA2")
    print("3 - WEP")
    print("4 - Sem senha")
    security = int(input())
    qrcode.wifi_security = security

    if security in [1, 2, 3]:
        password = input("Senha: ").strip()
        input_check(password, PASSWORD)
        qrcode.wifi_password = password

    a = qrcode.wifi()
    qrcode.generate_qr()
