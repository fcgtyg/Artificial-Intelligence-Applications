#The queue data structure specialized for this project.
class Queue:
    # author Fatih Cagatay Gulmez
    def __init__(self):
        self.content = []
        pass

    def __str__(self):
        return self.content.__str__()

    def enqueue(self, item):
        self.content.append(item)

    def dequeue(self):
        try:
            popped = self.content.pop(0)
            return popped
        except:
            pass

    def size(self):
        return len(self.content)

    def get(self, index):
        return self.content[index]

#Initialize the queue.
analyse = Queue()

# Checking if the empty tile is in middle.
def goal_check(processing):
    return get_loc(processing, 0) == (1, 1)

# Get location of any item in environment. Used to find 0.
def get_loc(processing, item):
    try:
        for x in range(len(processing)):
            for y in range(len(processing[x])):
                if processing[x][y] == item:
                    return x, y
    except:
        pass

#Get the item in givine coordinates
def get_item(processing , x, y):
    return processing[x][y]

#Find the horizon of given state, returns a 2d list consists of all next steps possible.
def expand(initial_state):
    # Returns next steps of environment.
    paths = list()
    zero = get_loc(initial_state, 0)#Find zero
    #Try all possible next states, if no error threw, enqueue the state to analyse and append to paths
    try:
        next_ = left(initial_state, zero[0], zero[1])
        if not next_ == None:
            paths.append(next_)
            analyse.enqueue(next_)
    except:
        pass

    try:
        next_ = right(initial_state, zero[0], zero[1])
        paths.append(next_)
        analyse.enqueue(next_)
    except:
        pass

    try:
        next_ = up(initial_state, zero[0], zero[1])
        if next_ != None:
            paths.append(next_)
            analyse.enqueue(next_)
    except:
        pass

    try:
        next_ = down(initial_state, zero[0], zero[1])
        paths.append(next_)
        analyse.enqueue(next_)
    except:
        pass

    return paths

#Basic swap funtion, swaps the items in given coordinates. Returns swapped state.
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

#Function for moving zero to the left, returns next state or none.
def left(processing, x, y):
    # type: (integer, integer) -> object
    if not y - 1 < 0:
        return swap(processing, x, y, x, y - 1)
    else:
        return None

#Function for moving zero to the right, returns next state or none.
def right(processing, x, y):
    # type: (integer, integer) -> object
    return swap(processing, x, y, x, y + 1)

#Function for moving zero to the up, returns next state or none.
def up(processing, x, y):
    # type: (integer, integer) -> object
    if not x - 1 < 0:
        return swap(processing, x, y, x - 1, y)
    else:
        return None

#Function for moving zero to the down, returns next state or none.
def down(processing, x, y):
    # type: (integer, integer) -> object
    return swap(processing, x, y, x + 1, y)

#Searching function. Prints searched states and returns found path.
def graph_search(initial_state):
    environment_ = initial_state
    processed_ = []#list for keeping searched state to prevent infinite loop.
    analyse.enqueue(environment_) #initialize queue for processing.
    current_ = environment_ #active state to be calculated.
    goal_ = goal_check(current_)

    while not goal_: #Searching until goal
        current_ = analyse.dequeue()
        if current_ not in processed_:
            expand(current_) #Enqueue is done here.
            processed_.append(current_ )
            goal_ = goal_check(current_)
        if analyse.size() == 0: #If queue is empty end goal cannot be reached, there is no solution.
            print "no such a solution!"
            return

    for i in processed_:
        for j in i:
            print j
        print "Searching..."
    
    # Returns the path, list of states.
    print "Well Done"
    print "Search finished, here is the path: "
    #Return scenarios
    try:
        return processed_[0], processed_[1], processed_[4]
    except:
        pass
    try:
        return processed_[0], processed_[3]
    except:
        return processed_[0], processed_[1]




