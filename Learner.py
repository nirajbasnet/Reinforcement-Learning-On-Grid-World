
import World
import threading
import time

class Qlearning:
    def __init__(self):
        self.discount=0.3
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

        for (i, j) in World.target_state_current:
            for action in self.actions:
                self.Q[(i, j)][action] = 1                                 #score for reaching the target
                World.set_cell_score((i, j), action, 1)


    def do_action(self,action):
        s = World.player
        r = -World.score
        if action == self.actions[0]:
            World.try_move(0, -1)
        elif action == self.actions[1]:
            World.try_move(0, 1)
        elif action == self.actions[2]:
            World.try_move(-1, 0)
        elif action == self.actions[3]:
            World.try_move(1, 0)
        else:
            return
        s2 = World.player
        r += World.score
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
            s = World.player
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

            time.sleep(0.1)

if __name__== "__main__":
    qlearning=Qlearning()
    t = threading.Thread(target=qlearning.run)
    t.daemon = True
    t.start()
    World.start_game()
