# controller.py
import threading
import time
from lymb import MyApp, command_queue
from random import random

app = MyApp()

STEPS = 70

class markov_controller:
    def __init__(self):
        self.states = {} # (x, y) : [probability action1, probability action2, ...]
        self.action = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.current_state = (1, 18)
        self.reward = []

        for row in range(20):
            for col in range(20):
                if app.patern[row * 20 + col] == 0:
                    self.states[(row, col)] = [0.25, 0.25, 0.25, 0.25]

    def get_current_state(self, current_position):
        self.current_state = current_position


    def get_action(self):
        futur_state = self.states[self.current_state]
        choice = random()
        print(choice)
        for state_i in range(len(futur_state)):
            print(futur_state[state_i])
            if futur_state[state_i] < choice:
                choice -= futur_state[state_i]
            else:
                self.reward.append(-1) 
                return self.action[state_i]

            
    def end_episode(self, reward):
        pass

        

def exec_state():
    markov = markov_controller()
    while True:
        for i in range(STEPS):
            time.sleep(1)
            markov.get_current_state((app.robot_row, app.robot_col))
            action = markov.get_action()
            command_queue.put(action)
            print(action)


# Lancer la logique dans un thread daemon (s'arrête avec l'app)
t = threading.Thread(target=exec_state, daemon=True)
t.start()

# Lancer Panda3D normalement (bloque ici)

app.run()