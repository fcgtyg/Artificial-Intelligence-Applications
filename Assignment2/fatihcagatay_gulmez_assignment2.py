# coding=utf-8
# author Fatih Cagatay Gulmez


# The queue data structure specialized for this project.


from math import sqrt

class MinPriorityQueue:
    def __init__(self):
        self.content = []
        self.min = None

    def __str__(self):
        word = ""
        for i in self.content:
            word = word + i[0].__str__() + " | "

        return "[" + word[0:len(word)-2] + "]"

    def enqueue(self, item, val = None):
        self.content.append((item,val))
        if len(self.content) == 1:
            self.min = 0
        else:
            if self.content[self.min][1] >= val:
                self.min = len(self.content)-1

    def dequeue(self):
        if len(self.content) == 0:
            return None
        try:
            popped = self.content.pop(self.min)
        except:
            return
        mini = popped
        for i in range(len(self.content)-1, -1, -1):
            if mini[1] >= self.content[i][1]:
                mini = self.content[i]
                self.min = i
        return popped

    def size(self):
        return len(self.content)

    def get(self, index):
        return self.content[index]


class Node:
    def __init__(self, item, parent):
        self.item = item
        self.parent = parent

    def __str__(self):
        return self.item.__str__()


# Initialize the queue.
analyse = MinPriorityQueue()


blue_one = [0]
blue_two = [0]
blue_thr = [0]
blue_fou = [0]
blue_fiv = [0]
blue_six = [0]

green_hor = [0,0]
green_ver = [0,0]

red = [0,0,0,0]

empty = [0,0]

path = []


# Checking if the empty tile is in middle.
def goal_check(state):
    return state[2][0] == "4" and state[2][1] == "4" and state[3][1] == "4" and state[3][0] == "4"


def find_blocks(state):
    greens = {}
    g = 0
    r = 0
    e = 0
    for i in range(len(state)):
        greens[i] = []
        for j in range(len(state[i])):
            if state[i][j] == 1:
                if len(blue_one) == 0:
                    blue_one[0]=(i, j)
                elif len(blue_two) == 0:
                    blue_two[0]=(i, j)
                elif len(blue_thr) == 0:
                    blue_thr[0]=(i, j)
                elif len(blue_fou) == 0:
                    blue_fou[0]=(i, j)
                elif len(blue_fiv) == 0:
                    blue_fiv[0]=(i, j)
                else:
                    blue_six.append((i, j))
            elif state[i][j] == 2:
                greens[i].append(j)
            elif state[i][j] == 4:
                red[r]=(i, j)
                r += 1

            elif state[i][j] == 0:
                empty[e]=(i, j)
                e+=1
    for row in greens:
        if len(greens[row]) == 3:
            if greens[row][1] - greens[row][0] == 1:
                green_hor[0] = (row, greens[row][0])
                green_hor[1] = (row, greens[row][1])
                if g == 0:
                    green_ver[0]=(row, greens[row][2])
                    g = 1
                else:
                    green_ver[1]=(row, greens[row][2])
            elif greens[row][2] - greens[row][1] == 1:
                green_hor[0] = (row, row[1])
                green_hor[1] = (row, row[2])
                if g == 0:
                    green_ver[0] = (row, row[1])
                    g = 1
                else:
                    green_ver[1] = (row, row[1])

        elif len(greens[row]) == 1:
            if g == 1:
                green_ver[1] = (row, greens[row][0])
            else:
                green_ver[0] = (row, greens[row][0])
                g = 1

        elif len(greens[row]) == 2:
            green_hor[0]=(row, greens[row][0])
            green_hor[1]=(row, greens[row][1])


def get_item(processing, x, y):
    return processing[x][y]


def swap(processing, x_in, y_in, x_next, y_next):
    environment_next = list()
    for i in processing:
        temp_list = []
        for j in i:
            temp_list.append(j)
        environment_next.append(temp_list)
    temp = get_item(environment_next, x_next, y_next)
    environment_next[x_next][y_next] = environment_next[x_in][y_in]
    environment_next[x_in][y_in] = temp
    return environment_next


