
import World
import threading
import time
import random

class Qlearning:
    def __init__(self):
        self.discount=0.8
        self.actions = World.actions
        self.states = []
        self.Q = {}
        for i in range(World.x):
            for j in range(World.y):
                self.states.append((i, j))

        for state in self.states:
            temp = {}
            for action in self.actions:
                temp[action] = 0.1
                World.set_cell_score(state, action, temp[action])
            self.Q[state] = temp

        for (i, j) in World.targets:
            for action in self.actions:
                self.Q[(i, j)][action] = 1                                 #score for reaching the target
                World.set_cell_score((i, j), action, 1)


    def do_action(self,action):
        s = World.player[0]
        r = -World.score
        World.try_move(World.characters[0], action)
        s2 = World.player[0]
        r += World.score
        World.try_move(World.characters[2],random.choice(World.actions))
        return s, action, r, s2


    def max_Q(self,s):
        val = None
        act = None
        for a, q in self.Q[s].items():
            if val is None or (q > val):
                val = q
                act = a
        return act, val


    def inc_Q(self,s, a, alpha, inc):
        self.Q[s][a] *= 1 - alpha
        self.Q[s][a] += alpha * inc
        World.set_cell_score(s, a, self.Q[s][a])


    def run(self):
        time.sleep(1)
        alpha = 1
        t = 1
        while True:
            # Pick the right action
            s = World.player[0]
            max_act, max_val = self.max_Q(s)
            (s, a, r, s2) = self.do_action(max_act)

            # Update Q
            max_act, max_val = self.max_Q(s2)
            self.inc_Q(s, a, alpha, r + self.discount * max_val)

            # Check if the game has restarted
            t += 1.0
            if World.has_restarted():
                World.restart_game()
                time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            alpha = pow(t, -0.1)

            time.sleep(0.2)

if __name__== "__main__":
    qlearning=Qlearning()
    t = threading.Thread(target=qlearning.run)
    t.daemon = True
    t.start()
    World.start_game()
