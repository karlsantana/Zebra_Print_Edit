# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teste_botao.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import time
import win32print
import win32api
#----------------------------------------------------------------------
def print_job_checker(filtro = None):
    try:
        
        """
        Prints out all jobs in the print queue every 5 seconds
        """
        result = []
        jobs = [1]
        while jobs:
            jobs = []
            for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,
                                             None, 1):
                flags, desc, name, comment = p

                #print(p)

                if filtro is not None:
                    for f in filtro:
                        if f in p[1]:
                            result.append(p)
                            break
                        
                else:
                    result.append(p)
                
                phandle = win32print.OpenPrinter(name)
                print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
                if print_jobs:
                    jobs.extend(list(print_jobs))
                for job in print_jobs:
                    #print("printer name => " + name)
                    document = job["pDocument"]
                    #print ("Document name => " + document)
                win32print.ClosePrinter(phandle)
                
            #time.sleep(5)
        #print ("No more jobs!")
        return result
    
    except Exception as e:
        print(e)
        return []


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(200, 220, 191, 22))
        self.comboBox.setObjectName("comboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.impressoras = []
        self.hPrinter = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def imprimir(self,comando):
        imp = self.comboBox.currentText()
        nomeCerto = imp.split(",")[0]

        
        try:
            
            if self.hPrinter is not None:
                win32print.ClosePrinter(self.hPrinter)
                self.hPrinter = None
            
            self.hPrinter = win32print.OpenPrinter(nomeCerto)
            print("abriu")
            hJob = win32print.StartDocPrinter(self.hPrinter, 1, ('PrintJobName', None, 'RAW'))
            #int:jobId = 1
            #hJob = win32print.ScheduleJob(self.hPrinter,jobId)
            try:
                #win32api.ShellExecute(0, "print","conteudo", None, ".", 0)
                win32print.StartPagePrinter(self.hPrinter)
                win32print.WritePrinter(self.hPrinter,bytearray(comando.encode()))  # Instead of raw text is there a way to print PDF File ?
                win32print.EndPagePrinter(self.hPrinter)
                print("imprimiu")
                #break
            except Exception as e1:
                print(e1)    
            finally:
                win32print.EndDocPrinter(self.hPrinter)
        except Exception as e:
            print(e)
        finally:
            #win32print.ClosePrinter(self.hPrinter)
            self.hPrinter = None
        print("Acabou")
    
    def atualizarListaDeImpressoras(self):
        global print_job_checker
        self.comboBox.clear()
        self.impressoras = print_job_checker(["GC420"])

        for i in self.impressoras:
            self.comboBox.addItem(i[1])

        comando = '''
                                ^XA^
                                FO50,50^GB100,100,100^FS
                                ^XZ
                            '''
        self.imprimir(comando)
        
        if True:
            return
        for i in self.impressoras:
            self.comboBox.addItem(i[1])
            print("Impressora: _______")
            print(i)
            print("Impressora FIM")
            nomeCerto = i[1].split(",")[0]
            #print("Nome certo:" +nomeCerto)
            if "ZDesigner GC420t (EPL)" in i[1]:
                print("Eu vou mandar")
                print("Nome certo:" +nomeCerto)
                #time.sleep(60)
                #hPrinter = win32print.OpenPrinter("ZDesigner GC420t (EPL)")
                hPrinter = win32print.OpenPrinter(nomeCerto)
                print("abriu")
                try:
                    hJob = win32print.StartDocPrinter(hPrinter, 1, ('PrintJobName', None, 'RAW'))
                    try:
                        #win32api.ShellExecute(0, "print", filename, None, ".", 0)
                        win32print.StartPagePrinter(hPrinter)
                        win32print.WritePrinter(hPrinter,bytearray(comando.encode()))  # Instead of raw text is there a way to print PDF File ?
                        win32print.EndPagePrinter(hPrinter)
                        print("imprimiu")
                        #break
                    except Exception as e1:
                        print(e1)    
                    finally:
                        win32print.EndDocPrinter(hPrinter)
                except Exception as e:
                    print(e)
                finally:
                    win32print.ClosePrinter(hPrinter)
                    break
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.comboBox.addItem("gfi")
    #ui.comboBox.addItem("7777")

    #global print_job_checker

    ui.atualizarListaDeImpressoras()
    '''
    ui.comboBox.clear()
    impressoras = print_job_checker()

    for i in impressoras:
        ui.comboBox.addItem(i[1])        
    '''
    sys.exit(app.exec_())
