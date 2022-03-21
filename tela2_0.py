from PyQt5.QtGui import *

from PyQt5.QtWidgets import *


from PyQt5 import QtCore, QtGui, QtWidgets






from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QVBoxLayout, \
    QAbstractItemView

import tela2
import tela4_0

import tela1_1


import ZEBRA_IMPRESSORA

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


class Jiga1(QMainWindow, tela2.Ui_MainWindow):

    def selecionarTodos(self):
        con = None
        try:

            con = sqlite3.connect('sqlprodutosbottomup.db')
            cur = con.cursor()

            query = """SELECT * FROM zplconfig"""

            cur.execute(query)

            lista = []

            for linha in cur.fetchall():
                zpl = {"id": linha[0],
                       "nome": linha[1],
                       "descricao": linha[2],
                       "zplComandCentral": linha[3],
                       "atual": linha[4],
                       "zplComandDuplo": linha[5],
                       "indexZplUsando": linha[6],
                       "editando": linha[7]}
                lista.append(zpl)

            return lista

        except Exception as e:

            print(e)

            return []

        finally:
            if con is not None:
                con.close();

    def refreshList(self):

        self.lista = self.selecionarTodos()
        lenLista = len(self.lista)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(lenLista)
        self.tableWidget.setColumnCount(1)
        #self.tableWidget.setRowCount.setFont(QFont('Times', 30))
        self.pushButton.setFont(QFont('Times', 30))
        #self.pushButton.(QFont('Times', 30))

        indexItem = 0
        for zpl in self.lista:
            self.tableWidget.setItem(0, indexItem, QtWidgets.QTableWidgetItem(zpl["nome"]))
            self.tableWidget.setItem(1, indexItem, QtWidgets.QTableWidgetItem(zpl["nome"]))
            indexItem = indexItem + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.lista = None

        self.lista = self.selecionarTodos()
        lenLista = len(self.lista)
        self.tableWidget.setRowCount(lenLista)
        self.tableWidget.setColumnCount(1)
        self.pushButton.setFont(QFont('Times', 15))



        indexItem = 0
        for zpl in self.lista:
            self.tableWidget.setItem(0,indexItem,QtWidgets.QTableWidgetItem(zpl["nome"]))
            #self.tableWidget.setItem(1,indexItem, QtWidgets.QTableWidgetItem(zpl["nome"]))
            indexItem = indexItem + 1



        self.pushButton_2.clicked.connect(self.criar_impressao)
        self.pushButton_3.clicked.connect(self.pegarZplSelecionado)
        self.pushButton.clicked.connect(self.abrindoZplSelecionado)
        #self.tableWidget.horizontalHeaderItem.setFont(QFont('Times', 30))
        self.pushButton_3.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)




        #self.jiga = None
        #self.jiga2 = None

    def set_jiga(self, jiga):
            self.Jiga = jiga





    def set_jiga3(self, jiga3):
            self.Jiga3 = jiga3

    def criar_impressao(self):
        self.loginform = tela4_0.Jiga2()
        self.loginform.set_jiga2(self)
        self.loginform.show()
        self.close()



    def criar_editar(self):
        self.loginform = tela1_1.Jiga3()
        self.loginform.set_jiga3(self)
        self.loginform.show()
        self.close()


    def voltar_tela_principal(self):
        self.loginform = ZEBRA_IMPRESSORA.Jiga()
        self.loginform.set_jiga(self)
        self.loginform.show()
        self.close()

    def pegarZplSelecionado(self):
        indexList = self.tableWidget.selectionModel().selectedIndexes();

        for linha in indexList:
            row = linha.row()
            zpl = self.lista[row]
            print(zpl)
            if self.editarZpl(zpl) == True:
                self.criar_editar()


    def deletarZplSelecionado(self):
        indexList = self.tableWidget.selectionModel().selectedIndexes();

        for linha in indexList:
            row = linha.row()
            zpl = self.lista[row]
            print(zpl)
            if self.delZpl(zpl) == True:
                self.refreshList()

    def abrindoZplSelecionado(self):
        indexList = self.tableWidget.selectionModel().selectedIndexes();

        for linha in indexList:
            row = linha.row()
            zpl = self.lista[row]
            print(zpl)
            print("idjeidjo")
            if self.abrirZpl(zpl) == True:
                self.voltar_tela_principal()


    def delZpl(self,zpl):
        con = None
        try:

            id = zpl["id"]

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """DELETE FROM zplconfig WHERE id=?"""

            cur.execute(query,[id])

            con.commit()

            return True
        except Exception as e:

            print(e)
            return False

        finally:
            if con is not None:
                con.close();

    def abrirZpl(self,zpl):
        con = None
        try:

            id = zpl["id"]

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """UPDATE zplconfig SET abrindo=false"""

            cur.execute(query)

            query = """UPDATE zplconfig SET abrindo=true WHERE id=?"""

            cur.execute(query, [id])

            con.commit()

            return True
        except Exception as e:

            print(e)
            return False

        finally:
            if con is not None:
                con.close();


    def editarZpl(self, zpl):
        con = None
        try:

            id = zpl["id"]

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """UPDATE zplconfig SET editando=false"""

            cur.execute(query)

            query = """UPDATE zplconfig SET editando=true WHERE id=?"""

            cur.execute(query, [id])

            con.commit()

            return True
        except Exception as e:

            print(e)
            return False

        finally:
            if con is not None:
                con.close();

    def selecionarTodos(self):
        con = None
        try:

            con = sqlite3.connect('serialprodutosbottomup.db')
            cur = con.cursor()

            query = """SELECT * FROM zplconfig"""

            cur.execute(query)

            lista = []

            for linha in cur.fetchall():
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

                lista.append(zpl)

            return lista

        except Exception as e:

            print(e)

            return []

        finally:
            if con is not None:
                con.close();


if __name__ == '__main__':
    import sys
    qt = QtWidgets.QApplication(sys.argv)
    jiga_teste1 = Jiga1()

    jiga_teste1.show()
    qt.exec_()



