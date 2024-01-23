from PyQt5.QtGui import *

from serial.tools import list_ports

import tela2_0

import xyz

import serial.tools.list_ports

from PyQt5 import QtCore, QtGui, QtWidgets

import threading
import subprocess

from zebra import Zebra

import warnings
import serial
import serial.tools.list_ports

import time

import glob

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QVBoxLayout,QInputDialog
import urllib3
import requests

import csv
import os.path
import time
from datetime import datetime
COM=""
Tags = None

printduplo=False

Zebra_print = None

import sqlite3
import json

Impressaozpl = None

index = -1

SNcont = 0

printers = None

Tags = None
contador = None
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget,
)



try:

    db_id = sqlite3.connect("id.db")
except Exception as erro:
    print(erro)

try:
    now = datetime.now()

    #print("Data =", now)

    # dd/mm/YY H:M:S
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_string = now.strftime("%d/%m/%Y")
    # print("date and time =", dt_string)
    txt = dt_string

    x = txt.replace("/", "_").replace(" ", "_").replace(":", "_")

    # x = txt.replace("/", "").replace(" ", "").replace(":", "")
    z = x

    #print(z)

except Exception as e:
    print(e)

if sys.platform.lower().startswith('win'):
    IS_WINDOWS = True
    import win32print

else:
    IS_WINDOWS = False
    import subprocess

ipadr=""
DEVPFID=""
APPID=""
DEVID_classA=""
deviceProfileID_classA=""
Grav_sem_cadastro=""
SERIAL_OP=""
def config_read():
        global DEVPFID
        global APPID
        global ipadr
        global DEVID_classA
        global deviceProfileID_classA
        global Grav_sem_cadastro
        with open("IP.json", 'r', encoding='utf-8') as meu_json:
            dados = json.load(meu_json)
            #dados = json.load(meu_json)DEVPFID
            #dados = APPID

        print(dados)
        ipadr = str(dados["IP"])
        DEVPFID = str(dados["deviceProfileID"])
        APPID = str(dados["applicationID"])
        DEVID_classA = str(dados["applicationID_classA"])
        deviceProfileID_classA = str(dados["deviceProfileID_classA"])
        Grav_sem_cadastro = str(dados["Grav_sem_cadastro"])

        print(deviceProfileID_classA)
        print(DEVID_classA)
        print(ipadr)
        print(DEVPFID)
        print(APPID)
        print(Grav_sem_cadastro)


config_read()


def _getqueues_unix():
    queues = []
    try:
        output = subprocess.check_output(['lpstat', '-p'], universal_newlines=True)
    except subprocess.CalledProcessError:
        return []
    for line in output.split('\n'):
        if line.startswith('printer'):
            queues.append(line.split(' ')[1])
    return queues

