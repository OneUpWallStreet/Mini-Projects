import numpy as np
import copy
import time


class ChessBoard:


    def __init__(self):

        self.board = np.zeros((8,8))
        self.reset()
    
    def reset(self):

        #Pawn counters
        self.black_pawn_start = ((1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7))
        self.white_pawn_start = ((6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7))
        self.En_Passant_counter = []

        #Castle Counters when rook dies change counter to 1
        self.Has_White_King_Moved = 0
        self.Has_White_Rook_Queen_Side_Moved = 0
        self.Has_White_Rook_Right_Side_Moved = 0

        self.Has_Black_King_Moved = 0
        self.Has_Black_Rook_Queen_Side_Moved = 0
        self.Has_Black_Rook_Right_Side_Moved = 0

        self.Castle_Counter_White_Right = 0
        self.Castle_Counter_White_Left = 0

        self.Castle_Counter_Black_Right = 0
        self.Castle_Counter_Black_Left = 0

        

        #Make sure that at the end of board pawn can become a queen
        self.Black_King = -1
        self.White_King = 1

        self.Black_Pawn = -2
        self.White_Pawn = 2

        self.Black_Knight = -3
        self.White_Knight = 3

        self.Black_Bishop = -4
        self.White_Bishop = 4

        self.Black_Rook = -5
        self.White_Rook = 5

        self.Black_Queen = -6
        self.White_Queen = 6

        #None = 0
        #King = 1
        #Pawn = 2
        #Knight = 3
        #Bishop = 4
        #Rook = 5
        #Queen = 6

        #White = +
        #Black = -
        
        self.board[0][0] = -5
        self.board[0][1] = -3
        self.board[0][2] = -4
        self.board[0][3] = -6
        self.board[0][4] = -1
        self.board[0][5] = -4
        self.board[0][6] = -3
        self.board[0][7] = -5
        self.board[1][0] = -2
        self.board[1][1] = -2
        self.board[1][2] = -2
        self.board[1][3] = -2
        self.board[1][4] = -2
        self.board[1][5] = -2
        self.board[1][6] = -2
        self.board[1][7] = -2

        self.board[7][0] = 5
        self.board[7][1] = 3
        self.board[7][2] = 4
        self.board[7][3] = 6
        self.board[7][4] = 1
        self.board[7][5] = 4
        self.board[7][6] = 3
        self.board[7][7] = 5
        self.board[6][0] = 2
        self.board[6][1] = 2
        self.board[6][2] = 2
        self.board[6][3] = 2
        self.board[6][4] = 2
        self.board[6][5] = 2
        self.board[6][6] = 2
        self.board[6][7] = 2

        self.check_moves = []

        #So Possible Moves does not remove counter 
        self.check_counter = False


    def check_for_check(self,player,board):

        check = False
        # print(self.check_moves)
        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1
        

        fake_board = copy.deepcopy(board)
        throw = env.get_actions(other_player,fake_board)

        if player == 1:
            for i,y in enumerate(fake_board):
                for j,x in enumerate(y):
                    if board[i,j] == 1:
                        king_loc = (i,j)
                        # print(king_loc)
        
        elif player == -1:
            for i,y in enumerate(fake_board):
                for j,x in enumerate(y):
                    if board[i,j] == -1:
                        king_loc = (i,j)
                        # print(king_loc)

        # print(self.check_moves)
        check_moves_local = []
        # print(king_loc)
        if len(self.check_moves)!=0:
            for x in self.check_moves:
                for y in x:
                    check_moves_local.append(y)
                # check_moves_local.append(x)
        else:
            check_moves_local = self.check_moves

        # print('\n')
        # print('Check Moves Local: ',check_moves_local)
        # print('King Loc: ',king_loc)
        # print('\n')
        # print(self.check_moves)
        if king_loc in check_moves_local:
            check = True

        return check


    #If Black puts check on white than white uses this to calculate move that remove check
    def actions_when_check(self,player,board):

        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1

        legal_check_moves = []

        #Player = 1 in story
        self.check_counter = True
        actions = self.get_actions(player,board)

        # print(actions)

        self.check_counter = False

        for a in actions:

            fake_board = copy.deepcopy(board)

            peice_one_y = a[0][0]
            peice_one_x = a[0][1]
            # print(a)
            peice_next_y = a[1][0]
            peice_next_x = a[1][1]

            peice = fake_board[peice_one_y,peice_one_x]

            fake_board[peice_one_y,peice_one_x] = 0
            fake_board[peice_next_y,peice_next_x] = peice


            #Reset the self.check_moves other wise it fills it up with old data 


            opp_action_after_check_move = self.get_actions(other_player,fake_board)
            # print(self.check_moves)
            self.check_moves = []
            # opp_action_after_check_move = self.filter_actions(other_player,opp_action_after_check_move,fake_board)
            # print(self.check_moves)

            check = self.check_for_check(player,fake_board)
            # print(check)

            # print('Action: ',a)
            # print('Check_Moves: ',self.check_moves)
            # print(fake_board)


            if check == False:
                legal_check_moves.append(a)
        
        legal_check_moves_copy = copy.deepcopy(legal_check_moves)

        for a in legal_check_moves_copy:

            if a[0] == (0,4) or a[0] == (7,4):
                if a[1] == (0,2) or a[1] == (0,6) or a[1] == (7,2) or a[1] == (7,6):
                    legal_check_moves.remove(a)

        return legal_check_moves

    def peice_on_board(self,board):

        all_peices = []

        for i,y in enumerate(board):
            for j,x in enumerate(y):
                if board[i,j] > 0 or  board[i,j]<0:
                    all_peices.append(board[i,j])

        return all_peices

    def final_actions(self,player,board):

        self.check_moves = []

        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1

        opp_action = self.get_actions(other_player,board)
        check = self.check_for_check(player,board)

        if check == True:
            actions = self.actions_when_check(player,board)
            return actions


        else:
            self.Castle_Counter_White_Right = 0
            self.Castle_Counter_White_Left = 0
            self.Castle_Counter_Black_Right = 0
            self.Castle_Counter_Black_Left = 0

            actions = self.get_actions(player,board)
            final_actions = self.filter_actions(player,actions,board)
            final_actions = self.check_castle_middle(final_actions,player,board)

        if len(final_actions)==0:
            return []

        return final_actions


    def get_actions(self,player,board):

        self.check_counter = False

        fake_board = copy.deepcopy(board)
        # If actions are empty return None,None to say that game is over?

        actions = []

        if player == 1:

            for i,y in enumerate(fake_board):
                for j,x in enumerate(y):
                    if board[i,j] > 0:
                        ava_actions = self.possible_move(board,(i,j))
                        if len(ava_actions)!= 0:
                            for a in ava_actions:
                                actions.append(a)

        if player == -1:

            for i,y in enumerate(fake_board):
                for j,x in enumerate(y):
                    if board[i,j] < 0:
                        ava_actions = self.possible_move(board,(i,j))
                        if len(ava_actions)!= 0:
                            for a in ava_actions:
                                actions.append(a)


        return actions

    def step(self,action,player,board):

        # if action = (None,None)

        reward,done = self.check_terminal(player,board)

        if done == True:
            return reward,done

        peice_one_y = action[0][0]
        peice_one_x = action[0][1]

        start_loc = (peice_one_y,peice_one_x)

        peice_next_y = action[1][0]
        peice_next_x = action[1][1]

        next_loc = (peice_next_y,peice_next_x)

        piece = board[peice_one_y][peice_one_x]

        if board[start_loc] == -5 and start_loc == (0,0):
            self.Has_Black_Rook_Queen_Side_Moved = 1

        if board[start_loc] == -5 and start_loc == (0,7):
            self.Has_Black_Rook_Right_Side_Moved = 1

        if board[start_loc] == 5 and start_loc == (7,0):
            self.Has_White_Rook_Queen_Side_Moved = 1

        if board[start_loc] == 5 and start_loc == (7,7):
            self.Has_White_Rook_Right_Side_Moved = 1

        if piece == 1 and next_loc != (7,2):
            self.Has_White_King_Moved = 1

        if piece == 1 and next_loc != (7,6):
            self.Has_White_King_Moved = 1

        if piece == -1 and next_loc != (0,2):
            self.Has_Black_King_Moved = 1

        if piece == -1 and next_loc != (0,6):
            self.Has_Black_King_Moved = 1


        if piece == 1 and start_loc == (7,4) and next_loc == (7,2):

            board[start_loc] = 0
            board[next_loc] == 1

            board[7,0] = 0 
            board[7,3] = 5

        if piece == 1 and start_loc == (7,4) and next_loc == (7,6):

            board[start_loc] = 0
            board[next_loc] == 1

            board[7,7] = 0 
            board[7,5] = 5

        if piece == -1 and start_loc == (0,4) and next_loc == (0,2):

            board[start_loc] = 0
            board[next_loc] == -1

            board[0,0] = 0 
            board[0,3] = -5

        if piece == -1 and start_loc == (0,4) and next_loc == (0,6):

            board[start_loc] = 0
            board[next_loc] == -1

            board[0,7] = 0 
            board[0,5] = -5

        board[start_loc] = 0
        board[next_loc] = piece

        if player == 1:

            if next_loc in ((0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)) and piece == 2:
                board[next_loc] = 6

        if player == -1:

            if next_loc in ((7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)) and piece == -2:
                board[next_loc] = -6

        return None,done


    def check_terminal(self,player,board):

        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1

        reward = None
        done = False

        fake_board = copy.deepcopy(board)

        check = self.check_for_check(player,board)

        if check == True:

            actions_pos = self.final_actions(player,fake_board)

            if len(actions_pos)==0:
                done = True
                return other_player,done

        elif check == False:

            peices = self.peice_on_board(fake_board)
            # print('peices: ',peices)
            if len(peices) == 2:
                done = True
                return 0,done

            actions_pos = self.final_actions(player,fake_board)

            if len(actions_pos)==0:
                done = True
                return 0,done

        return None,done

            
    def check_castle_middle(self,actions,player,board):
        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1

        opp_moves = self.get_actions(other_player,board)
        opp_moves_final = self.filter_actions(other_player,opp_moves,board)

        for a in opp_moves_final:
            if a[1] == (7,3) or a[1] == (7,2):
                self.Castle_Counter_White_Left = 1

            if a[1] == (7,5) or a[1] ==  (7,6):
                self.Castle_Counter_White_Right = 1

            if a[1] == (0,3) or a[1] == (0,2):
                self.Castle_Counter_Black_Left = 1

            if a[1] == (0,5) or a[1] == (0,6):
                self.Castle_Counter_Black_Right = 1
        
        final_copy = copy.deepcopy(actions)
        for a in final_copy:

            if a[0] == (7,4) and a[1] == (7,2) and board[7,4]==1 and self.Castle_Counter_White_Left==1:
                actions.remove(a)

            if a[0] == (7,4) and a[1] == (7,6) and board[7,4] == 1 and self.Castle_Counter_White_Right==1:
                actions.remove(a)

            if a[0] == (0,4) and a[1] == (0,2) and board[0,4] == -1 and self.Castle_Counter_Black_Left == 1:

                actions.remove(a)

            if a[0] == (0,4) and a[1] == (0,6) and board[0,4] == -1 and self.Castle_Counter_Black_Right==1:
                actions.remove(a) 
        
        return actions

        

    def filter_actions(self,player,actions,board):

        moves_copy = copy.deepcopy(actions)

        if player == 1:
            other_player = -1

        elif player == -1:
            other_player = 1

        for a in moves_copy:
            fake_board = copy.deepcopy(board)

            peice_one_y = a[0][0]
            peice_one_x = a[0][1]

            peice_next_y = a[1][0]
            peice_next_x = a[1][1]

            peice = fake_board[peice_one_y,peice_one_x]

            fake_board[peice_one_y,peice_one_x] = 0 

            fake_board[peice_next_y,peice_next_x] = peice
            
            self.check_moves = []

            opp_ac = self.get_actions(other_player,fake_board)

            

            check = self.check_for_check(player,fake_board)
            # print(check)
            # print(fake_board)

            if check == True:
                actions.remove(a)

        return actions

    def change_player(self,player):

        if player == 1:
            return -1
        elif player == -1:
            return 1


    def possible_move(self,board,square_loc):

        #(Start_pos,End_pos)
        actions = []

        y = square_loc[0]
        x = square_loc[1]

        piece = board[y][x]

        if piece>0:
            player = 1
            other_player = -1

        elif piece<0:
            player = -1
            other_player = 1

        #Move Queen
        #____________________________________________________________________________________________________________________________________


        if piece == self.Black_Queen or piece == self.White_Queen:

            #Move Right 
            next_x = x
            while True:

                next_x = next_x+1
                
                if next_x == 8:
                    break

                if player == 1:
                    if board[y][next_x] == 0 or board[y][next_x] <0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break

                elif player == -1:

                    if board[y][next_x] == 0 or board[y][next_x] >0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break

            # Move Left

            next_x = x
            while True:

                next_x = next_x-1
                
                if next_x == -1:
                    break

                if player == 1:
                    if board[y][next_x] == 0 or board[y][next_x] <0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break

                elif player == -1:

                    if board[y][next_x] == 0 or board[y][next_x] >0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break
            
            #Move Up 

            next_y = y
            while True:

                next_y = next_y-1
               
                if next_y == -1:
                    break


                if player == 1:
                    if board[next_y][x] == 0 or board[next_y][x] <0:

                        actions.append([square_loc,(next_y,x)])

                    if board[next_y][x]!=0:
                        break

                elif player == -1:

                    if board[next_y][x] == 0 or board[next_y][x] >0:
                        actions.append([square_loc,(next_y,x)])


                    if board[next_y][x]!=0:
                        break

            # Move Down

            next_y = y
            while True:

                next_y = next_y+1
               
                if next_y == 8:
                    break


                if player == 1:
                    if board[next_y][x] == 0 or board[next_y][x] <0:

                        actions.append([square_loc,(next_y,x)])

                    if board[next_y][x]!=0:
                        break

                elif player == -1:

                    if board[next_y][x] == 0 or board[next_y][x] >0:
                        actions.append([square_loc,(next_y,x)])


                    if board[next_y][x]!=0:
                        break

            # Move Diagonal Up Left
            next_y = y
            next_x = x

            while True:

                next_y = next_y - 1
                next_x = next_x - 1


                if next_y == -1:
                    break

                if next_x == -1:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

            # Move Diagonal Up Right

            next_y = y
            next_x = x

            while True:

                next_y = next_y - 1
                next_x = next_x + 1


                if next_y == -1:
                    break

                if next_x == 8:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break


            # Move Diagonal Down Right

            next_y = y
            next_x = x
            count = 0

            while True:

                next_y = next_y + 1
                next_x = next_x + 1


                if next_y == 8:
                    break

                if next_x == 8:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

             # Move Diagonal Down Left

            next_y = y
            next_x = x

            while True:

                next_y = next_y + 1
                next_x = next_x - 1


                if next_y == 8:
                    break

                if next_x == -1:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

            

        #Move Knight
        #____________________________________________________________________________________________________________________________________

        if piece == self.Black_Knight or piece == self.White_Knight:

            #Move Knight Bottom Right

            next_y = y+1
            next_x = x+2

            if next_y<8 and next_x <8:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            


            #Move Knight Bottom Left X bias

            next_y = y+1
            next_x = x-2

            if next_y<8 and next_x >-1:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            #Move Knight Top Left X bias

            next_y = y-1
            next_x = x-2
            
            if next_y >-1 and next_x >-1:

                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            #Move Knight Top Right X bias

            next_y = y-1
            next_x = x+2

            if next_y > -1 and next_x <8:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            #Move Knight Top Right

            next_y = y-2
            next_x = x+1

            if next_y > -1 and next_x <8:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            #Move Knight Top Left

            next_y = y-2
            next_x = x-1
            
            if next_y >-1 and next_x >-1:

                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])


            #Move Knight Bottom Left

            next_y = y+2
            next_x = x-1

            if next_y<8 and next_x >-1:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:
                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])

            #Move Knight Bottom Right

            next_y = y+2
            next_x = x+1

            if next_y<8 and next_x <8:
            
                if player == 1:
                    
                    if board[next_y][next_x] == 0 or board[next_y][next_x] < 0:

                        actions.append([square_loc,(next_y,next_x)])

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        actions.append([square_loc,(next_y,next_x)])


        #Move Bishop
        #____________________________________________________________________________________________________________________________________

        if piece == self.Black_Bishop or piece == self.White_Bishop:

            # Move Diagonal Up Left
            next_y = y
            next_x = x

            while True:

                next_y = next_y - 1
                next_x = next_x - 1


                if next_y == -1:
                    break

                if next_x == -1:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

            # Move Diagonal Up Right

            next_y = y
            next_x = x

            while True:

                next_y = next_y - 1
                next_x = next_x + 1


                if next_y == -1:
                    break

                if next_x == 8:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break


            # Move Diagonal Down Right

            next_y = y
            next_x = x
            count = 0

            while True:



                next_y = next_y + 1
                next_x = next_x + 1


                if next_y == 8:
                    break

                if next_x == 8:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

             # Move Diagonal Down Left

            next_y = y
            next_x = x

            while True:

                next_y = next_y + 1
                next_x = next_x - 1


                if next_y == 8:
                    break

                if next_x == -1:
                    break

                if player == 1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] <0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break

                if player == -1:

                    if board[next_y][next_x] == 0 or board[next_y][next_x] >0:
                        
                        actions.append([square_loc,(next_y,next_x)])

                    if board[next_y][next_x]!=0:
                        break


        # Rook Moves
        #____________________________________________________________________________________________________________________________________
        if piece == self.White_Rook or piece == self.Black_Rook:

            #Move Right 
            next_x = x
            while True:

                next_x = next_x+1
                
                if next_x == 8:
                    break

                if player == 1:
                    if board[y][next_x] == 0 or board[y][next_x] <0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break

                elif player == -1:

                    if board[y][next_x] == 0 or board[y][next_x] >0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break

            # Move Left

            next_x = x
            while True:

                next_x = next_x-1
                
                if next_x == -1:
                    break

                if player == 1:
                    if board[y][next_x] == 0 or board[y][next_x] <0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break
                elif player == -1:

                    if board[y][next_x] == 0 or board[y][next_x] >0:
                        actions.append([square_loc,(y,next_x)])

                    if board[y][next_x]!=0:
                        break
            
            #Move Up 

            next_y = y
            while True:

                next_y = next_y-1
               
                if next_y == -1:
                    break


                if player == 1:
                    if board[next_y][x] == 0 or board[next_y][x] <0:

                        actions.append([square_loc,(next_y,x)])

                    if board[next_y][x]!=0:
                        break

                elif player == -1:

                    if board[next_y][x] == 0 or board[next_y][x] >0:
                        actions.append([square_loc,(next_y,x)])


                    if board[next_y][x]!=0:
                        break

            # Move Down

            next_y = y
            while True:

                next_y = next_y+1
               
                if next_y == 8:
                    break


                if player == 1:
                    if board[next_y][x] == 0 or board[next_y][x] <0:

                        actions.append([square_loc,(next_y,x)])

                    if board[next_y][x]!=0:
                        break

                elif player == -1:

                    if board[next_y][x] == 0 or board[next_y][x] >0:
                        actions.append([square_loc,(next_y,x)])


                    if board[next_y][x]!=0:
                        break

            

        
        #King Movement add Castle later
        #____________________________________________________________________________________________________________________________________
        if piece == self.White_King or piece == self.Black_King:
            
            #Move Up
            # next_pos_up = (y-1,x)  
            actions.append([square_loc,(y-1,x)])

            #Move Down
            # next_pos_down = (y+1,x)
            actions.append([square_loc,(y+1,x)])
            
            #Move Left
            # next_pos_left = (y,x-1)
            actions.append([square_loc,(y,x-1)])

            #Move Right
            # next_pos_right = (y,x+1)
            actions.append([square_loc,(y,x+1)])

            #Move Diagonal Left
            # next_pos_digonal_left = (y-1,x-1)
            actions.append([square_loc,(y-1,x-1)])

            #Move Diagonal Right
            # next_pos_digonal_right = (y-1,x+1)
            actions.append([square_loc,(y-1,x+1)])

            #Move Diagonal Bottom Left
            # next_pos_digonal_bottom_left = (y+1,x-1)
            actions.append([square_loc,(y+1,x-1)])

            #Move Diagonal Bottom Right
            # next_pos_digonal_bottom_right = (y+1,x+1)
            actions.append([square_loc,(y+1,x+1)])


            #Remove invalid actions
            actions_copy = copy.deepcopy(actions)
            if actions!=0:
                for action in actions_copy:

                    if action[1][0] <0 or action[1][0]>7 or action[1][1]<0 or action[1][1]>7:
                        actions.remove(action)

                actions_copy = copy.deepcopy(actions)
                fake_board = copy.deepcopy(board)

                # Check this and unmark
                # print(actions)

                if player == -1:

                    for action in actions_copy:
                        
                        next_pos_y = action[1][0]
                        next_pos_x = action[1][1]

                        # print(action)
                        # print(actions)
                        # print(next_pos_y,next_pos_x)

                        if board[max(next_pos_y-1,0),max(next_pos_x-1,0)] == 1:
                            # print('1')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[max(next_pos_y-1,0),next_pos_x] == 1:
                            # print('2')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[max(next_pos_y-1,0),min(next_pos_x+1,7)] == 1:
                            # print('3')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[next_pos_y,max(next_pos_x-1,0)] == 1:
                            # print('4')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[next_pos_y,min(next_pos_x+1,7)] == 1:
                            # print('Action: ',action)
                            # print('Actions: ',actions)
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),max(next_pos_x-1,0)] == 1:
                            # print('5')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),next_pos_x] == 1:
                            # print('6')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),min(next_pos_x+1,7)] == 1:
                            # print('7')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        next_pos_y = action[1][0]
                        next_pos_x = action[1][1]

                        if fake_board[next_pos_y,next_pos_x] == 1:
                            actions.remove(action)


                if player == 1:

                    for action in actions_copy:
                        
                        next_pos_y = action[1][0]
                        next_pos_x = action[1][1]

                        # print(action)
                        # print(actions)
                        # print(next_pos_y,next_pos_x)

                        if board[max(next_pos_y-1,0),max(next_pos_x-1,0)] == -1:
                            # print('1')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[max(next_pos_y-1,0),next_pos_x] == -1:
                            # print('2')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[max(next_pos_y-1,0),min(next_pos_x+1,7)] == -1:
                            # print('3')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[next_pos_y,max(next_pos_x-1,0)] == -1:
                            # print('4')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[next_pos_y,min(next_pos_x+1,7)] == -1:
                            # print('Action: ',action)
                            # print('Actions: ',actions)
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),max(next_pos_x-1,0)] == -1:
                            # print('5')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),next_pos_x] == -1:
                            # print('6')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        if board[min(next_pos_y+1,7),min(next_pos_x+1,7)] == -1:
                            # print('7')
                            # print('action: ',action)
                            # print('\n')
                            if action in actions:
                                actions.remove(action)

                        next_pos_y = action[1][0]
                        next_pos_x = action[1][1]

                        if fake_board[next_pos_y,next_pos_x]  == -1:
                            actions.remove(action)
                    
                actions_copy = copy.deepcopy(actions)

                

                for action in actions_copy:
                    if player == 1:
                        if board[action[1][0],action[1][1]]>0:
                            actions.remove(action)

                    elif player ==-1:
                        if board[action[1][0],action[1][1]]<0:
                            actions.remove(action) 

            #If Castling is possible

            if player == 1:

                if self.Has_White_King_Moved == 0:
                    if self.Has_White_Rook_Queen_Side_Moved==0:

                        if board[7][1]==0 and board[7][2] ==0 and board[7][3] == 0:

                            actions.append([square_loc,(7,2)])

                    if self.Has_White_Rook_Right_Side_Moved ==0:

                        if board[7][5] ==0 and board[7][6] == 0:

                            actions.append([square_loc,(7,6)])


            if player == -1:

                if self.Has_Black_King_Moved == 0:

                    if self.Has_Black_Rook_Queen_Side_Moved ==0:

                        if board[0][1] ==0 and board[0][2] == 0 and board[0][3] == 0:

                            actions.append([square_loc,(0,2)])


                    if self.Has_Black_Rook_Right_Side_Moved == 0:

                        if board[0][5] == 0 and board[0][6] == 0:

                            actions.append([square_loc,(0,6)])


        #____________________________________________________________________________________________________________________________________

        #Pawn Movement

        if piece == self.White_Pawn or piece == self.Black_Pawn:

            #White 
            if piece ==self.White_Pawn:

                if y-1 > -2 and y-2 >-2 and x-1>-2 and x+1<9:

                    if board[y-1][x] == 0:
                        actions.append([square_loc,(y-1,x)])

                    if square_loc in self.white_pawn_start:

                        if board[y-2][x] == 0 and board[y-1][x]==0:
                            # print([square_loc,(y-2,x)])
                            actions.append([square_loc,(y-2,x)])


                    if x!=0:

                        if board[y-1][x-1]<0:
                            actions.append([square_loc,(y-1,x-1)])

                        if board[y-1][x-1]==0 and (y-1,x-1) in self.En_Passant_counter:
                            actions.append([square_loc,(y-1,x-1)])

                    if x!=7:

                        if board[y-1][x+1]<0:
                            actions.append([square_loc,(y-1,x+1)])

                        if board[y-1][x-1]==0 and (y-1,x+1) in self.En_Passant_counter:
                            actions.append([square_loc,(y-1,x+1)])

            #Black
            elif piece == self.Black_Pawn:
                
                if y+1 < 9 and y +2 <9 and x-1>-2 and x+1<9:
                    if board[y+1][x] == 0:
                        actions.append([square_loc,(y+1,x)])

                    if square_loc in self.black_pawn_start:
                        if board[y+2][x] == 0 and board[y+1][x]==0:

                            actions.append([square_loc,(y+2,x)])

                    if x!=0:

                        if board[y+1][x-1]>0:
                            actions.append([square_loc,(y+1,x-1)])

                        if board[y+1][x-1] == 0 and (y+1,x-1) in self.En_Passant_counter:
                            actions.append([square_loc,(y+1,x-1)])

                    if x!=7:

                        if board[y+1][x+1]>0:
                            actions.append([square_loc,(y+1,x+1)])

                        if board[y+1][x+1]==0 and (y+1,x+1) in self.En_Passant_counter:
                            actions.append([square_loc,(y+1,x+1)])

        if self.check_counter == False:
            # self.check_moves = []
                
            all_actions_copy = copy.deepcopy(actions)
            for a in all_actions_copy:
                # print(a)
                next_pos = (a[1][0],a[1][1])

                if board[next_pos] == 1 or board[next_pos] == -1:
                    self.check_moves.append(a)



        all_actions_copy = copy.deepcopy(actions)
        for a in all_actions_copy:
            # print(a)
            next_pos = (a[1][0],a[1][1])

            if board[next_pos] == 1 or board[next_pos] == -1:
                actions.remove(a)

        return actions


env = ChessBoard()


# env.reset()


# player = 1
# env.reset()
# while True:
#     fake_board = copy.deepcopy(env.board)
#     actions = env.final_actions(player,fake_board)
#     # print('actions: ',actions)
#     if len(actions)!=0:
#         a_index = np.random.randint(0,len(actions))
#         action = actions[a_index]
#     else:
#         action = (None,None)

#     # if player==1:
#     #     p =  "White" 
#     # else: 
#     #     p = "Black"

#     print('Player making move: ',player)
#     reward,done = env.step(action,player,env.board)
    
#     print('\n')
#     print(env.board)
#     print('\n')
    
#     print('________________________________')

    
    
    
    # player = env.change_player(player)

    # if done== True:
    #     if reward == 1:
    #         print('Winner: White! ')

    #     elif reward == -1:
    #         print('Winner: Black!')

    #     else:
    #         print('Draw')
    #     break


