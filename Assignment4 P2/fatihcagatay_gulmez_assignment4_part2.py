from collections import deque
from math import log

class Node():
    def __init__(self, environment, green, red, value, level, parent=None, end=False):
        self.content = (environment, green, red)
        self.parent = parent
        self.level = level
        self.status = end
        self.value = value
        pass

    def __str__(self):
        out_parent = self.parent
        while True:
            if out_parent is None:
                break
            if out_parent.level == 1:
                break
            out_parent = out_parent.parent

        out = {"Expected State (Green, Red)": (self.content[1],self.content[2]),
               "Next Move (Green, Red)" : (out_parent.content[1],out_parent.content[2]) if out_parent is not None else None,
               "Level" : self.level,
               "Expected Minimax" : self.value}
        return out.__str__()


def game_tree_iteration(grid_config, node, queue, ):
    green = node.content[1]
    red = node.content[2]
    parent = node
    gx, gy = green
    rx, ry = red

    red_valid = []
    green_valid = []

    if gx != 0:green_valid.append("N")
    if gx != 7:green_valid.append("S")

    if gy != 0:green_valid.append("W")
    if gy != 7:green_valid.append("E")

    if rx != 0:red_valid.append("N")
    if rx != 7:green_valid.append("S")

    if ry != 0:red_valid.append("W")
    if ry != 7:red_valid.append("E")

    for g in green_valid:
        if g == "W":
            gx_ = gx
            gy_ = gy - 1
        elif g == "E":
            gx_ = gx
            gy_ = gy + 1
        elif g == "S":
            gx_ = gx + 1
            gy_ = gy
        elif g == "N":
            gx_ = gx - 1
            gy_ = gy

        if (gx_,gy_) == (rx, ry):
            queue.appendleft(Node(grid_config, (gx_, gy_), (rx, ry),
                              -50,parent.level+1 if parent is not None else 0, parent=parent if parent is not None else None, end=True))
        else:
            for r in red_valid:
                if r == "W":
                    rx_ = rx
                    ry_ = ry - 1
                elif r == "E":
                    rx_ = rx
                    ry_ = ry + 1
                elif r == "S":
                    rx_ = rx + 1
                    ry_ = ry
                elif r == "N":
                    rx_ = rx - 1
                    ry_ = ry

                if (gx_,gy_) != (rx, ry) or (gx_,gy_) != (rx_, ry_) or (rx,ry) != (gx,gy):
                    reward = get_reward(grid_config, gx_, gy_)
                    queue.appendleft(Node(grid_config, (gx_, gy_), (rx_, ry_),
                                      reward[0],parent.level+1 if parent is not None else 0, parent=parent if parent is not None else None, end=reward[1]))
                else:
                    queue.appendleft(Node(grid_config, (gx_, gy_), (rx_, ry_),
                                      -50, parent.level + 1, parent=parent if parent is not None else None, end=True))
    return queue


def get_reward(grid_config, x, y):
    rewards = {0: 0, 1: -5, 2: -10, 3: 30}
    reward = rewards[grid_config[x][y]]
    return reward, False if reward == 0 else True


def emm_no_prunning(grid_config, depth_limit):
    """
    Input = 2D Array of environment or state, A depth limit
    Return = Topmost Max node
    Procedure = Construct a game tree of the given depth. Assume non-terminal states have a value of 0.
    """
    count = 0
    queue = deque()
    root = Node(grid_config, (1,1), (6,1), None, 0)
    queue.append(root)
    while len(queue)!=0:
        current = queue.pop()
        if current.status:
            queue.appendleft(current)
        if current.level == depth_limit:
            queue.append(current)
            break
        if not current.status and current.level != depth_limit:
            game_tree_iteration(grid_config, current, queue)

    depth=1
    while 2**depth < len(queue):
        depth+=1

    maximum = True if depth%2 == 1 else False

    while len(queue) > 1:
        temp = deque()
        while len(queue)>1:
            a = queue.pop()
            b = queue.pop()
            if maximum:
                if a.value>b.value:
                    temp.appendleft(a)
                else:
                    temp.appendleft(b)
            else:
                if a.value>b.value:
                    temp.appendleft(b)
                else:
                    temp.appendleft(a)
            if len(queue)== 1:
                temp.appendleft(queue.pop())
            count+=1
        queue = temp
        maximum = not maximum

    return queue.pop().value


def emm_ab_prunning(grid_config, depth_limit):
    """
     Input = 2D Array of environment or state, A depth limit
     Return = Total number of nodes.
     Procedure = Construct a game tree, apply alpha-beta pruning and find minimax nodes.
    """
    count = 0
    queue = deque()
    root = Node(grid_config, (1, 1), (6, 1), None, 0)
    queue.append(root)
    while len(queue) != 0:
        current = queue.pop()
        if current.status:
            queue.appendleft(current)
        if current.level == depth_limit:
            queue.append(current)
            break
        if not current.status and current.level != depth_limit:
            game_tree_iteration(grid_config, current, queue)

    depth = 1
    while 2 ** depth < len(queue):
        depth += 1

    maximum = True if depth % 2 == 1 else False

    while len(queue) > 1:
        branch = False
        temp = deque()
        while len(queue) > 1:
            a = queue.pop()
            b = queue.pop()
            if not branch:
                if maximum:
                    cutoff = 9999
                else:
                    cutoff = -9999

            if maximum:
                if cutoff>a.value:
                    if a.value > b.value:
                        temp.appendleft(a)
                        cutoff = a.value
                    else:
                        temp.appendleft(b)
                        cutoff = b.value
                    count +=1
            else:
                if cutoff<a.value:
                    if a.value > b.value:
                        temp.appendleft(b)
                        cutoff = b.value
                    else:
                        temp.appendleft(a)
                        cutoff = a.value
                count+=1

            if len(queue) == 1:
                temp.appendleft(queue.pop())
            branch = not branch
        queue = temp
        maximum = not maximum

    return count


def approximate_q_learning():
    """
    Input = 
    Return = w's
    Procedure = w1,w2:= 1,1 ; learning rate = 0.1; Q(s, a) := w 1 *f 1 (s, a) + w 2 *f 2 (s, a) 
    """
    pass

test = [
[2, 2, 2, 2, 2, 2, 2, 2],
[2, 0, 0, 1, 1, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 1, 2],
[2, 0, 1, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 2],
[2, 1, 0, 0, 0, 0, 3, 2],
[2, 2, 2, 2, 2, 2, 2, 2]
       ]

print emm_ab_prunning(test, 5)
print emm_no_prunning(test, 5)

