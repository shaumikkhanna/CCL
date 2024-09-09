import numpy as np
import time


class Game:
    def __init__(self, starter=None):
        self.number = 1
        
        if starter is None:
            if np.random.rand() < 0.5:
                self.whose_turn = 0
            else:
                self.whose_turn = 1
        else:
            self.whose_turn = starter
        
        
    def play(self, player, num):
        if num not in [1, 2]:
            raise ValueError(f"Invalid number {num}")
        
        if player != self.whose_turn:
            raise ValueError("Not your turn")
        
        self.number += num
        if self.number >= 13:
            # print(f'Player {int(not self.whose_turn)} wins!')
            self.winner = int(not self.whose_turn)
            return -1
        else:
            self.whose_turn = int(not self.whose_turn)
            return self.number
        

class Agent:
    def __init__(self, method):
        self.arms = np.ones(shape=(12, 2), dtype=int) * 25
        self.method = method

    def pick_arm(self, current_number, method):
        if method == 'random':
            return np.random.randint(1, 3)
        
        elif method == 'greedy':
            if self.arms[current_number - 1, 0] > self.arms[current_number - 1, 1]:
                return 1
            elif self.arms[current_number - 1, 0] < self.arms[current_number - 1, 1]:
                return 2
            else:
                return self.pick_arm(current_number, method='random')
        
        elif method == 'epsilon_greedy':
            if np.random.rand() < 1 / 6:
                return self.pick_arm(current_number, method='random')
            else:
                return self.pick_arm(current_number, method='greedy')
        
        elif method == 'softmax':
            if np.random.rand() < np.exp(self.arms[current_number - 1, 0]) / np.sum(np.exp(self.arms[current_number - 1])):
                return 1
            else:
                return 2

    def train_game(self):
        self.play_history = []
        
        g = Game()
        whose_turn = g.whose_turn
        current_number = 1

        while True:
            # Pick an arm and record that pick
            arm = self.pick_arm(current_number, method=self.method)
            self.play_history.append((whose_turn, current_number, arm))

            # Play that arm and get the new number
            current_number = g.play(whose_turn, arm)
            whose_turn = int(not whose_turn)

            # Check for endgame
            if current_number == -1:
                break

        # print(self.play_history)
                
        # Update the arms based on the results of the game
        for turn, number, arm in self.play_history:
            if 0 < self.arms[number - 1, arm - 1] < 50:
                self.arms[number - 1, arm - 1] += 1 if turn == g.winner else -1


    
def lets_play(agent, sleep=0):
    g = Game(starter=int(input("Press 0 to start the game or 1 for the computer to start - \n")))

    while True:
        print(f"\n --- Current number is {g.number} --- \n")
        if g.whose_turn == 1:
            arm = agent.pick_arm(g.number, method='greedy')
            if sleep:
                time.sleep(sleep)
            print(f"BEEP BOOP! I pick {arm}")
            g.play(g.whose_turn, arm)
        else:
            arm = int(input("Enter 1 or 2 - \n"))
            print(f"You pick {arm}")
            g.play(g.whose_turn, arm)
        
        if g.number >= 13:
            print('\n\n\n')
            if g.whose_turn == 1:
                print(f'Hooray you win!')
            else:
                print(f'BEEP BOOP! You lose!')
            break

    
a = Agent('epsilon_greedy')
for _ in range(100):
    a.train_game()

lets_play(a, sleep=1.5)

time.sleep(2)

print('\n\n\n')
print('Final arm values:')
for i, a in enumerate(a.arms):
    print(f'On number {i+1} - Beads of 1: {a[0]} - Beads of 2: {a[1]}')