def _getqueues_win():
    global printers
    printers = []
    for (a, b, name, d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
        # printers.append(name)
        # print(name)
        if 'ZDesigner' in name:
            printers.append(name)
    #             print("ZDesigner GC420t (EPL)")
    #             impressora = i
    #             # print('Achou impressora')
    #print(printers)
    return printers

def getqueues():
    """Returns a list of printer queues on local machine"""
    if IS_WINDOWS:
        return _getqueues_win()
    else:
        return _getqueues_unix()

def serial_ports():
    try:

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    except Exception as e:
        print(e)
        return []

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


class Jiga(QMainWindow, xyz.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.pushButton_2.clicked.connect(self.abrir_form_tela1)
        self.pushButton.clicked.connect(self.imprimir)
        self.impressaoAtual = None
        self.sn = None
        self.sem = threading.Semaphore()

        self.run_thread = None

        def mudou():
            self.checarRadioButton()

        #if self.radio_central.toggled.connect(mudou) == False:
            #print("funfou")
        #self.radio_duplo.toggled.connect(mudou)

        #self.pushButton.setEnabled(False)
        self.printarar_zpl()


        self.radio_duplo.toggled.connect(mudou)

        self.radio_central.toggled.connect(mudou)

        self.zplAtual = self.pegarZplAbrindo()

        if self.zplAtual is not None:

            #print(self.zplAtual)

            self.label_3.setText(self.zplAtual["nome"])
            self.label_4.setText(self.zplAtual["modelo"])
            self.label_2.setFont(QFont('Times', 20))
            self.label.setFont(QFont('Times', 20))
            self.label_4.setFont(QFont('Times', 20))
            self.label_4.setFont(QFont('Times', 20))
            self.label_3.setFont(QFont('Times', 20))
            self.pushButton.setFont(QFont('Times', 20))
            self.pushButton_2.setFont(QFont('Times', 15))
            self.radio_duplo.setFont(QFont('Times', 10))
            self.radio_central.setFont(QFont('Times', 10))
            self.radio_central.setFont(QFont('Times', 10))

            #pushButton_2

            #and size
            #self.label_2.setFont(QFont('Times', 10))

            i = self.zplAtual["indexZplUsando"]
            if i == 0:
                print("oia1")
                self.zplAtual["nome"]
               # print(self.getComandoZpl())
                print("comando central")

                self.radio_central.setChecked(True)
            elif i == 1:
                print("oia2")
                #print(self.getComandoZpl())
                print("comando duplo")
                self.radio_duplo.setChecked(True)
            else:
                print("oia3")
                self.radio_central.setChecked(False)
                self.radio_duplo.setChecked(False)


    def getComandoZpl(self):
        i = self.zplAtual["indexZplUsando"]
        #x=None
        if i == 0:
           # print(Linha[6])
           #y=self.zplAtual["zplComandCentral"]
            return self.zplAtual["zplComandCentral"]
            #x=self.zplAtual["zplComandCentral"]
        elif i == 1:
            return self.zplAtual["zplComandDuplo"]
            #x=self.zplAtual["zplComandDuplo"]

        #return x

    def abrir_form_tela1(self):
            self.loginform = tela2_0.Jiga1()
            self.loginform.set_jiga(self)
            self.loginform.show()
            self.close()

    def set_jiga(self, jiga1):
            self.Jiga = jiga1

    def checarRadioButton(self):

        global index

        if self.radio_central.isChecked():
            index = 0
            #print("comando central1")
            #print(self.getComandoZpl())
            #print(self.zpl["zplComandCentral"])
        elif self.radio_duplo.isChecked():
            index =  1
            #print("comando duplo1")
            #print(self.getComandoZpl())

        if self.setRadioButton(self.zplAtual,index) == True:
            print("alterou")
            #print(self.getComandoZpl())
        else:
            print("náo alterou")


    def setRadioButton(self, zpl, index):
        con = None
        try:

            id = zpl["id"]

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """UPDATE zplconfig SET indexZplUsando=? WHERE id=?"""

            cur.execute(query, (index, id))

            con.commit()

            return True
        except Exception as e:

            print(e)
            return False

        finally:
            if con is not None:
                con.close();

    def pegarZplAbrindo(self):
        con = None
        try:

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """SELECT * FROM zplconfig WHERE abrindo=true"""

            cur.execute(query)

            for linha in cur.fetchall():
                # print(linha)

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

                #print (zpl["zplComandCentral"])

                return zpl

            return None

        except Exception as e:

            print(e)

            return None
        finally:
            if con is not None:
                con.close();

    def printarar_zpl(self):
        global Tags
        con = None
        try:

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """SELECT * FROM zplconfig WHERE abrindo=true"""

            cur.execute(query)

            for linha in cur.fetchall():
                # print(linha)

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

                #print(zpl[8])
                if zpl["nome"] == "SEMPREGAS":
                    Tags = """["Sempregas_1(comFf)"]"""
                    print(Tags)
                if zpl["nome"] == "TX_400":
                    Tags = """["Tx_400"]"""
                    print(Tags)
                if zpl["nome"] == "TX_100":
                    Tags = """["Tx_100"]"""
                    print(Tags)

                   # print(Tags)


                return zpl

            return None

        except Exception as e:

            print(e)

            return None
        finally:
            if con is not None:
                con.close();

    def imprimir(self):
        global Impressaozpl
        self.pushButton.setEnabled(False)
        if self.radio_duplo.isChecked():
            Impressaozpl=self.zplAtual["zplComandDuplo"]
            print(Impressaozpl)
            self.inicio_da_thread()
            #self.pushButton.setEnabled(True)
            #self.close
        elif self.radio_central.isChecked():
            Impressaozpl = self.zplAtual["zplComandCentral"]
            print(Impressaozpl)
            self.inicio_da_thread()

            #self.close
    def inicio_da_class_thread(self):
        #self.sem.acquire()

        if self.run_thread is not None:
            self.run_thread.requestInterruption()
            print("matou a thread")
        time.sleep(0.1)
        self.run_thread = RunThread(parent=None)
        self.run_thread.Jiga = self
        self.run_thread.start()
    def inicio_da_thread(self):
        time.sleep(1)
        self.inicio_da_class_thread()
        #time.sleep(0.1)


class RunThread(QtCore.QThread):

    def __init__(self, parent=None):
        print("Executando init de RunThread")
        super(RunThread, self).__init__(parent)
        self.Jiga = None
        self.idImpressora=None

    def run(self):

            if self.Jiga:

                time.sleep(0.1)

            try:
                #print(self.contador)
                self.etapa_final()
                #self.Holtek()
                self.Jiga.pushButton.setEnabled(True)
                print("acabou o teste")
                #self.Jiga.btnSTART.setEnabled(True)
                #self.Jiga.sem.release()
                # time.sleep(5)
                # self.etapa_final()

            except:
                print("erro acabou a Run")


    def imprimirNaImpressora(self):
        try:
            cmd2 = self.printLabel()

            # Envia o array de byte para a impressora
            self.z.output(cmd2)

        except:
            print("erro")

    def getPrinter(self,z: Zebra):
        impressora = None
        impressoras = z.getqueues()
        for i in impressoras:
            print(i)
            #if i.find("GC405") or  is not -1:
            if 'ZDesigner ZD220-203' in i:
                print("ZDesigner GC420t (EPL)")
                impressora = i

                print(i)

                break
            #elif "ZDesigner" in i:
                #print("ZDesigner qualaquer")
               # impressora = i
               # break

        if impressora is not None:
                return impressora

        print("Impressora nao encontrada")

        return None

    def configurePrinter(self, labelHomeX, labelHomeY):
        try:
           # comando = "^XA"

            labelHomeX = str(labelHomeX)

            labelHomeY = str(labelHomeY)

            comando += "\r\n^LH" + labelHomeX + "," + labelHomeY

            # setar velocidade de impressão e de back vai de 2 a 12
            comando += "^PR2,2"

            # ativamento do sensor com GAP
            comando += "^MWN"

            # modo de impressão PEEL OFF
            #comando += "^MMP"

            # térmica direta
            #comando += "^MTD"

            # salva as configurações na impressora
            comando += "^JUS^XZ\r\n\r\n"

            # tirar os \r\n
            comando = comando.replace("\r\n", "")

            b = bytes(comando, 'utf-8')

            return b

        except:
            print("Erro")

    def printLabel(self):
        global Impressaozpl


        #comando = "^XA"



        #comando = comando.replace("\r\n", "")

        #Impressaozpl = Impressaozpl.replace("#{serial}",self.idImpressora)




        # comando += "^D8"

        print(Impressaozpl)


        b = bytes(Impressaozpl, 'utf-8')

        return b

    


    def etapa_final(self):
        #respostaDaRequisicao = self.send_post(self.idImpressora)

        #if respostaDaRequisicao[0] == False:
            #self.Jiga.lineEdit_CADASTROLORA.setText("REPROVADO")
            #self.cadastro_lora_status = False
            #print("Reprovado")
            #return
        print("vai imprimir")
        self.z = Zebra()
        # self.z.reset_default()
        self.pri = self.getPrinter(self.z)
        print("Testw")
        print(self.pri)
        self.z.setqueue(str(self.pri))
        cmd1 = self.configurePrinter(3, 0)

        # Envia o comando para a impressora
        self.z.output(cmd1)



        self.imprimirNaImpressora()

        self.Jiga.pushButton.setEnabled(True)


        print("etapa final")
        print("Executando init de RunThread")



if __name__ == '__main__':
    import sys
    qt = QtWidgets.QApplication(sys.argv)
    jiga_teste = Jiga()

    jiga_teste.show()
    qt.exec_()

