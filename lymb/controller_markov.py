# controller.py
import threading
import time
from lymb import MyApp, command_queue
from random import random

app = MyApp()

class markov_controller:
    def __init__(self):
        self.states = {} # (x, y) : [probability action1, probability action2, ...]
        self.action = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.current_state = (1, 18)

        for row in range(20):
            for col in range(20):
                if app.patern[row * 20 + col] == 0:
                    self.states[(row, col)] = [0.25, 0.25, 0.25, 0.25]

    def get_current_state(self, current_position):
        self.current_state = current_position


    def get_action(self):
        futur_state = self.states[self.current_state]
        choice = random()
        for state in futur_state:
            if state < choice:
                choice -= state
            else:
                return self.action[futur_state.index(state)]
        

def exec_state():
    markov = markov_controller()
    while True:
        time.sleep(1)
        markov.get_current_state((app.robot_row, app.robot_col))
        command_queue.put(markov.get_action())


# Lancer la logique dans un thread daemon (s'arrête avec l'app)
t = threading.Thread(target=exec_state, daemon=True)
t.start()

# Lancer Panda3D normalement (bloque ici)

app.run()