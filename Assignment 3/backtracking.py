from copy import deepcopy
import time
class Node:
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent



class Stack:
    # author Fatih Cagatay Gulmez
    def __init__(self):
        self.content = list()
        pass

    def __str__(self):
        return self.content.__str__()

    def put(self, item):
        self.content.append(item)

    def pop(self):
        if len(self.content) == 0:
            return None
        else:
            return self.content.pop()

    def size(self):
        return len(self.content)

    def get(self, index):
        return self.content[index]


class CSP_Solver(object):
    # CSP Solver using backtracking search
    # See assignment description for details regarding the return value of each method
    def __init__(self):
        self.conflicts = dict()
        self.liste = []
        self.stack = Stack()
        self.find_conflicts()
        self.remain = []

    def find_conflicts(self):
        lines = open("conflicts.txt", "r")
        liste = []
        for line in lines:
            line = line.replace("\n", "")
            sep_line = line.split("-")
            self.conflicts[sep_line[0]] = sep_line[1].split(",")
            liste.append(sep_line[0])
        liste.sort()
        liste.reverse()
        self.liste = liste

    def is_conflict(self, arrangement, x, y, item):
        check = self.conflicts[item]
        if x!=0:
            if arrangement[x-1][y] in check:
                return True
            if y!=0:
                if arrangement[x-1][y-1] in check:
                    return True
            if y!= 3 and arrangement[x-1][y+1] in check:
                return True
        if x!=3:
            if arrangement[x+1][y] in check:
                return True
            if y!=0:
                if arrangement[x+1][y-1] in check:
                    return True
            if y != 3:
                if arrangement[x+1][y+1] in check:
                    return True
        if y!=0:
            if arrangement[x][y-1] in check:
                return True
        if y!=3:
            if arrangement[x][y+1] in check:
                return True
        return False

    def backtracking_search_2(self, arrangement):
        temp = []
        temp_x = {}
        x, y = 0, 0
        while x<=len(arrangement):
            while y<=len(arrangement[x]):
                if (x, y) not in temp_x:
                    temp_x[(x, y)] = []
                if len(self.liste) == 0:
                    if len(temp) == 0:
                        return arrangement
                    else:
                        self.liste.extend(temp)
                        self.liste.reverse()
                    if arrangement[x][y] != "":
                        self.liste.append(arrangement[x][y])
                    arrangement[x][y] = ""
                    temp = []
                    if y != 0:
                        y -= 1
                        temp_x[(x, y+1)] = []
                    elif x != 0:
                        x -= 1
                        y = 3
                        temp_x[(x+1,0)] = []
                    else:
                        return "No solution"
                item = self.liste.pop()
                check = self.is_conflict(arrangement, x, y, item)
                if (not check) and (item not in temp_x[(x, y)]):
                    if arrangement[x][y] != "":
                        temp.append(arrangement[x][y])
                        temp_x[(x, y)].append(arrangement[x][y])
                    arrangement[x][y] = item
                    if y != 3:
                        y += 1
                        temp_x[(x, y - 1)] = []
                    elif x != 3:
                        x += 1
                        y = 0
                        temp_x[(x-1, 3)] = []
                    else:
                        return arrangement
                elif check:
                    temp.append(item)


    def backtracking_search(self, arrangement):
        print "\tPlease be patient, it will solve the question, DFS takes long time " \
              "\n (Given example took around 1 minute in Samsung Laptops.)"
        cp_arr = deepcopy(arrangement)
        parent = Node(cp_arr)
        while self.steps(parent) == 0:
            parent = self.stack.pop()
            self.steps(parent)
        return parent.item

    def steps(self, node):
        arrangement = deepcopy(node.item)
        restricted=[]
        k = 0
        for i in range (len(arrangement)):
            for j in range (len(arrangement[i])):
                if arrangement[i][j] == "":
                    break
                else:
                    restricted.append(arrangement[i][j])
                    if len(restricted) == len(self.liste):
                        return 1
            if arrangement[i][j] == "":
                break
        for k in self.liste:
            if k not in restricted:
                if not self.is_conflict(arrangement, i, j, k):
                    arrangement[i][j] = k
                    restricted.append(k)
                    self.stack.put(Node(deepcopy(arrangement), node))
                    arrangement[i][j] = ""
        return 0

    def forward_checking(self, assignment, domain_dict):
        x,y = assignment[0]
        person = assignment[1][0]
        domain_dict[(x, y)] = []
        domain_dict[(x,y)].append(person)

        if x != 0 and y != 0 and person in domain_dict[(x-1, y-1)]:
            domain_dict[(x-1,y-1)].remove(person)
            for i in domain_dict[(x-1, y-1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x-1, y-1)].remove(i)

        if x != 0 and person in domain_dict[(x - 1, y)]:
            domain_dict[(x - 1, y)].remove(person)
            for i in domain_dict[(x-1, y)]:
                if i in self.conflicts[person]:
                    domain_dict[(x-1, y)].remove(i)

        if x != 0 and y != 3 and person in domain_dict[(x - 1, y + 1)]:
            domain_dict[(x - 1, y + 1)].remove(person)
            for i in domain_dict[(x-1, y + 1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x-1, y + 1)].remove(i)

        if x != 3 and y != 0 and person in domain_dict[(x + 1, y - 1)]:
            domain_dict[(x + 1, y - 1)].remove(person)
            for i in domain_dict[(x + 1, y - 1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x+1, y-1)].remove(i)

        if x != 3 and person in domain_dict[(x + 1, y)]:
            domain_dict[(x + 1, y)].remove(person)
            for i in domain_dict[(x+1, y)]:
                if i in self.conflicts[person]:
                    domain_dict[(x+1, y)].remove(i)

        if x != 3 and y != 3 and person in domain_dict[(x + 1, y + 1)]:
            domain_dict[(x + 1, y + 1)].remove(person)
            for i in domain_dict[(x+1, y+1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x+1, y+1)].remove(i)

        if y != 0 and person in domain_dict[(x, y - 1)]:
            domain_dict[(x, y - 1)].remove(person)
            for i in domain_dict[(x, y-1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x, y-1)].remove(i)

        if y != 3 and person in domain_dict[(x, y + 1)]:
            domain_dict[(x, y + 1)].remove(person)
            for i in domain_dict[(x, y+1)]:
                if i in self.conflicts[person]:
                    domain_dict[(x, y+1)].remove(i)

        return domain_dict


    def backtracking_with_forward_checking(self):
        pass

    def backtracking_with_ac3(self):
        pass

a = CSP_Solver()

arr = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""]
       ]

# print a.backtracking_search(arr)
assin = (0, 0), ["Alan"]

dic = {(0, 0): ["Alan", "Bill", "Dan", "Dave", "Jack", "Jeff", "Jill", "Joe", "John", "Kim", "Mike", "Nick", "Sam", "Sue", "Tom", "Will"],
       (0,1): ["Alan", "Bill", "Dan", "Dave", "Jack", "Jeff", "Jill", "Joe", "John", "Kim", "Mike", "Nick", "Sam", "Sue", "Tom", "Will"],
       (1,0): ["Alan", "Bill", "Dan", "Dave", "Jack", "Jeff", "Jill", "Joe", "John", "Kim", "Mike", "Nick", "Sam", "Sue", "Tom", "Will"],
       (1,1): ["Alan", "Bill", "Dan", "Dave", "Jack", "Jeff", "Jill", "Joe", "John", "Kim", "Mike", "Nick", "Sam", "Sue", "Tom", "Will"]}

start = time.time()
print a.backtracking_search(arr)
print time.time() - start