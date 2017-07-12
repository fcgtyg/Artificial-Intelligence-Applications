from copy import deepcopy as dc


class Node():
    def __init__(self, x_coor, y_coor, reward = 0):
        self.name = x_coor, y_coor
        self.q_values = [None, None, None, None, None]  # [N, E, S, W, Exit]
        self.reward = reward
        self.v_val = 0
        self.policy = None

    def update_q(self, move=None, value=None):
        if move is not None and value is not None:
            self.q_values[move] = value
        self.v_val = max(self.q_values)
        self.policy = self.q_values.index(self.v_val)

states = {}


def compute_v_values(grid_config):
    global states
    results = []

    def iteration(states):
        for i in range(len(grid_config)):
            for j in range(len(grid_config[i])):

                if grid_config[i][j] == 2:
                    if (i,j) in states:
                        states[(i, j)] = compute_step(grid_config, states, states[(i,j)])
                    else:
                        state = Node(i, j)
                        state.reward = -10
                        state.q_values[4] = -10
                        state.v_val = -10
                        state.policy = 4
                        states[state.name] = (state)

                elif grid_config[i][j] == 1:
                    if (i,j) in states:
                        states[(i,j)] = compute_step(grid_config, states, states[(i,j)])
                    else:
                        state = Node(i, j)
                        state.reward = -5
                        state.q_values[4] = -5
                        state.v_val = -5
                        state.policy = 4
                        states[state.name] = (state)
                elif grid_config[i][j] == 3:
                    if (i,j) in states:
                        states[(i, j)] = compute_step(grid_config, states, states[(i,j)])
                    else:
                        state = Node(i, j)
                        state.reward = 30
                        state.q_values[4] = 30
                        state.v_val = 30
                        state.policy = 4
                        states[state.name] = (state)
                elif grid_config[i][j] == 0:
                    if (i,j) in states:
                        states[(i, j)] = compute_step(grid_config, states, states[(i,j)])
                    else:
                        state = Node(i, j)
                        state.reward = -1
                        states[state.name] = (state)
        return states
    i = 0

    while i<50:
        states = iteration(states)
        i += 1

    ############
    visualise = []
    for x in range(8):
        v = []
        for y in range(8):
            v.append(states[(x,y)].policy)
            print (x,y), states[(x,y)].q_values, states[(x,y)].v_val, states[(x,y)].policy
        visualise.append(v)
    for i in visualise:
        print i
    print "\n############\n"
    ############

    for i in states:
        results.append(((7-i[0], i[1]), states[i].v_val))
    results.sort()
    return results


