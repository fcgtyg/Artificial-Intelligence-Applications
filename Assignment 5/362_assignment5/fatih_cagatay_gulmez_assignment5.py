from random import shuffle, randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class card():
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.color + " " + str(self.value)

class easy21():
    def __init__(self):
        self.players = {}
        for player in ["dealer", "player"]:
            self.players[player] = [], True, True #hand, first_hand, hit
        self.deck = []
        for color in ["black", "black", "red"]:
            for i in range(10):
                if color == "red":
                    self.deck.append(card(color, -i-1))
                else:
                    self.deck.append(card(color, i+1))
        shuffle(self.deck)

    def pick_a_card(self, first_hand = False):
        if first_hand:
            picked = card("black", randint(1,10))
        else:
            picked = self.deck[randint(1, len(self.deck)-1)]

        return picked

    def check_hand(self, hand):
        value = 0
        for item in hand:
            value += item.value
        return value

    #Returns if next state is Terminal or not.
    def play(self,player = "dealer", hit = True):
        hand, first_hand, hit = self.players[player]
        if hit:
            hand.append(self.pick_a_card(first_hand))
        self.players[player] = hand, False, hit
        value = self.check_hand(hand)
        if value < 1 or value > 21:
            print "%s lost!" %player, value
            return
        if player == "dealer" and hit:
            if value>=17:
                self.players["dealer"] = hand, False, False
                self.play("player", self.players["player"][2])
            else:
                hit = True
                self.play("dealer", hit)

        elif player == "player" and hit:
            print "Value %d " % value
            next_move = raw_input("Press any key for Hit; press 0 for Stick: ")

            if next_move == "0":
                self.players["player"] = hand, False, False
                self.play("dealer", self.players["dealer"][2])
            else:
                hit = True
                self.play("player", hit)
        else:
            player_value = self.check_hand(self.players["player"][0])
            dealer_value = self.check_hand(self.players["dealer"][0])
            if player_value>dealer_value:
                print "Player won!", "Player:",player_value, "Dealer:", dealer_value
                return "Terminal", 1.0
            else:
                print "Dealer won!", "Dealer:", dealer_value, "Player: ", player_value
                return "Terminal", -1.0

    def step(self, state, action):
        #State = (Player's sum, Dealer's Sum)
        #Action = ("hit" or "stick")
        dealerShowing, player = state
        if action == "hit":
            player += self.pick_a_card().value
            if player < 1 or player > 21:
                return (dealerShowing, player), -1.0, "Terminal"
            else:
                return (dealerShowing, player), 0.0, "Not Terminal"
        else:
            dealer = dealerShowing
            while dealer < 17 :
                dealer += self.pick_a_card().value
                if dealer<1 or dealer>21:
                    return (dealerShowing, player), 1.0, "Terminal"
            return (dealerShowing, player), 1.0 if player > dealer else (0.0 if player == dealer else -1.0),"Terminal"

    def playGame(self):
        dealerShowing = self.pick_a_card(True).value
        record = (dealerShowing, self.pick_a_card(True).value), 0.0, "Not Terminal"
        records = [record]
        while record[2] != "Terminal":
            policy = "hit" if randint(0,1) == 0 else "stick"
            record = step(record[0], policy)
            records.append(record)
        return records

    def playGameTD(self, records):
        dealerShowing = self.pick_a_card(True).value
        record = (dealerShowing, self.pick_a_card(True).value), 0.0, "Not Terminal"

        recordOld = record

        policy = "hit" if randint(0,1) == 0 else "stick"
        record = step(record[0], policy)
        x,y = recordOld[0]
        if records[x][y] is not None:
            record = record[0], recordOld[1] + 0.5*(record[1] + recordOld[1] - records[x][y]), record[2]
        else:
            record = record[0], recordOld[1] + 0.5*(record[1] + record[1]-recordOld[1]), record[2]
        x, y = record[0]
        records[x][y] = record[1]
        return record

class monteCarlo():
    def __init__(self):
        self.returns = []
        for i in range(11):
            self.returns.append([])
            for j in range(22):
                self.returns[i].append((None,0))

    def simulation(self, maxIteration = 1000000):
        iteration = 0
        while iteration<maxIteration:
            results = game.playGame()
            for i in range(len(results)-1):
                x, y = results[i][0]
                reward = results[i][1]
                for j in range(i, len(results)):
                    reward += results[j][1]
                if self.returns[x][y][0] == None:
                    self.returns[x][y] = 0,0
                self.returns[x][y] = (self.returns[x][y][0]*self.returns[x][y][1] + reward)/(self.returns[x][y][1] + 1), self.returns[x][y][1] + 1
            iteration += 1

        graph = [[],[],[]]
        for i in range(11):
            for j in range(22):
                if self.returns[i][j][0] != None:
                    graph[0].append(i)
                    graph[1].append(j)
                    graph[2].append(self.returns[i][j][0])
        dealer, player, rewards = graph[0], graph[1], graph[2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(dealer, player, rewards)
        ax.set_xlabel('Dealer axis')
        ax.set_ylabel('Player axis')
        ax.set_zlabel('Rewards axis')
        plt.show()
        return self.returns

class TD():
    def __init__(self):
        self.returns = []
        for i in range(11):
            self.returns.append([])
            for j in range(22):
                self.returns[i].append(None)

    def simulate(self, maxIteration = 1000000):
        iteration = 0
        while iteration < maxIteration:
            result = game.playGameTD(self.returns)
            while result[2] != "Terminal":
                x, y = result[0]
                result = game.playGameTD(self.returns)
            iteration += 1


        graph = [[], [], []]
        for i in range(11):
            for j in range(22):
                if self.returns[i][j] is not None:
                    graph[0].append(i)
                    graph[1].append(j)
                    graph[2].append(self.returns[i][j])
        dealer, player, rewards = graph[0], graph[1], graph[2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(dealer, player, rewards)
        ax.set_xlabel('Dealer axis')
        ax.set_ylabel('Player axis')
        ax.set_zlabel('Rewards axis')
        plt.show()
        return self.returns

game = easy21()

def step(state, action):
    return game.step(state, action)

def MonteCarlo(iteration = None):
    mc = monteCarlo()
    if iteration:
        return mc.simulation(maxIteration=iteration)
    else:
        return mc.simulation()

def tD():
    td = TD()
    td.simulate()

tD()