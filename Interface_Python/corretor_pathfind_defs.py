import time
# sensor_mask = {"esquerda": 0,
#                "frente": 1,
#                "direita": 2,
#                "saida": 3,
#                "tras1": 4,
#                "tras2": 5
#                }


class Pathfinder():
    def __init__(self):
        self.pathfinder_state = "survey"
        self.state_pathfind_maps = {"standby": "ok",
                                    "done": "done",
                                    "fwd": "busy",
                                    "shuffle_right": "busy",
                                    "shuffle_left": "busy",
                                    "left": "busy",
                                    "right": "busy",
                                    "fix_r": "busy",
                                    "fix_l": "busy",
                                    "ret": "busy"
                                    }

        self.state_pathfind_defs = {"survey": self.survey,
                                    "ret": self.ret,
                                    "ret_write": self.ret_write,
                                    "fix_l": self.fix_l,
                                    "fix_r": self.fix_r,
                                    "right": self.right,
                                    "right_write": self.right_write,
                                    "left": self.left,
                                    "left_write": self.left_write,
                                    "fwd": self.fwd,
                                    "fwd_write": self.fwd_write,
                                    }

    def run(self, interface, sensores, cpt_state):
        print("Estado Pathfinder:" + self.pathfinder_state)
        self.state_pathfind_defs[self.pathfinder_state](
            interface, sensores, cpt_state)

    def survey(self, interface, sensores, cpt_state):
        esquerda = (sensores[0] == "1")
        centro = (sensores[1] == "1")
        direita = (sensores[2] == "1")
        # saida = (sensores[3] == "1")
        tras1 = (sensores[4] == "1")
        tras2 = (sensores[5] == "1")
        fix = tras1 and tras2
        self.pathfinder_state = "survey"
        if esquerda and centro and direita and fix:
            self.pathfinder_state = "right_write"

        if esquerda and centro and (direita is False) and fix:
            self.pathfinder_state = "left_write"

        if esquerda and (centro is False) and (direita is False) and fix:
            self.pathfinder_state = "left_write"

        if (esquerda is False) and (centro is False) and direita and fix:
            self.pathfinder_state = "right_write"

        if (esquerda is False) and centro and direita and fix:
            self.pathfinder_state = "right_write"

        if (esquerda is False) and centro and (direita is False) and fix:
            self.pathfinder_state = "fwd_write"

        if (esquerda is False) and (centro is False) and (direita is False) and fix:
            self.pathfinder_state = "ret_write"

        if esquerda and (centro is False) and direita and fix:
            self.pathfinder_state = "right_write"

        if (fix is False):
            if (tras1 is False):
                self.pathfinder_state = "fix_r"
            else:
                self.pathfinder_state = "fix_l"

    def fix_l(self, interface, sensores, cpt_state):
        self.pathfinder_state = "fix_l"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"

    def fix_r(self, interface, sensores, cpt_state):
        self.pathfinder_state = "fix_r"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"

    def fwd_write(self, interface, sensores, cpt_state):
        # rotina de escrita
        self.pathfinder_state = "fwd"

    def fwd(self, interface, sensores, cpt_state):
        self.pathfinder_state = "fwd"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"

    def left_write(self, interface, sensores, cpt_state):
        # rotina de escrita
        self.pathfinder_state = "left"

    def left(self, interface, sensores, cpt_state):
        self.pathfinder_state = "left"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"

    def ret_write(self, interface, sensores, cpt_state):
        # rotina de escrita
        self.pathfinder_state = "ret"

    def ret(self, interface, sensores, cpt_state):
        self.pathfinder_state = "ret"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"

    def right_write(self, interface, sensores, cpt_state):
        # rotina de escrita
        self.pathfinder_state = "right"

    def right(self, interface, sensores, cpt_state):
        self.pathfinder_state = "right"
        if self.state_pathfind_maps[cpt_state] == "done":
            self.pathfinder_state = "survey"