def compute_step(grid_config, states, state, gamma=1, theta = 1):
    x,y = state.name
    if grid_config[x][y] != 0:
        #state.v_val = gamma * state.v_val + state.reward
        return state
    else:
        for i in range(len(state.q_values)):
            if i == 0:

                if (x-1,y) in states:
                    if x == 0:
                        a = 0.70 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        a = 0.70 * (gamma * states[(x - 1, y)].v_val + theta * states[(x - 1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        a = 0.70 * theta * -1
                    elif grid_config[x][y] == 1:
                        a = 0.70 * theta * -5
                    elif grid_config[x][y] == 2:
                        a = 0.70 * theta * -10
                    else:
                        a = 0.70 * theta * 30

                if (x, y-1) in states:
                    if y == 0:
                        b = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        b = 0.15 * (gamma * states[(x, y - 1)].v_val + theta * states[(x, y - 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        b = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        b = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        b = 0.15 * theta * -10
                    else:
                        b = 0.15 * theta * 30

                if (x, y+1) in states:
                    if y == 7:
                        c = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        c = 0.15 * (gamma * states[(x, y + 1)].v_val + theta * states[(x, y + 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        c = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        c = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        c = 0.15 * theta * -10
                    else:
                        c = 0.15 * theta * 30

                state.q_values[i] = a + b + c
                state.update_q()
            elif i == 1:

                if (x, y+1) in states:
                    if y == 7:
                        a = 0.70 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        a = 0.70 * (gamma * states[(x, y + 1)].v_val + theta * states[(x, y + 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        a = 0.7 * theta * -1
                    elif grid_config[x][y] == 1:
                        a = 0.7 * theta * -5
                    elif grid_config[x][y] == 2:
                        a = 0.7 * theta * -10
                    else:
                        a = 0.7 * theta * 30

                if (x-1, y) in states:
                    if x == 0:
                        b = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        b = 0.15 * (gamma * states[(x - 1, y)].v_val + theta * states[(x - 1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        b = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        b = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        b = 0.15 * theta * -10
                    else:
                        b = 0.15 * theta * 30

                if (x+1, y) in states:
                    if x == 7:
                        c = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        c = 0.15 * (gamma * (states[(x + 1, y)].v_val) + theta * states[(x + 1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        c = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        c = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        c = 0.15 * theta * -10
                    else:
                        c = 0.15 * theta * 30

                state.q_values[i] = a + b + c
                state.update_q()

            elif i == 2:

                if (x + 1, y) in states:
                    if x == 7:
                        a = 0.70 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        a = 0.70 * (gamma * states[(x + 1, y)].v_val + theta * states[(x + 1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        a = 0.7 * theta * -1
                    elif grid_config[x][y] == 1:
                        a = 0.7 * theta * -5
                    elif grid_config[x][y] == 2:
                        a = 0.7 * theta * -10
                    else:
                        a = 0.7 * theta * 30

                if (x, y - 1) in states:
                    if y == 0:
                        b = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        b = 0.15 * (gamma * states[(x, y - 1)].v_val + theta * states[(x, y - 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        b = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        b = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        b = 0.15 * theta * -10
                    else:
                        b = 0.15 * theta * 30

                if (x, y + 1) in states:
                    if y == 7:
                        c = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        c = 0.15 * (gamma * states[(x, y + 1)].v_val + theta * states[(x, y + 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        c = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        c = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        c = 0.15 * theta * -10
                    else:
                        c = 0.15 * theta * 30

                state.q_values[i] = a + b + c
                state.update_q()

            elif i == 3:

                if (x, y-1) in states:
                    if y == 0:
                        a = 0.70 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        a = 0.70 * (gamma * states[(x, y - 1)].v_val + theta * states[(x, y - 1)].reward)
                else:
                    if grid_config[x][y] == 0:
                        a = 0.7 * theta * -1
                    elif grid_config[x][y] == 1:
                        a = 0.7 * theta * -5
                    elif grid_config[x][y] == 2:
                        a = 0.7 * theta * -10
                    else:
                        a = 0.7 * theta * 30

                if (x-1, y) in states:
                    if x == 0:
                        b = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        b = 0.15 * (gamma * states[(x - 1, y)].v_val + theta * states[(x - 1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        b = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        b = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        b = 0.15 * theta * -10
                    else:
                        b = 0.15 * theta * 30

                if (x+1, y) in states:
                    if x == 7:
                        c = 0.15 * (gamma * states[(x,y)].v_val + theta * states[(x,y)].reward)
                    else:
                        c = 0.15 * (gamma * states[(x+1, y)].v_val + theta * states[(x+1, y)].reward)
                else:
                    if grid_config[x][y] == 0:
                        c = 0.15 * theta * -1
                    elif grid_config[x][y] == 1:
                        c = 0.15 * theta * -5
                    elif grid_config[x][y] == 2:
                        c = 0.15 * theta * -10
                    else:
                        c = 0.15 * theta * 30

                state.q_values[i] = a + b + c
                state.update_q()
    return state


def get_optimal_policy(grid_config):
    global states
    states = {}
    compute_v_values(grid_config)
    results = []
    for i in states:
        results.append(((7 - i[0], i[1]), states[i].policy))
    results.sort()
    return results

ex = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 1, 0, 1, 2],
    [2, 0, 1, 0, 0, 0, 1, 2],
    [2, 0, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 2, 2, 0, 0, 2],
    [0, 0, 2, 2, 2, 0, 0, 2],
    [0, 1, 0, 0, 0, 0, 3, 2],
    [0, 0, 0, 2, 0, 2, 2, 2]
    ]

ex2 = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 1, 0, 1, 2],
    [2, 0, 1, 0, 0, 0, 1, 2],
    [2, 0, 1, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 1, 0, 0, 0, 0, 3, 2],
    [2, 2, 2, 2, 2, 2, 2, 2]
    ]


ex3 = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 1, 0, 1, 2],
    [0, 0, 1, 0, 2, 0, 1, 2],
    [0, 0, 1, 0, 0, 0, 0, 2],
    [0, 2, 0, 0, 2, 2, 0, 2],
    [0, 0, 0, 2, 2, 2, 2, 2],
    [0, 1, 0, 0, 0, 0, 3, 2],
    [0, 2, 2, 2, 2, 2, 2, 2]
    ]
compute_v_values(ex2)
print ""
get_optimal_policy(ex)
print ""
get_optimal_policy(ex3)

