import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice
from scanner import scan
from vigia_sensor import vigia
import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
import os
from datetime import datetime
from PySide2.QtCore import Slot
import threading
from threading import Thread, active_count
import queue
from utility import model_to_csv


class janela(QMainWindow):
    def __init__(self):
        loader = QUiLoader()
        dirname = os.path.dirname(os.path.abspath(__file__))
        os.chdir(dirname)
        ui_file = QFile("mover.ui")
        ui_file.open(QFile.ReadOnly)
        self.interface = loader.load(ui_file)
        self.interface.setWindowTitle(
            'Projeto Integrador 2 - Carrinho Autônomo')
        ui_file.close()
        super(janela, self).__init__()


class Gerente:
    def __init__(self, app, janela, last_uart):
        self.app = app
        self.runners = []
        self.semaphores = []
        running_detector = threading.Event()
        running_detector.set()
        interrupt_scanner = threading.Event()
        interrupt_scanner.set()
        semafaro_detector = threading.Semaphore(1)
        semafaro_scanner = threading.Semaphore(0)
        self.runners.append(running_detector)
        self.semaphores.append(semafaro_detector)
        self.semaphores.append(semafaro_scanner)
        self.janela = janela
        self.janela.interface.show()
        self.janela.interface.botao_pathfind.setEnabled(False)
        self.janela.interface.botao_solve.setEnabled(False)
        self.janela.interface.botao_manual.setEnabled(False)
        self.janela.interface.botao_salvar.setEnabled(False)
        self.fname = "bateria_" + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        janela.interface.label_tempo.setText('')
        scannerThread = Thread(name='scan', target=scan, args=(
            janela.interface, running_detector, interrupt_scanner, semafaro_scanner, semafaro_detector, self.fname, last_uart))
        vigiaThread = Thread(name='vigia_sensor', target=vigia, args=(
            janela.interface, running_detector, interrupt_scanner, semafaro_scanner, semafaro_detector, last_uart))
        scannerThread.start()
        vigiaThread.start()

        @Slot()
        def go():
            janela.interface.label_tempo.setText(
                "bateria_" + datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
            janela.interface.label_relatorio.setText('')
            interrupt_scanner.clear()
            semafaro_scanner.release()
            running_detector.set()

        @Slot()
        def stop():
            arq = janela.interface.label_tempo.text()
            janela.interface.label_relatorio.setText(
                'Relatório Salvo: ' + arq)
            janela.interface.label_tempo.setText('')
            interrupt_scanner.set()

        @Slot()
        def detecting():
            pass
            semafaro_detector.release()

        @Slot()
        def salvar_manual():
            #fname = get_filename(self.janela.interface)
            print("kk eae men")

        @Slot()
        def frente():
            self.janela.interface.label_comando_atual.setText('f')
            #fname = get_filename(self.janela.interface)
            print("kk eae men")

        @Slot()
        def re():
            self.janela.interface.label_comando_atual.setText('b')
            #fname = get_filename(self.janela.interface)
            print("kk eae men")

        @Slot()
        def esquerda():
            self.janela.interface.label_comando_atual.setText('l')
            #fname = get_filename(self.janela.interface)
            print("kk eae men")

        @Slot()
        def direita():
            self.janela.interface.label_comando_atual.setText('r')
            #fname = get_filename(self.janela.interface)
            print("kk eae men")

        @Slot()
        def parar():
            #fname = get_filename(self.janela.interface)
            self.janela.interface.label_comando_atual.setText('p')
            print("kk eae men")

        self.janela.interface.botao_conectar.clicked.connect(go)
        self.janela.interface.botao_frente.clicked.connect(frente)
        self.janela.interface.botao_tras1.clicked.connect(re)
        self.janela.interface.botao_esquerda.clicked.connect(esquerda)
        self.janela.interface.botao_direita.clicked.connect(direita)
        self.janela.interface.botao_parar.clicked.connect(parar)
        self.janela.interface.botao_desconectar.clicked.connect(stop)
        self.janela.interface.botao_salvar.clicked.connect(salvar_manual)

    def exec(self):
        self.app.exec_()
        self.clean_up()

    def clean_up(self):
        print("CLEAN EXIT")
        for runner in self.runners:
            runner.clear()

        for semaphore in self.semaphores:
            semaphore.release()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    last_uart = queue.Queue()
    window = janela()
    gerente = Gerente(app, window, last_uart)
    gerente.exec()
