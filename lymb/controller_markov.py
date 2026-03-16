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
        self.history = [] # action, state
        self.current_state = (1, 18)
        self.reward, self.G = {0: [[] for i in range(STEPS)]}, [[] for i in range(STEPS)]
        self.gamma, self.alpha = 0.7, 0.05
        self.cursor, self.nb_episode = 0, 0

        for row in range(20):
            for col in range(20):
                if app.patern[row * 20 + col] == 0:
                    self.states[(row, col)] = [0.25, 0.25, 0.25, 0.25]

    def get_current_state(self, current_position):
        self.current_state = current_position

    def get_action(self):
        if self.current_state == (1.0, 18.0):
            self.reward[self.nb_episode][self.cursor] = 1
            self.end_episode()
            return (0, 0) # renitialise le bordel
        
        futur_state = self.states[self.current_state]
        choice = random()
        print(choice)
        for state_i in range(len(futur_state)):
            print(futur_state[state_i])
            if futur_state[state_i] < choice:
                choice -= futur_state[state_i]
            else:
                action = self.action[state_i]
                
                self.reward[self.nb_episode][self.cursor] = -1
                self.history.append([action, self.current_state])
                self.cursor += 1
                return action

    def opposite(self, val): return 1-val
    
    def end_episode(self):
        self.cursor = 0
        for state_i in range(STEPS):
            G = sum(self.reward[self.nb_episode][state_i + k] * (self.gamma ** k) for k in range(STEPS - state_i))
            action_previous = self.history[state_i][0] # get action
            i_other_action = [i for i in range(4) if i != action_previous]
            old_action = self.states[state_i][action_previous]
            
            if self.G[state_i] > 0:
                self.state[self.history[state_i]] += self.alpha * self.G[state_i] * self.states[state_i][action_previous]
            else: self.state[self.history[state_i]] -= self.alpha * self.G[state_i] * self.states[state_i][action_previous]
            ratio = self.opposite(self.state[self.history[state_i]])/self.opposite(old_action)
            for i in i_other_action:
                self.state[self.history[state_i]] *= ratio
            
        self.nb_episode += 1
        self.reward[self.nb_episode], self.G[self.nb_episode] = [[] for i in range(STEPS)],[[] for i in range(STEPS)]

def exec_state():
    markov = markov_controller()
    while True:
        for i in range(STEPS):
            time.sleep(1)
            markov.get_current_state((app.robot_row, app.robot_col))
            action = markov.get_action()
            command_queue.put(action)
            print(action)
        markov.end_episode()


# Lancer la logique dans un thread daemon (s'arrête avec l'app)
t = threading.Thread(target=exec_state, daemon=True)
t.start()

# Lancer Panda3D normalement (bloque ici)

app.run()