

#import os.path


Impressaozpl=None

index = -1

box_txt=None


from PyQt5 import QtCore, QtGui, QtWidgets

#import threading

#from zebra import Zebra



#import serial
#import serial.tools.list_ports
#import subprocess
#import os

#import time

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QVBoxLayout

import tela1

import tela2_0

import sqlite3







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


class Jiga3(QMainWindow, tela1.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.pushButton_4.clicked.connect(self.salvar)
        self.pushButton_5.clicked.connect(self.cancelar)
        self.jiga = None


        def mudou():
            self.checarRadioButton()

        #if self.radio_central.toggled.connect(mudou) == False:
            #print("funfou")
        #self.radio_duplo.toggled.connect(mudou)


        self.radioButton.toggled.connect(mudou)

        self.radioButton_2.toggled.connect(mudou)

        #self.zplAtual = self.pegarZplAbrindo()


        self.zplAtual = self.pegarEditando()
        if self.zplAtual is not None:
            print(self.zplAtual["nome"])
            self.textEdit.setText(self.zplAtual["nome"])
            self.textEdit_2.setText(self.zplAtual["modelo"])

            i = self.zplAtual["indexZplUsando"]
            if i == 0:
                self.radioButton_2.setChecked(True)
            elif i == 1:
                self.radioButton.setChecked(True)
            else:
                self.radioButton.setChecked(False)
                self.radioButton_2.setChecked(False)

    def set_jiga3(self, jiga):
            self.Jiga = jiga

    def salvar(self):
        self.Salvar_tudo(self.zplAtual, index)
        self.loginform = tela2_0.Jiga1()
        self.loginform.set_jiga(self)
        self.loginform.show()
        self.close()

    def cancelar(self):
        self.loginform = tela2_0.Jiga1()
        self.loginform.set_jiga(self)
        self.loginform.show()
        self.close()

    def pegarEditando(self):
        con = None
        try:

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """SELECT * FROM zplconfig WHERE editando=true"""

            cur.execute(query)

            for linha in cur.fetchall():
                print(linha)

                zpl = {"id": linha[0],
                       "nome": linha[1],
                       "descricao": linha[2],
                       "zplComandCentral": linha[3],
                       "atual": linha[4],
                       "zplComandDuplo": linha[5],
                       "indexZplUsando": linha[6],
                       "editando": linha[7],
                       "abrindo": linha[8],
                       "modelo": linha[9]}

                return zpl

            return None

        except Exception as e:

            print(e)

            return None
        finally:
            if con is not None:
                con.close();

    def checarRadioButton(self):

        global box_txt
        global index
        global Impressaozpl

        if self.radioButton_2.isChecked():
            index = 0
            #print("comando central1")
            #print(self.getComandoZpl())
            #print(self.zpl["zplComandCentral"])
        elif self.radioButton.isChecked():
            index =  1
            #print("comando duplo1")
            #print(self.getComandoZpl())

        if self.setRadioButton(self.zplAtual,index) == True:
            self.edtar_txt_bx()
            self.textEdit_3.clear()
            self.textEdit_3.setText(Impressaozpl)
            print("1alterou")
            #print(self.getComandoZpl())
        else:
            print("náo alterou")

    def setRadioButton(self, zpl, index):
        con = None
        try:

            id = zpl["id"]

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """UPDATE zplconfig SET editando=? WHERE id=?"""

            cur.execute(query, (index, id))

            con.commit()

            return True
        except Exception as e:

            print(e)
            return False

        finally:
            if con is not None:
                con.close();

    def edtar_txt_bx(self):
        global Impressaozpl
        if self.radioButton.isChecked():
            Impressaozpl=self.zplAtual["zplComandDuplo"]
            print(Impressaozpl)
            #self.inicio_da_thread()
            #self.close
        elif self.radioButton_2.isChecked():
            Impressaozpl = self.zplAtual["zplComandCentral"]
            print(Impressaozpl)
            #self.inicio_da_thread()
            #self.close
    def Salvar_tudo(self,zpl,index):

            comando_final = None

            con = None
            try:

                id = zpl["id"]

                con = sqlite3.connect('serialprodutosbottomup.db')
                cur = con.cursor()

                global Impressaozpl
                if self.radioButton.isChecked():
                    box_txt = self.textEdit_3.toPlainText()
                    comando_final = box_txt
                    print(comando_final)
                    query = """UPDATE zplconfig SET zplComandDuplo=? WHERE id=?"""

                    cur.execute(query, (comando_final, id))

                    con.commit()
                    # self.inicio_da_thread()
                    # self.close
                elif self.radioButton_2.isChecked():
                    box_txt = self.textEdit_3.toPlainText()
                    comando_final = box_txt
                    print(comando_final)
                    query = """UPDATE zplconfig SET zplComandCentral=? WHERE id=?"""

                    cur.execute(query, (comando_final, id))

                    con.commit()
                    # self.inicio_da_thread()
                    # self.close



                return True
            except Exception as e:

                print(e)
                return False

            finally:
                if con is not None:
                    con.close();


if __name__ == '__main__':
    import sys
    qt = QtWidgets.QApplication(sys.argv)
    jiga_teste = Jiga3()

    jiga_teste.show()
    qt.exec_()



