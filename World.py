from Tkinter import *
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 100
(x, y) = (10, 5)
actions = ["up", "down", "left", "right"]
characters=["player1","player2","target"]
board = Canvas(master, width=x*Width, height=y*Width)
player_home=[(4,2),(1,2)]
player = [(4, 2),(1,2)]
score = 1
restart = False
walk_reward = -0.04
target_home=[(9,3)]
targets= [(9, 3)]
cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    # for (i,j) in targets:
    #     board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="red", width=1)

render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def map_action_commands(action_cmd):
    if action_cmd=="up":
        return 0,-1
    elif action_cmd=="down":
        return 0,1
    elif action_cmd=="right":
        return 1,0
    elif action_cmd=="left":
        return -1,0
    else:
        return 0,0


def try_move(agent, action_cmd):
    global player,targets,characters, x, y, score, walk_reward, me,me2,target, restart
    player_id=0
    target_id=1
    if restart == True:
        restart_game()
    if agent == characters[0]:
        player_id = 0
        display_object=me
        old_x=player[0][0]
        old_y=player[0][1]
    elif agent == characters[1]:
        player_id = 1
        display_object = me2
        old_x = player[1][0]
        old_y = player[1][1]
    elif agent == characters[2]:
        target_id = 0
        display_object = target
        old_x = targets[0][0]
        old_y = targets[0][1]
    dx,dy=map_action_commands(action_cmd)
    new_x = old_x + dx
    new_y = old_y + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y):
        board.coords(display_object, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        if target_id==0:
            targets[target_id]=(new_x,new_y)
            return
        else:
            player[player_id] = (new_x, new_y)
    for (i, j) in targets:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += 1
            if score > 0:
                print("Success! score: ", score)
            else:
                print("Fail! score: ", score)
            restart = True
            return


def call_up(event):
    try_move(characters[0],actions[0])

def call_down(event):
    try_move(characters[0],actions[1])

def call_left(event):
    try_move(characters[0],actions[2])

def call_right(event):
    try_move(characters[0],actions[3])

def restart_game():
    global player, score, me,me2,target, restart
    player[0] = player_home[0]
    player[1]=player_home[1]
    targets[0]=target_home[0]
    score = 1
    board.coords(me, player_home[0][0]*Width+Width*2/10, player_home[0][1]*Width+Width*2/10, player_home[0][0]*Width+Width*8/10, player_home[0][1]*Width+Width*8/10)
    board.coords(me2, player_home[1][0] * Width + Width * 2 / 10, player_home[1][1] * Width + Width * 2 / 10,
                 player_home[1][0] * Width + Width * 8 / 10, player_home[1][1] * Width + Width * 8 / 10)
    board.coords(target, target_home[0][0] * Width + Width * 2 / 10, target_home[0][1] * Width + Width * 2 / 10,
                 target_home[0][0] * Width + Width * 8 / 10, target_home[0][1] * Width + Width * 8 / 10)
    restart = False



def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0][0]*Width+Width*2/10, player[0][1]*Width+Width*2/10,
                            player[0][0]*Width+Width*8/10, player[0][1]*Width+Width*8/10, fill="blue", width=1, tag="me")
me2 = board.create_rectangle(player[1][0]*Width+Width*2/10, player[1][1]*Width+Width*2/10,
                            player[1][0]*Width+Width*8/10, player[1][1]*Width+Width*8/10, fill="orange", width=1, tag="me2")
target = board.create_rectangle(targets[0][0]*Width+Width*2/10, targets[0][1]*Width+Width*2/10,
                                targets[0][0]*Width+Width*8/10, targets[0][1]*Width+Width*8/10, fill="red", width=1, tag="target")


board.grid(row=0, column=0)


def start_game():
    master.mainloop()
