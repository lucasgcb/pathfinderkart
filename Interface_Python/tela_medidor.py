import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice
from scanner import scan
import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
import os
from datetime import datetime
from PySide2.QtCore import Slot
import threading
from threading import Thread, active_count
from utility import model_to_csv


class janela(QMainWindow):
    def __init__(self):
        loader = QUiLoader()
        dirname = os.path.dirname(os.path.abspath(__file__))
        os.chdir(dirname)
        ui_file = QFile("mover.ui")
        ui_file.open(QFile.ReadOnly)
        self.interface = loader.load(ui_file)
        self.interface.setWindowTitle('Projeto Integrador 2 - Carrinho Autônomo')
        ui_file.close()
        super(janela, self).__init__()


class Gerente:
    def __init__(self, app, janela):
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
            janela.interface, running_detector, interrupt_scanner, semafaro_scanner, semafaro_detector, self.fname))
        scannerThread.start()

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

        self.janela.interface.botao_conectar.clicked.connect(go)
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
    window = janela()
    gerente = Gerente(app, window)
    gerente.exec()
