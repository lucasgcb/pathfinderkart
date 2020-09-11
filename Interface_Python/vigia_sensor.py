# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:18:45 2019

@author: Dave
"""
import csv
from datetime import datetime
import time
import serial


def vigia(interface, running, interrupt, semafaro, detector, last_uart):
    sensor_list = [
        interface.botao_esquerda,
        interface.botao_frente,
        interface.botao_saida,
        interface.botao_direita,
        interface.botao_tras1,
        interface.botao_tras2,
    ]
    sensor_state = ["0", "0", "0", "0", "0", "0"]
    colors = {
        "0": "color: green",
        "1": "color: red"
    }
    while(True):
        if running.is_set() is False:
            return
        try:
            while(interrupt.is_set() is False and running.is_set()):
                # fazer dicionario
                txt = last_uart.get()
                print(txt)
                try:
                    sensores = txt.decode("utf-8").split(';')[1:]
                    for sensor in range(0, 6):
                        if sensores[sensor] != sensor_state[sensor]:
                            print("sensor changed")
                            print(colors[sensores[sensor]])
                            sensor_state[sensor] = sensores[sensor]
                            sensor_list[sensor].setStyleSheet(
                                colors[sensores[sensor]])
                except Exception as e:
                    print(e)
                    pass
        except (KeyboardInterrupt) as e:
            print("WATCH THREAD KILLED!" + str(e))
            try:
                if running.is_set() is False:
                    return
            except Exception:
                if running.is_set() is False:
                    return

        except Exception as e:
            print("watch thread died: " + str(e))
            try:
                if running.is_set() is False:
                    return
            except Exception:
                if running.is_set() is False:
                    return
