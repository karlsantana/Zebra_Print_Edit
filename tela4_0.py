#import sys

#import os.path

#import serial.tools.list_ports


from PyQt5 import QtCore, QtGui, QtWidgets



from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QVBoxLayout

import tela4

import tela2_0


class Banco:
    def __init__(self, parent=None,nomeDoBanco: str = "jiga_novo_banco.db",jigaTable:str = "jiga nao definida",numeroDaJiga:str = "Nao definida",deviceNome:str = "nao definido",campos: tuple = [],variaveis = None):
        self.parent = parent
        self.nomeBanco = nomeDoBanco
        self.jigaTable = jigaTable
        self.campos = campos
        self.deviceNome = deviceNome
        self.numeroDaJiga = numeroDaJiga
        self.variaveis = variaveis


class Dispositivo:
    def __init__(self, parent=None,idDevice: int = None,serialDevice: str = None,aprovado: bool = None,dbm: bool =  None,radiacao: bool = None,gravacao: bool = None,variacaoAdc: bool = None,variacaoCristal: bool = None,holtek: bool = None,cadastroLora: bool = None):
        self.idDevice = idDevice
        self.serialDevice = serialDevice
        self.aprovado = aprovado
        self.dbm = dbm
        self.radiacao = radiacao
        self.gravacao = gravacao
        self.variacaoAdc = variacaoAdc
        self.variacaoCristal = variacaoCristal
        self.holtek = holtek
        self.cadatroLora = cadastroLora


class Jiga2(QMainWindow, tela4.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.pushButton_2.clicked.connect(self.salar)
        self.pushButton.clicked.connect(self.cancelar)

        self.jiga = None



    def set_jiga2(self, jiga2):
            self.Jiga2 = jiga2

    def salar(self):
        self.loginform = tela2_0.Jiga1()
        self.loginform.set_jiga(self)
        self.loginform.show()
        self.close()

    def cancelar(self):
        self.loginform = tela2_0.Jiga1()
        self.loginform.set_jiga(self)
        self.loginform.show()
        self.close()

    def Salvar_banco(self):
        print("sanvando banco de dados")



if __name__ == '__main__':
    import sys
    qt = QtWidgets.QApplication(sys.argv)
    jiga_teste = Jiga2()

    jiga_teste.show()
    qt.exec_()



