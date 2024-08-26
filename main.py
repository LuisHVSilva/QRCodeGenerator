from src import qrcodegenerate
from utils.helper import input_check
# -----------------------------------------------
# Constants
COMPANY = 'COMPANY'
WIFI = 'WIFI'
PASSWORD = 'PASSWORD'

# -----------------------------------------------
# Main


print("Qual tipo de QR Code gostaria de criar?")
print("1 - Wifi")
print("2 - Pix")

qrcode_type = int(input())

company = input('Qual o nome da empresa?\n').strip()
input_check(company, COMPANY)
qrcode = qrcodegenerate.QrcodeGenerate(company)

if qrcode_type == 1 :
    print("-----------------------")
    print("Wifi QRCODE")
    print("-----------------------")
    ssid = input_check(input("Nome da rede (SSID): ").strip(), WIFI)

    print("Qual o tipo de segurança da rede?")
    print("1 - WPA")
    print("2 - WPA2")
    print("3 - WEP")
    print("4 - Sem senha")
    security = int(input())

    password = None
    if security in [1, 2, 3]:
        password = input_check(input("Senha: ").strip(), PASSWORD)

    qrcode.wifi(ssid, security, password)

if qrcode_type == 2:
    print("-----------------------")
    print("Pix QRCODE")
    print("-----------------------")

    #print("Qual a chave pix?")
    key = input("Qual a chave pix?: ")

    #print("Qual o nome da conta do recebedor?")
    merchant_name = input("Qual o nome da conta do recebedor?: ")

    merchant_city = input("Qual a cidade do recebedor?: ")
    qrcode.pix(key, merchant_name, merchant_city)