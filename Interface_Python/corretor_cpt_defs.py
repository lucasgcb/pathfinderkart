import time
# sensor_mask = {"esquerda": 0,
#                "frente": 1,
#                "direita": 2,
#                "saida": 3,
#                "tras1": 4,
#                "tras2": 5
#                }


class CPT():
    def __init__(self):
        self.cpt_state = "standby"

        self.state_pathfind_maps = {"survey": "standby",
                                    "ret": "ret",
                                    "ret_write": "standby",
                                    "fix_l": "fix_l",
                                    "fix_r": "fix_r",
                                    "right": "right",
                                    "right_write": "standby",
                                    "left": "left",
                                    "left_write": "standby",
                                    "fwd": "fwd",
                                    "fwd_write": "standby",
                                    "err": "shuffle_right"
                                    }
        self.state_cpt_defs = {
            "standby": self.standby,
            "fwd": self.fwd,
            "shuffle_right": self.shuffle_right,
            "shuffle_left": self.shuffle_left,
            "left": self.left,
            "right": self.right,
            "fix_r": self.fix_r,
            "fix_l": self.fix_l,
            "ret": self.ret,
            "done": self.done
        }

    def run(self, interface, sensors, pathfind_state):
        print("Estado CPT:" + self.cpt_state)
        self.state_cpt_defs[self.cpt_state](interface, sensors, pathfind_state)

    def done(self, interface, sensors, pathfind_state):
        interface.label_comando_atual.setText('p')
        self.cpt_state = self.state_pathfind_maps[pathfind_state]

    def standby(self, interface, sensores, pathfind_state):
        self.cpt_state = self.state_pathfind_maps[pathfind_state]

    def fix_l(self, interface, sensores, pathfind_state):
        #esquerda = (sensores[0] == "1")
        #frente = (sensores[1] == "1")
        #direita = (sensores[2] == "1")
        #saida = (sensores[3] == "1")
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        fix = tras1 and tras2
        self.cpt_state = "fix_l"
        if (tras1 is False):
            interface.label_comando_atual.setText('l')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"
        if (tras2 is False):
            interface.label_comando_atual.setText('r')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"

    def fix_r(self, interface, sensores, pathfind_state):
        # esquerda = (sensores[0] == "1")
        # frente = (sensores[1] == "1")
        # direita = (sensores[2] == "1")
        # saida = (sensores[3] == "1")
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        self.cpt_state = "fix_r"
        if (tras2 is False):
            interface.label_comando_atual.setText('r')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"
        if (tras1 is False):
            interface.label_comando_atual.setText('l')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"

    def left(self, interface, sensores, pathfind_state):
        interface.label_comando_atual.setText('l')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(3)
        interface.label_comando_atual.setText('l')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(2.5)
        interface.label_comando_atual.setText('l')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(1)
        interface.label_comando_atual.setText('l')
        time.sleep(0.5)
        self.cpt_state = "done"

    def right(self, interface, sensores, pathfind_state):
        interface.label_comando_atual.setText('r')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(3)
        interface.label_comando_atual.setText('r')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(2.5)
        interface.label_comando_atual.setText('r')
        time.sleep(1)
        interface.label_comando_atual.setText('f')
        time.sleep(1)
        interface.label_comando_atual.setText('r')
        time.sleep(0.5)
        self.cpt_state = "done"

    def ret(self, interface, sensores, pathfind_state):
        interface.label_comando_atual.setText('r')
        time.sleep(0.1)
        self.cpt_state = "done"

    def fwd(self, interface, sensores, pathfind_state):
        frente = (sensores[1] == "1")
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        self.cpt_state = "fwd"
        if fix and frente:
            interface.label_comando_atual.setText('f')
        else:
            self.cpt_state = "done"

    def shuffle_right(self, interface, sensores, pathfind_state):
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        self.cpt_state = "shuffle_right"
        if (fix is False):
            interface.label_comando_atual.setText('r')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"

    def shuffle_left(self, interface, sensores, pathfind_state):
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        self.cpt_state = "shuffle_left"
        if (fix is False):
            interface.label_comando_atual.setText('r')
        else:
            interface.label_comando_atual.setText('p')
            self.cpt_state = "done"
