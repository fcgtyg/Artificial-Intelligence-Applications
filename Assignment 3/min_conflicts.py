import random
random.seed(1)


class CSP_Solver(object):

    def __init__(self):
        self.conflicts = {}
        self.conflicted_studs = []
        self.find_conflicts()
    # CSP Solver using min conflicts algorithm
    # See assignment description for details regarding the return value of each method

# Check the conflicts file and create a dictionary (Key = Person, Value= Key person's conflicts as a list of strings)
    def find_conflicts(self):
        file_in = open("conflicts.txt", "r")

        for line in file_in:
            line_ = line.replace("\n", "")
            line_ = line_.split("-")
            self.conflicts[line_[0]] = line_[1].split(",")

# Return given student's location in 2-D array
    def find_student_seat(self, student, arrangement):
        for i in range(len(arrangement)):
            for j in range(len(arrangement[i])):
                if arrangement[i][j] == student:
                    return i, j

# Return given student's conflicted neighbours
    def get_num_of_conflicts(self, student, arrangement):
        loc = tuple()

        for i in range(len(arrangement)):
            for j in range(len(arrangement[i])):
                if arrangement[i][j] == student:
                    loc = i, j

        count = 0
        i = loc[0]
        j = loc[1]

        if j != 0:
            if arrangement[i][j - 1] in self.conflicts[student]:
                count += 1
        if j != 3:
            if arrangement[i][j + 1] in self.conflicts[student]:
                count += 1
        if i != 3:
            if arrangement[i + 1][j] in self.conflicts[student]:
                count += 1
        if i != 0:
            if arrangement[i - 1][j] in self.conflicts[student]:
                count += 1
        if j != 0 and i != 3:
            if arrangement[i + 1][j - 1] in self.conflicts[student]:
                count += 1
        if j != 3 and i != 3:
            if arrangement[i + 1][j + 1] in self.conflicts[student]:
                count += 1
        if i != 0 and j != 0:
            if arrangement[i - 1][j - 1] in self.conflicts[student]:
                count += 1
        if i != 0 and j != 3:
            if arrangement[i - 1][j + 1] in self.conflicts[student]:
                count += 1

        if count != 0:
            self.conflicted_studs.append(student)
        return count

# Return the number of total conflicts, the value is cumulative (double-counting enabled).
    def get_total_conflicts(self, arrangement):
        count = 0
        for i in arrangement:
            for j in i:
                count += self.get_num_of_conflicts(j, arrangement)
        return count

# Returns a random 2-D dimensional array element.
    def find_a_random_student(self, arrangement):
        return arrangement[random.randint(0, 3)][random.randint(0, 3)]

# Returns the best arrangement for swapping two students randomly,
    # and finds chosen student's least number of conflicted arrangement.
    def get_best_arrangement(self, student, current_arrangement):
        if self.get_num_of_conflicts(student, current_arrangement) == 0:
            return current_arrangement
        coor = self.find_student_seat(student, current_arrangement)
        min_ = (current_arrangement,
                (self.get_num_of_conflicts(student, current_arrangement)
                 + 1000
                 )
                )
        for i in range(len(current_arrangement)):
            for j in range(len(current_arrangement[i])):
                b = self.swap(current_arrangement, coor, (i, j))
                a = self.get_num_of_conflicts(student, b) + self.get_num_of_conflicts(current_arrangement[i][j], b)
                if min_[1] > a:
                    min_ = b, a

        return min_[0]

# Returns the solution of the problem, zero-conflicted arrangement.
    def solve_csp(self, arrangement):

        check = self.get_total_conflicts(arrangement)

        while check>0:
            student = self.find_a_random_student(arrangement)
            arrangement = self.get_best_arrangement(student, arrangement)
            check = self.get_total_conflicts(arrangement)
        return arrangement
        pass

# Swapping function
    def swap(self, arrangement_, coor1, coor2):
        arrangement = []
        for i in range(len(arrangement_)):
            arrangement.append([])
            for j in arrangement_[i]:
                arrangement[i].append(j)
        temp = arrangement[coor1[0]][coor1[1]]
        arrangement[coor1[0]][coor1[1]] = arrangement[coor2[0]][coor2[1]]
        arrangement[coor2[0]][coor2[1]] = temp
        return arrangement
        

arr = [["Alan", "Bill", "Jack", "Jeff"],
       ["Dan", "Dave", "Jill", "Joe"],
       ["John", "Kim", "Sam", "Sue"],
       ["Mike", "Nick", "Tom", "Will"]]

a = CSP_Solver()
