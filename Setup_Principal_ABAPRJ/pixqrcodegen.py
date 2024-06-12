import crcmod
import qrcode
import os


class Payload:
    def __init__(self, nome, chavepix, valor, cidade, txtId, diretorio=""):
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor.replace(",", ".")
        self.cidade = cidade
        self.txtId = txtId
        self.diretorioQrCode = diretorio

        self.merchantAccount_tam = f"0014BR.GOV.BCB.PIX01{len(self.chavepix):02}{self.chavepix}"
        self.transactionAmount_tam = f"{len(self.valor):02}{float(self.valor):.2f}"
        self.addDataField_tam = f"05{len(self.txtId):02}{self.txtId}"
        self.nome_tam = f"{len(self.nome):02}"
        self.cidade_tam = f"{len(self.cidade):02}"

        self.payloadFormat = "000201"
        self.merchantAccount = f"26{len(self.merchantAccount_tam):02}{self.merchantAccount_tam}"
        self.merchantCategCode = "52040000"
        self.transactionCurrency = "5303986"
        self.transactionAmount = f"54{self.transactionAmount_tam}"
        self.countryCode = "5802BR"
        self.merchantName = f"59{self.nome_tam}{self.nome}"
        self.merchantCity = f"60{self.cidade_tam}{self.cidade}"
        self.addDataField = f"62{len(self.addDataField_tam):02}{self.addDataField_tam}"
        self.crc16 = "6304"

    def gerarPayload(self):
        self.payload = f"{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}"
        self.gerarCrc16(self.payload)

    def gerarCrc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
        self.crc16Code = crc16(payload.encode("utf-8"))
        self.crc16Code_formatado = f"{self.crc16Code:04X}"
        self.payload_completa = f"{payload}{self.crc16Code_formatado}"
        self.gerarQrCode(self.payload_completa, self.diretorioQrCode)

    def gerarQrCode(self, payload, diretorio):
        dir = os.path.expanduser(diretorio)
        self.qrcode = qrcode.make(payload)
        self.qrcode.save(os.path.join(dir, "pixqrcodegen.png"))

        return payload

# Exemplo de uso:
# payload = Payload("Pedro Cezar Silva de Souza", "+5521995897270", "100.00", "São Gonçalo", "ProjetoABAPRJ")
# payload.gerarPayload()
