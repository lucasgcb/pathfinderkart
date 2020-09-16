# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:18:45 2019

@author: Dave
"""
import csv
from datetime import datetime
import time
import serial
from corretor_pathfind_defs import Pathfinder
from corretor_cpt_defs import CPT


def corretor(interface, running, interrupt, semafaro, detector, last_state):
	#Recebe novas informações dos sensores em last_state
	#Executa máquina de estados.
	#Se não houver novas informações, continue.
    sensor_state = ["0", "0", "0", "0", "0", "0"]
    while(True):
        detector.acquire()
        maq_CPT = CPT()
        maq_Pathfinder = Pathfinder()
        if running.is_set() is False:
            return
        try:
            while(interrupt.is_set() is False and running.is_set()):
                try:
                    try:
                        sensor_state = last_state.get(timeout=2)[:-1]
                    except Exception as e:
                        print("sensor update timeout")
                        pass
                    print("sensores:" + str(sensor_state))
                    maq_Pathfinder.run(
                        interface, sensor_state, maq_CPT.cpt_state)
                    maq_CPT.run(interface, sensor_state,
                                maq_Pathfinder.pathfinder_state)
                except Exception as e:
                    print("PAU NAS MAQUINA: " + str(e))
                    pass
        except (KeyboardInterrupt) as e:
            print("WATCH THREAD KILLED!" + str(e))
            try:
                if running.is_set() is False:
                    detector.release()
                    return
            except Exception:
                if running.is_set() is False:
                    detector.release()
                    return

        except Exception as e:
            print("watch thread died: " + str(e))
            try:
                if running.is_set() is False:
                    detector.release()
                    return
            except Exception:
                if running.is_set() is False:
                    detector.release()
                    return
