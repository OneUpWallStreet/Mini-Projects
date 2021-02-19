import numpy as np

class TicTacToe:

    def __init__(self):

        self.states = np.zeros((3,3))

    def reset(self):
        self.states = np.zeros((3,3))

    def check_terminal(self):

        winner = self.check_horizontal()
        if winner == 2:
            return -1
            
        if winner == 1:
            return 1

        winner = self.check_vertical()
        if winner == 2:
            return -1
            
        if winner == 1:
            return 1


        winner = self.check_vertical()
        if winner == 2:
            return -1
            
        if winner == 1:
            return 1

        winner = self.check_diagonal()
        if winner == 2:
            return -1
            
        if winner == 1:
            return 1

        draw = self.check_draw()
        if draw == True:
            return 0


    def check_draw(self):

        actions = self.get_valid_action()

        if not actions:
            return True

        else:
            return False

    def get_valid_action(self):

        valid_actions = []

        for x in range(3):
            for y in range(3):

                if self.states[x][y] == 0:
                    valid_actions.append((x,y))


        return valid_actions


    def check_horizontal(self):

        winner = 0

        for i in range(3):
            can = []
            for j in range(3):
                can.append(self.states[i][j])

            one_wins = all(x == 1 for x in can)
            two_wins = all(x == 2 for x in can)


            if one_wins:
                winner = 1
                return winner

            elif two_wins:
                winner = 2
                return winner

        return 0

    def check_vertical(self):

        winner = 0

        for i in range(3):
            can = []
            for j in range(3):
                can.append(self.states[j][i])

            one_wins = all(x ==1 for x in can)
            two_wins = all(x ==2 for x in can)

            if one_wins:
                winner = 1
                return winner

            elif two_wins:
                winner = 2
                return winner

        return 0

    def check_diagonal(self):

        winner = 0

        if self.states[0][0]==1 and self.states[1][1]==1 and self.states[2,2] == 1:
            winner = 1
            return winner

        elif self.states[0][2]==1 and self.states[1][1]==1 and self.states[2][0] == 1:
            winner = 1
            return winner

        elif self.states[0][0]==2 and self.states[1][1]==2 and self.states[2,2] == 2:
            winner = 2
            return winner

        elif self.states[0][2]==2 and self.states[1][1]==2 and self.states[2][0] == 2:
            winner = 2
            return winner

        return 0