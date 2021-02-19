
import numpy as np
import time
import copy
from env import *


MIN = -2
MAX = 2

env = TicTacToe()

env.reset()

class MiniMax:

    def __init__(self):

        env.reset()
        self.count = 0

    def minimax(self,action,MAX_PLAYER,env):

        print("Predicting State Values: {:.5f}".format(self.count), end="\r")
        self.count +=1

        winner = env.check_terminal()

        if winner ==1:
            return winner

        elif winner == -1:
            return winner
        
        elif winner == 0:
            return 0


        if MAX_PLAYER ==True:

            best = MIN

            actions = env.get_valid_action()


            for x in actions:

                env_2 = copy.deepcopy(env)

                env_2.states[x[0]][x[1]] = 1

                best = max(best,self.minimax(x,False,env_2))


            return best

        else:

            best = MAX

            actions = env.get_valid_action()

            for x in actions:

                env2 = copy.deepcopy(env)

                env2.states[x[0]][x[1]] = 2

                best = min(best,self.minimax(x,True,env2))

            return best

    def minimax_action(self,env):

        env_fake = copy.deepcopy(env)

        best_action = (0,0)

        best_value = -10

        actions = env_fake.get_valid_action()

        for x in actions:

            env_2 = copy.deepcopy(env_fake)

            env_2.states[x[0]][x[1]] = 1

            action_value = self.minimax(x,False,env_2)

            if action_value>best_value:

                best_value = action_value
                best_action = x

        return best_action

def Play(env,mm):

    print('Starting...')
    print('\n')
    print(env.states)
    print('\n')
    time.sleep(2)

    while True:

        mm.count = 0 

        player_rows = int(input('Enter Row: '))
        player_column = int(input('Enter Column: '))

        action = (player_rows,player_column)

        env.states[player_rows][player_column] = 2

        print('\n')
        print(env.states)
        print('\n')
        time.sleep(2)

        winner = env.check_terminal()

        if winner == 1:
            print('AI Wins')
            break

        elif winner == -1:
            print('Player Wins')
            break

        elif winner == 0:
            print('Draw')
            break


        action = mm.minimax_action(env)

        print('Taking Action: ',action)

        env.states[action[0]][action[1]] = 1

        winner = env.check_terminal()

        print('\n')
        print(env.states)
        print('\n')
        time.sleep(2)

        if winner == 1:
            print('AI Wins')
            break

        elif winner == -1:
            print('Player Wins')
            break

        elif winner == 0:
            print('Draw')
            break

mm = MiniMax()
env = TicTacToe()

Play(env,mm)


