# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:18:45 2019

@author: Dave
"""
import csv
from datetime import datetime
import time
import serial


class Interrupt_Error(Exception):
    pass


def connection_setup(interface):
    interface.label_estado.setText("Conectando...")
    serCOM3 = serial.Serial("COM3", 9600, timeout=1.5, write_timeout=2)
    interface.label_estado.setText("Conectado")
    return serCOM3


def connection_cleanup(cmdr_handle, interface):
    try:
        interface.label_bateria.setText("N/A")
        interface.label_estado.setText("Desconectado")
        cmdr_handle.close()
    except Exception:
        pass
    return


def atualizar_csv_bateria(spamwriter, recebido_bluetooth, interface):
    try:
        lido = int(recebido_bluetooth.decode("utf-8").split(';')[0])
        volts = lido/1241
        percentual = int((lido - 3661)/(435) * 100)
        if percentual < 0:
            percentual = 0
        interface.label_bateria.setText(
            str(percentual) + '%' + " (" + str(round(volts, 2)) + "V)")
        spamwriter.writerow([datetime.now().strftime(
            "%d-%m-%Y %H-%M-%S"), str(percentual) + '%'])
    except Exception as e:
        print("err:")
        print(e)
        pass


def scan(interface, running, interrupt, semafaro, detector, fname, last_uart):
    anterior = time.time()
    motor_names = {"SBY#": "Aguardando",
                   "FWD#": "Frente",
                   "RGT#": "Direita",
                   "LFT#": "Esquerda",
                   "BAK#": "Ré", }
    while(True):
        semafaro.acquire()
        if running.is_set() is False:
            return
        try:
            placa = connection_setup(interface)
            with open(interface.label_tempo.text() + '.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(["Data", "Carga Bateria 12V"])
                while(interrupt.is_set() is False and running.is_set()):
                    test = interface.label_comando_atual.text()
                    placa.write(test.encode('utf-8'))
                    recebido_bluetooth = placa.read_until(b'#')
                    last_uart.put(recebido_bluetooth)
                    # print(str(last_uart))

                    if (time.time() - (anterior+1) > 0):
                        atualizar_csv_bateria(
                            spamwriter, recebido_bluetooth, interface)
                        anterior = time.time()
            raise Interrupt_Error
        except (KeyboardInterrupt) as e:
            print("Something went wrong: " + str(e))
            try:
                if running.is_set() is False:
                    return
                connection_cleanup(placa, interface)
            except Exception:
                if running.is_set() is False:
                    return

        except Exception as e:
            print("Something went wrong: " + str(e))
            try:
                if running.is_set() is False:
                    return
                connection_cleanup(placa, interface)
            except Exception:
                if running.is_set() is False:
                    return