def scenarios00h(up1 = None, up2 = None, dw1 = None, dw2 = None, lf1 = None, lf2 = None, rg1 = None, rg2 = None, mid = None, check = None):
    parent = []
    successors = []
    for i in mid:
        a = []
        for j in i:
            a.append(j)
        parent.append(a)

    if check == "up":
        if up1 == 4 and up2 == 4:
            mid = swap(mid, red[0][0], red[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[1][0], red[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, red[0][0], red[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[1][0], red[1][1], empty[1][0], empty[1][1])

        if up1 == 1:
            mid = swap(mid, empty[0][0]-1, empty[0][1], empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0] - 1, empty[0][1], empty[0][0], empty[0][1])

        if up2 == 1:
            mid = swap(mid, empty[1][0]-1, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0] - 1, empty[1][1], empty[1][0], empty[1][1])

        if up1 == 2 and up2 == 2:
            if ((empty[0][0]-1, empty[0][1]) in green_hor) and ((empty[1][0]-1, empty[1][1]) in green_hor):
                mid = swap(mid, green_hor[0][0], green_hor[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_hor[1][0], green_hor[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, green_hor[0][0], green_hor[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_hor[1][0], green_hor[1][1], empty[1][0], empty[1][1])

        if ((empty[0][0]-1, empty[0][1]) in green_ver) and up1 == 2:
                mid = swap(mid, empty[0][0]-2, empty[0][1], empty[0][0], empty[0][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[0][0] - 2, empty[0][1], empty[0][0], empty[0][1])

        if (empty[1][0]-1, empty[1][1]) in green_ver and up2 == 2:
                mid = swap(mid, empty[1][0]-2, empty[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[1][0] - 2, empty[1][1], empty[1][0], empty[1][1])

    elif check == "down":
        if dw1 == 1:
            mid = swap(mid, empty[0][0] + 1, empty[0][1], empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0][0] + 1, empty[0][1], empty[0][0], empty[0][1])

        if dw2 == 1:
            mid = swap(mid, empty[1][0] + 1, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[1][0] + 1, empty[1][1], empty[1][0], empty[1][1])

        if dw1 == 4 and dw2 == 4:
            mid = swap(mid, red[2][0], red[2][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[3][0], red[3][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, red[2][0], red[2][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[3][0], red[3][1], empty[1][0], empty[1][1])

        if dw1 == 2 and dw2 == 2:
            if ((empty[0][0]+1, empty[0][1]) in green_hor) and ((empty[1][0]+1, empty[1][1]) in green_hor):
                mid = swap(mid, green_hor[0][0], green_hor[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_hor[1][0], green_hor[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, green_hor[0][0], green_hor[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_hor[1][0], green_hor[1][1], empty[1][0], empty[1][1])

        if ((empty[0][0]+1, empty[0][1]) in green_ver) and dw1 == 2:
                mid = swap(mid, empty[0][0]+2, empty[0][1], empty[0][0], empty[0][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[0][0] + 2, empty[0][1], empty[0][0], empty[0][1])

        if (empty[1][0]+1, empty[1][1]) in green_ver and dw2 == 2:
                mid = swap(mid, empty[1][0]+2, empty[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[1][0] + 2, empty[1][1], empty[1][0], empty[1][1])

    elif check == "left":
        if lf1 == 1:
            mid = swap(mid, empty[0][0], empty[0][1] - 1, empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0], empty[0][1] - 1, empty[0][0], empty[0][1])

        if lf2 == 1:
            mid = swap(mid, empty[0][0], empty[0][1] - 1, empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0], empty[0][1] - 1, empty[0][0], empty[0][1])
        if empty[0][1] >= 2 and (lf1 == 2 or lf2 == 2):
            mid = swap(mid, empty[0][0], empty[0][1] - 2, empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0], empty[1][1] - 2, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0], empty[0][1] - 2, empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0], empty[1][1] - 2, empty[1][0], empty[1][1])

    elif check == "right":
        if rg1 == 1:
            mid = swap(mid, empty[1][0], empty[1][1] + 1, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0], empty[1][1] + 1, empty[1][0], empty[1][1])

        if rg2 == 1:
            mid = swap(mid, empty[1][0], empty[1][1] + 1, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0], empty[1][1] + 1, empty[1][0], empty[1][1])
        if empty[1][1] < 2 and (rg1 == 2 or rg2 == 2):
            mid = swap(mid, empty[0][0], empty[0][1] + 2, empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0], empty[1][1] + 2, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0], empty[0][1] + 2, empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0], empty[1][1] + 2, empty[1][0], empty[1][1])
    return successors


def scenarios00v(up1 = None, up2 = None, dw1 = None, dw2 = None, lf1 = None, lf2 = None, rg1 = None, rg2 = None, mid = None, check = None):
    successors = []
    parent = []
    for i in mid:
        a = []
        for j in i:
            a.append(j)
        parent.append(a)

    if check == "left":
        if lf1 == 4 and lf2 == 4:
            mid = swap(mid, red[0][0], red[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[2][0], red[2][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, red[0][0], red[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[1][0], red[1][1], empty[1][0], empty[1][1])

        if lf1 == 1:
            mid = swap(mid, empty[0][0], empty[0][1]-1, empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0], empty[0][1]-1, empty[0][0], empty[0][1])

        if lf2 == 1:
            mid = swap(mid, empty[1][0], empty[1][1]-1, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0] - 1, empty[1][1], empty[1][0], empty[1][1])

        if lf1 == 2 and lf2 == 2:
            if ((empty[0][0], empty[0][1]-1) in green_ver) and ((empty[1][0], empty[1][1]-1) in green_ver):
                mid = swap(mid, green_ver[0][0], green_ver[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_ver[1][0], green_ver[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, green_ver[0][0], green_ver[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_ver[1][0], green_ver[1][1], empty[1][0], empty[1][1])

        if ((empty[0][0], empty[0][1]-1) in green_hor) and lf1 == 2:
                mid = swap(mid, empty[0][0], empty[0][1]-2, empty[0][0], empty[0][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[0][0], empty[0][1]-2, empty[0][0], empty[0][1])

        if (empty[1][0], empty[1][1]-1) in green_hor and lf2 == 2:
                mid = swap(mid, empty[1][0], empty[1][1]-2, empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[1][0], empty[1][1]-2, empty[1][0], empty[1][1])

    elif check == "right":
        if rg1 == 1:
            mid = swap(mid, empty[0][0], empty[0][1]+1, empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0][0], empty[0][1]+1, empty[0][0], empty[0][1])

        if rg2 == 1:
            mid = swap(mid, empty[1][0], empty[1][1]+1, empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[1][0], empty[1][1]+1, empty[1][0], empty[1][1])

        if rg1 == 4 and rg2 == 4:
            mid = swap(mid, red[1][0], red[1][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[3][0], red[3][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, red[1][0], red[1][1], empty[0][0], empty[0][1])
            mid = swap(mid, red[3][0], red[3][1], empty[1][0], empty[1][1])

        if rg1 == 2 and rg2 == 2:
            if ((empty[0][0], empty[0][1]+1) in green_ver) and ((empty[1][0], empty[1][1]+1) in green_ver):
                mid = swap(mid, green_ver[0][0], green_ver[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_ver[1][0], green_ver[1][1], empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, green_ver[0][0], green_ver[0][1], empty[0][0], empty[0][1])
                mid = swap(mid, green_ver[1][0], green_ver[1][1], empty[1][0], empty[1][1])

        if ((empty[0][0], empty[0][1]+1) in green_hor) and rg1 == 2:
                mid = swap(mid, empty[0][0], empty[0][1]+2, empty[0][0], empty[0][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[0][0], empty[0][1]+2, empty[0][0], empty[0][1])

        if (empty[1][0], empty[1][1]+1) in green_hor and rg2 == 2:
                mid = swap(mid, empty[1][0], empty[1][1]+2, empty[1][0], empty[1][1])
                analyse.enqueue(Node(mid, parent), 1)
                successors.append(mid)
                goal_check(mid)
                mid = swap(mid, empty[1][0], empty[1][1]+2, empty[1][0], empty[1][1])

    elif check == "up":
        if up1 == 1:
            mid = swap(mid, empty[0][0]-1, empty[0][1], empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0]-1, empty[0][1] - 1, empty[0][0], empty[0][1])

        if up2 == 1:
            mid = swap(mid, empty[0][0]-1, empty[0][1], empty[0][0], empty[0][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0]-1, empty[0][1], empty[0][0], empty[0][1])
        if empty[0][0] >= 2 and (up1 == 2 or up2 == 2):
            mid = swap(mid, empty[0][0]-2, empty[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0]-2, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0]-2, empty[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0]-2, empty[1][1], empty[1][0], empty[1][1])

    elif check == "down":
        if dw1 == 1:
            mid = swap(mid, empty[1][0]+1, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0]+1, empty[1][1], empty[1][0], empty[1][1])
        if dw2 == 1:
            mid = swap(mid, empty[1][0]+1, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[1][0]+1, empty[1][1], empty[1][0], empty[1][1])
        if empty[1][0] < 2 and (dw1 == 2 or dw2 == 2):
            mid = swap(mid, empty[0][0]+2, empty[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0]+2, empty[1][1], empty[1][0], empty[1][1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            goal_check(mid)
            mid = swap(mid, empty[0][0] + 2, empty[0][1], empty[0][0], empty[0][1])
            mid = swap(mid, empty[1][0] + 2, empty[1][1], empty[1][0], empty[1][1])
    return successors


def scenariosd(empty = None, up = None, dw = None, lf = None, rg = None, mid = None):
    successors = []
    parent = []

    for i in mid:
        a = []
        for j in i:
            a.append(j)
        parent.append(a)

    if up == 1:
        mid = swap(mid, empty[0] - 1, empty[1], empty[0], empty[1])
        analyse.enqueue(Node(mid, parent), 1)
        successors.append(mid)
        mid = swap(mid, empty[0] - 1, empty[1], empty[0], empty[1])

    if up == 2:
        if (empty[0]-1, empty[1]) in green_ver:
            mid = swap(mid, empty[0]-2, empty[1], empty[0], empty[1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0] - 2, empty[1], empty[0], empty[1])

    if dw == 1:
        mid = swap(mid, empty[0] + 1, empty[1], empty[0], empty[1])
        analyse.enqueue(Node(mid, parent), 1)
        successors.append(mid)
        mid = swap(mid, empty[0] + 1, empty[1], empty[0], empty[1])

    if dw == 2:
        if (empty[0]+1, empty[1]) in green_ver:
            mid = swap(mid, empty[0]+2, empty[1], empty[0], empty[1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0] - 2, empty[1], empty[0], empty[1])

    if lf == 1:
        mid = swap(mid, empty[0], empty[1] - 1, empty[0], empty[1])
        analyse.enqueue(Node(mid, parent), 1)
        successors.append(mid)
        mid = swap(mid, empty[0], empty[1] - 1, empty[0], empty[1])

    if lf == 2:
        if (empty[0], empty[1]-1) in green_hor:
            mid = swap(mid, empty[0], empty[1]-2, empty[0], empty[1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0], empty[1]-2, empty[0], empty[1])

    if rg == 1:
        mid = swap(mid, empty[0], empty[1] + 1, empty[0], empty[1])
        analyse.enqueue(Node(mid, parent), 1)
        successors.append(mid)
        mid = swap(mid, empty[0], empty[1] + 1, empty[0], empty[1])

    if rg == 2:
        if (empty[0], empty[1]+1) in green_hor:
            mid = swap(mid, empty[0], empty[1]+2, empty[0], empty[1])
            analyse.enqueue(Node(mid, parent), 1)
            successors.append(mid)
            mid = swap(mid, empty[0], empty[1]+2, empty[0], empty[1])
    return successors


def get_successor(initial_state):
    successors = []

    up1 = None
    up2 = None
    dw1 = None
    dw2 = None
    lf1 = None
    lf2 = None
    rg1 = None
    rg2 = None

    checks = ["up", "down", "left", "right"]

    find_blocks(initial_state)
    e1x = empty[0][0]
    e1y = empty[0][1]
    e2x = empty[1][0]
    e2y = empty[1][1]
    if e1x != 0:
        up1 = initial_state[e1x-1][e1y]
    if e2x != 0:
        up2 = initial_state[e2x-1][e2y]
    if e1x != 3:
        dw1 = initial_state[e1x+1][e1y]
    if e2x != 3:
        dw2 = initial_state[e2x+1][e2y]
    if e1y != 0:
        lf1 = initial_state[e1x][e1y-1]
    if e2y != 0:
        lf2 = initial_state[e2x][e2y-1]
    if e1y != 3:
        rg1 = initial_state[e1x][e1y+1]
    if e2y != 3:
        rg2 = initial_state[e2x][e2y+1]

    if lf2 == 0 and rg1 == 0:
        for check in checks:
            mid = []
            for i in initial_state:
                a = []
                for j in i:
                    a.append(j)
                mid.append(a)
            successors.extend(scenarios00h(up1=up1, up2=up2, mid=mid, check=check))
            successors.extend(scenarios00h(dw1=dw1, dw2=dw2, mid=mid, check=check))
            successors.extend(scenarios00h(lf1=lf1, lf2=lf2, mid=mid, check=check))
            successors.extend(scenarios00h(rg1=rg1, rg2=rg2, mid=mid, check=check))

    elif dw1 == up2 and up2 == 0:
        for check in checks:
            mid = []
            for i in initial_state:
                a = []
                for j in i:
                    a.append(j)
                mid.append(a)
            successors.extend(scenarios00v(up1=up1, up2=up2, mid=mid, check=check))
            successors.extend(scenarios00v(dw1=dw1, dw2=dw2, mid=mid, check=check))
            successors.extend(scenarios00v(lf1=lf1, lf2=lf2, mid=mid, check=check))
            successors.extend(scenarios00v(rg1=rg1, rg2=rg2, mid=mid, check=check))
    else:
        mid = []
        for i in initial_state:
            a = []
            for j in i:
                a.append(j)
            mid.append(a)
        successors.extend(scenariosd(empty=empty[0], up=up1, dw=dw1, rg=rg1, lf=lf1, mid=mid))
        successors.extend(scenariosd(empty=empty[1], up=up2, dw=dw2, rg=rg2, lf=lf2, mid=mid))
    return successors


def uniform_cost_search(initial_state):
    looked = []
    first = Node(initial_state, None)
    analyse.enqueue(first, 100)
    goal = False
    while (not goal) and (len(analyse.content)>0):
        item = analyse.dequeue()
        if item is not None:

            processing = item[0].item
            goal = goal_check(processing)
            if processing not in looked:
                looked.append(processing)
                get_successor(processing)

        else:
            break
    while(processing.parent != None):
        path.append[processing]
        processing = processing.parent

    return path.reverse()


def a_star_heuristic(state):
    find_blocks(state)
    return sqrt(((red[2][0] - 4)**2)+((red[2][1] - 0)**2))


problem = [
[1, 4, 4, 1], # [1, 2, 1, 1]
[1, 4, 4, 2], # [1, 2, 4, 4]
[1, 1, 1, 2], # [2, 2, 4, 4]
[2, 2, 0, 0]  # [1, 1, 0, 0]
           ]

#print get_successor(problem)

#uniform_cost_search(problem)

#print a_star_heuristic(problem)