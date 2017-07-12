from copy import deepcopy as dc
class Node():
    def __init__(self, x_coor, y_coor, reward = 0):
        self.name = x_coor, y_coor
        self.q_values = [None, None, None, None, None]  # [N, E, S, W, Exit]
        self.reward = reward
        self.v_val = 0
        self.policy = 0

    def update_q(self, move=None, value=None):
        if move is not None and value is not None:
            self.q_values[move] = value
        self.v_val = max(self.q_values)
        self.policy = self.q_values.index(self.v_val)

states = {}

def compute_v_values(grid_config):
    global states
    results = []
    for i in range(len(grid_config)):
        for j in range(len(grid_config[i])):
            state = Node(i, j)
            if grid_config[i][j] == 2:
                state.reward = -10
                state.q_values[4] = -10
                state.v_val = -10
                state.policy = 4
                states[state.name] = (state)
            elif grid_config[i][j] == 1:
                state.reward = -5
                state.q_values[4] = -5
                state.v_val = -5
                state.policy = 4
                states[state.name] = (state)
            elif grid_config[i][j] == 3:
                state.reward = 30
                state.update_q(4, 30)
                states[state.name] = (state)
            elif grid_config[i][j] == 0:
                state.reward = -1
                states[state.name] = (state)
    def iteration(states):
        for i in range(len(grid_config)):
            for j in range(len(grid_config[i])):
                state = states[(i,j)]
                state = compute_step(grid_config, states, state)
                states[state.name] = state
        return states
    i = 0
    while i<50:
        states = iteration(states)
        i+=1
    for x in range(8):
        for y in range(8):
            print (x,y), states[(x,y)].q_values, states[(x,y)].v_val, states[(x,y)].policy
    for i in states:
        results.append(((7-i[0], i[1]), states[i].v_val))
    results.sort()
    return results

def compute_step(grid_config, states, state):
    #states = dc(states_or)
    x,y = state.name
    invalid_moves = []
    if x == 0:invalid_moves.append(0)
    elif x == 7:invalid_moves.append(2)
    if y == 7:invalid_moves.append(1)
    elif y == 0:invalid_moves.append(3)
    if grid_config[x][y] != 0:
        #state.v_val = state.v_val + state.reward
        return state

    for i in range(len(state.q_values)):
        if i not in invalid_moves:
            if i == 0:
                if (x-1,y) in states:
                    a = 0.70 * 0.8*states[(x-1, y)].v_val + 0.70 * 0.2*states[(x-1, y)].reward


                if (x, y-1) in states:
                    b = 0.15 * 0.8*states[(x, y-1)].v_val + 0.15 * 0.2*states[(x, y-1)].reward


                if (x, y+1) in states:
                    c = 0.15 * 0.8*states[(x, y+1)].v_val + 0.15 * 0.2*states[(x, y+1)].reward


                state.q_values[i] = a + b + c
                state.update_q()
            elif i == 1:
                if (x, y+1) in states:
                    a = 0.7 * 0.8*states[(x, y+1)].v_val + 0.7 * 0.2*states[(x, y+1)].reward


                if (x-1, y) in states:
                    b = 0.15 * 0.8*states[(x-1, y)].v_val + 0.15 * 0.2*states[(x-1, y)].reward


                if (x+1, y) in states:
                    c = 0.15 * 0.8*(states[(x+1, y)].v_val) + 0.15 * 0.2*states[(x+1, y)].reward


                state.q_values[i] = a + b + c
                state.update_q()

            elif i == 2:
                if (x + 1, y) in states:
                    a =  0.7 * 0.8*states[(x+1, y)].v_val +  0.7 * 0.2*states[(x+1, y)].reward


                if (x, y - 1) in states:
                    b =  0.15 * 0.8*states[(x, y-1)].v_val + 0.15 * 0.2*states[(x, y-1)].reward


                if (x, y + 1) in states:
                    c = 0.15 * 0.8*states[(x, y+1)].v_val + 0.15 * 0.2*states[(x, y+1)].reward


                state.q_values[i] = a + b + c
                state.update_q()

            elif i == 3:
                if (x, y-1) in states:
                    a =  0.7 * 0.8*states[(x, y-1)].v_val + 0.7 * 0.2*states[(x, y-1)].reward


                if (x-1, y) in states:
                    b = 0.15 * 0.8*states[(x-1, y)].v_val + 0.15 * 0.2*states[(x-1, y)].reward


                if (x+1, y) in states:
                    c =  0.15 * 0.8*states[(x+1, y)].v_val + 0.15 * 0.2*states[(x+1, y)].reward


                state.q_values[i] = a + b + c
                state.update_q()
    return state



def get_optimal_policy(grid_config):
    global states
    #states = {}
    compute_v_values(grid_config)
    results = []
    for i in states:
        results.append(((7 - i[0], i[1]), states[i].policy))
    results.sort()
    return results

ex = [[2, 2, 2, 2, 2, 2, 2, 2],
[2, 0, 0, 1, 1, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 0, 2],
[2, 0, 2, 2, 2, 0, 0, 2],
[0, 0, 2, 2, 2, 0, 0, 2],
[0, 1, 0, 0, 0, 0, 3, 2],
[0, 0, 0, 2, 0, 2, 2, 2]]

ex2 = [[2, 2, 2, 2, 2, 2, 2, 2],
[2, 0, 0, 1, 1, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 2],
[2, 1, 0, 0, 0, 0, 3, 2],
[2, 2, 2, 2, 2, 2, 2, 2]]

print compute_v_values(ex2)
#print get_optimal_policy(ex)