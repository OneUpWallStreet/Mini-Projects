from Enviorment import ChessBoard
import numpy as np
import copy

env = ChessBoard()


player = 1
env.reset()
print(env.board)
while True:
    
    # print('actions: ',actions)
    if player == -1:

        fake_board = copy.deepcopy(env.board)
        actions = env.final_actions(player,fake_board)
            
        if len(actions)!=0:
            a_index = np.random.randint(0,len(actions))
            action = actions[a_index]
        else:
            action = (None,None)

        reward,done = env.step(action,player,env.board)
    
    else:
        
        old_y = int(input('Old y: '))
        old_x = int(input('Old x: '))

        new_y = int(input('New y: '))
        new_x = int(input('New x: '))

        old_pos = (old_y,old_x)
        new_pos = (new_y,new_x)

        action = [old_pos,new_pos]

        reward,done = env.step(action,player,env.board)

    print('Player making move: ',player)
    
    
    print('\n')
    print(env.board)
    print('\n')
    
    print('________________________________')

    
    
    
    player = env.change_player(player)

    if done== True:
        if reward == 1:
            print('Winner: White! ')

        elif reward == -1:
            print('Winner: Black!')

        else:
            print('Draw')
        break