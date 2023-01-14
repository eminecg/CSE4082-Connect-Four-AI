import numpy
import random

import sys
import math


PLAYER = 0
AI = 1
COL_COUNT = 8 # 7
ROW_COUNT = 7 # 6


def create_board():  # create_game_board
    # Create board and fill positions with zeros
    board = numpy.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board

def drop_piece(board, row, col, piece):     # drop_piece
    #play game
    board[row][col] = piece


def is_playable(board, col):    # playable_location_control
    # if location is 0 this means it is valid
    isPlayable=board[ROW_COUNT-1][col] == 0    
    return isPlayable


def get_row(board, col):
    
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

# flips the board to drop all piaces to the bottom
def print_board(board):
    print("-------------------")
    temp=numpy.flip(board, 0).copy()
    for row in range(ROW_COUNT):
        print("|", end=" ")
        for col in range(COL_COUNT):
            print(temp[row][col], end=" ")
        print("|")
    print("-------------------")
    print("  0 1 2 3 4 5 6 7")
    print("")

def possible_drop_locations(board):
    playable_locations = []
    for col in range(COL_COUNT):
        if is_playable(board, col):
            playable_locations.append(col)
    return playable_locations
    
# check the game is won or not, give different name to this function
def check_winner(board):
    players = {1, 2}
    for piece in players:
        
        # vertical four check
        for col in range(COL_COUNT):
            for row in range(ROW_COUNT-3):            
                if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                    print("vertical four check")
                    print_board(board)
                    print("............")
                    return True, piece

        # horizontal four check
        for col in range(COL_COUNT-3):
            for row in range(ROW_COUNT):
                if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                    print("horizontal four check")
                    print_board(board)
                    print("............")
                    return True, piece

        # pozitive diagonal four check
        for col in range(COL_COUNT-3):
            for row in range(ROW_COUNT-3):
                if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                    print("pozitive diagonal four check")
                    print_board(board)
                    print("............")
                    return True, piece

        # negative diagonal four check
        for col in range(COL_COUNT-3):
            for row in range(3, ROW_COUNT):
                if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                    print("negative diagonal four check")
                    print_board(board)
                    print("............")
                    return True, piece       
    
    if len(possible_drop_locations(board)) <= 0:
        return True, 0
    else:
        return False, -1

# change turn function
def change_turn(turn):
    turn += 1
    turn = turn % 2  ##for which player is turn

    #print("current turn:",turn)

    return turn

# funtion for celebrating the winner
def celebrate_winner(board, turn):
    print_board(board)    
    print("***************")
    print("\n    "+get_player_name(turn)+"\n     Wins !!\nCongratulations!\n")
    print("***************")

# return name of the player 
def get_player_name(turn):
    if  turn==0:
        return "Player 1 "
    else :
        return "Player 2 "


# check input bound
def check_input_bound(col):
    if col < 0 or col > COL_COUNT-1:
        return False
    else:
        return True 

def get_human_input(turn):
    while True:               
        col = int(input("Your turn "+get_player_name(turn)+"\nMake your choice (0-6): "))
        if check_input_bound(col):
            return int(col)
        else:
            
            print("\nInvalid input! Please try again.\n")


# heuristic ideas

'''
-----------------------------------------------------------------------------
H1:
        finds consequtive pieces same color  for all directions  as vertical, horizontal, diagonal, negative diagonal, then sum the score of them 

    - 4 in a direction
        sore = 100
    - 3 in a direction with empty space
        score = 5
    - 2 in a direction with 2 empty space
        score = 2        
    - 1 in a direction with 3 empty space
        score = 1

         score = playerI_two_score + playerI_three_score + playerI_four_score - 
                 player2_two_score - player2_three_score - player2_four_score
--------------------------------------------------------------------------------
H2:
    give more weight to the center columns
    create a matrix for weights for each index , then check the board for players pieces and add the weights to the score
 [
 [3, 4, 5, 7, 5, 4, 4, 3 ],
 [4, 6, 7, 8, 7, 6, 4, 4 ],
 [5, 7, 8, 9, 8, 7, 5, 5 ],
 [7, 8, 9, 10,9, 8, 7, 7 ] ,
 [5, 7, 8, 9, 8, 7, 5, 5 ],
 [4, 6, 7, 8, 7, 6, 4, 4 ],
 [3, 4, 5, 7, 5, 4, 4, 3 ] ]

----------------------------------------------------------------------------------
H3:

'''

weight_matrix = [
    [30, 40, 50, 70, 60, 50, 40, 30],
    [40, 60, 80, 100, 100, 80, 60, 40],
    [50, 80, 110, 130, 130, 110, 80, 50],
    [70, 100, 130, 160, 160, 130, 100, 70],
    [50, 80, 110, 130, 130, 110, 80, 50],
    [40, 60, 80, 100, 100, 80, 60, 40],
    [30, 40, 50, 70, 60, 50, 40, 30],
    ]




def calculate_consequtives_score(board, piece):

    score = 0

    #print("heuristic_1")
    # steps

    # step 1 ---------------------------------------------------------------------
    # calculate 1 pieces exist not consequtive, multiply number of occurence by 10

    not_connected_pieces = 0
    not_connected_pieces_indexes =   []
    two_connected_pieces_indexes =   []
    three_connected_pieces_indexes = []


   #for col in range(COL_COUNT-1):
   #    for row in range(ROW_COUNT-1):
   #        if board[row][col] == piece:
   #            not_connected_pieces += 1
   #            not_connected_pieces_indexes.append((row, col))

   ##print("not_connected_pieces:", not_connected_pieces)

   #score += not_connected_pieces * 10

    # step 2 ----------------------------------------------------------------------------
    # calculate consequetive 2 pieces , multiply number of occurence by 100
    
    
    # on vertical direction
    connected_pieces = 0
    for col in range(COL_COUNT-1):
        for row in range(ROW_COUNT-2):
            if board[row][col] == piece and board[row+1][col] == piece:
                connected_pieces += 1
                two_connected_pieces_indexes.append((row, col))
                

    #print("connected_pieces_2_vertical:", connected_pieces)

    # on horizontal direction
    for col in range(COL_COUNT-2):
        for row in range(ROW_COUNT-1):
            if board[row][col] == piece and board[row][col+1] == piece:
                connected_pieces += 1
                two_connected_pieces_indexes.append((row, col))

    #print("connected_pieces_2_horizontal:", connected_pieces)

    # on diagonal direction
    for col in range(COL_COUNT-2):
        for row in range(ROW_COUNT-2):
            if board[row][col] == piece and board[row+1][col+1] == piece:
                connected_pieces += 1
                two_connected_pieces_indexes.append((row, col))

    #print("connected_pieces_2_diagonal:", connected_pieces)

    # on negative diagonal direction
    for col in range(1, COL_COUNT-1):
        for row in range(1, ROW_COUNT-1):
            if board[row-1][col-1] == piece and board[row][col] == piece:
                connected_pieces += 1
                two_connected_pieces_indexes.append((row, col))

    #print("connected_pieces_2_negative_diagonal:", connected_pieces)

    score += connected_pieces * 100

    # step 3 ------------------------------------------------------------------------------
    # calculate consequetive 3 pieces , multiply number of occurence by 1000    
    connected_pieces = 0
    # on vertical direction
    for col in range(COL_COUNT-1):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece:
                connected_pieces += 1
                three_connected_pieces_indexes.append((row, col))

    #print("connected_pieces_3_vertical:", connected_pieces)

    # on horizontal direction
    for col in range(COL_COUNT-3):
        for row in range(ROW_COUNT-1):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece:
                connected_pieces += 1
                three_connected_pieces_indexes.append((row, col))
    #print("connected_pieces_3_horizontal:", connected_pieces)

    # on diagonal direction
    for col in range(COL_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece:
                connected_pieces += 1
                three_connected_pieces_indexes.append((row, col))
    #print("connected_pieces_3_diagonal:", connected_pieces)

    # on negative diagonal direction
    for col in range(2, COL_COUNT-1):
        for row in range(2, ROW_COUNT-1):
            if board[row-2][col-2] == piece and board[row-1][col-1] == piece and board[row][col] == piece:
                connected_pieces += 1
                three_connected_pieces_indexes.append((row, col))

    #print("connected_pieces_3_negative_diagonal:", connected_pieces)
    score += connected_pieces * 1000

    #print("piece : ", piece, "score : ", score)

    # step 4 ------------------------------------------------------------------------------
    # calculate consequetive 4 pieces , multiply number of occurence by 10000
    connected_pieces = 0
    # on vertical direction
    for col in range(COL_COUNT-1):
        for row in range(ROW_COUNT-4):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                connected_pieces += 1
    
    # on horizontal direction
    for col in range(COL_COUNT-4):
        for row in range(ROW_COUNT-1):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                connected_pieces += 1

    # on diagonal direction
    for col in range(COL_COUNT-4):
        for row in range(ROW_COUNT-4):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                connected_pieces += 1

    # on negative diagonal direction
    for col in range(3, COL_COUNT-1):
        for row in range(3, ROW_COUNT-1):
            if board[row-3][col-3] == piece and board[row-2][col-2] == piece and board[row-1][col-1] == piece and board[row][col] == piece:
                connected_pieces += 1
    
    score += connected_pieces * 100000000
    

    return score,not_connected_pieces_indexes,two_connected_pieces_indexes,three_connected_pieces_indexes

def other_player(piece):
    players= {1,2}
    other_piece=-1

    for player in players:
        if player != piece:
            other_piece = player
    return other_piece

def  heuristic_1(board, piece):
    
    other_piece=other_player(piece)

    max_player_score=calculate_consequtives_score(board,piece)[0]
    min_player_score=calculate_consequtives_score(board,other_piece)[0]

    score=max_player_score-min_player_score
    
    return score


def heuristic_2(board, piece):
    
    score=0
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == piece:
                score += weight_matrix[row][col]
            else:
                score -= weight_matrix[row][col]        
    
    other_piece=other_player(piece)

    max_player_score=calculate_consequtives_score(board,piece)[0]
    min_player_score=calculate_consequtives_score(board,other_piece)[0]

    score+=(max_player_score-min_player_score)

    return score

# heuristic function 3
def heuristic_3(board, piece):
     
    other_piece=other_player(piece)

    max_player_score,not_connected_pieces,two_connected_pieces_indexes,three_connected_pieces_indexes=calculate_consequtives_score(board,piece)
    min_player_score,other_not_connected_pieces,other_two_connected_pieces_indexes,other_three_connected_pieces_indexes=calculate_consequtives_score(board,other_piece)
    
    score=0
    # check first if there is a 3 connected pieces
    if len(three_connected_pieces_indexes) > 0:
        max_player_score+=get_center_score(three_connected_pieces_indexes,3)
    if len (other_three_connected_pieces_indexes) > 0:
        min_player_score+=get_center_score(other_three_connected_pieces_indexes,3)
    if len (two_connected_pieces_indexes) > 0:
        max_player_score+=get_center_score(two_connected_pieces_indexes,2)
    if len (other_two_connected_pieces_indexes) > 0:
        min_player_score+=get_center_score(other_two_connected_pieces_indexes,2)
    if len (not_connected_pieces) > 0:
        max_player_score+=get_center_score(not_connected_pieces,1)
    if len (other_not_connected_pieces) > 0:
        min_player_score+=get_center_score(other_not_connected_pieces,1)

    score=max_player_score-min_player_score
    return score
        

# gets tuple list as input and return the center score
def get_center_score(connect_pieces_indexes, num_of_pieces):
    center_score = 0
    extra_score = pow(10,num_of_pieces)

    for index in connect_pieces_indexes:
        if index[1] == 3 or index[1] == 4:
            center_score += extra_score
        if index[0] == 3 :
            center_score += extra_score
    return center_score


def select_heuristic( ):    
    while True:
        heuristic = int(input("Select heuristic function (1-3): "))
        
        if heuristic == 1:
            return  "heuristic_1"
        elif heuristic == 2:
            return "heuristic_2"
        elif heuristic == 3:
            return "heuristic_3"
        else:
            print("Invalid input! Please try again.")

    

# minimax algorithm
def minimax(board, depth,maximizingPlayer,heuristic_type):
    
    playable_locations = possible_drop_locations(board)
        
    # Check if game is over or not
    is_four, winner = check_winner(board)
    if depth == 0 or is_four:
        # if game overzz
        if is_four:
            # If AI win return 1000000 score
            if winner == AI:
                return (None, 1000000)
            # If Player win return -1000000 score
            elif winner == PLAYER:
                return (None, -1000000)
            else:
                # If no one win ,return 0 score
                return (None, 0)
        else:
            # heuristic selection part

            # If depth equals 0 return evaluation score
            #if heuristic_type == "heuristic_1":
            #    return (None, heuristic_1(board, AI))
            #elif heuristic_type == "heuristic_2":
            #    return (None, heuristic_2(board, AI))
            #elif heuristic_type == "heuristic_3":
            #    return (None, heuristic_3(board, AI))

            return (None, heuristic_1(board, AI))
            #return (None, heuristic_2(board, AI))
            #return (None, heuristic_3(board, AI))

    if maximizingPlayer:
        max_value = float("-inf")
        
        # column = random.choice(playable_locations)
        random.shuffle(playable_locations)

        column = playable_locations[0]
        
        for col in playable_locations:
            row = get_row(board, col)

            # Create a temp board
            temp_board = board.copy()

            # simulation
            drop_piece(temp_board, row, col, AI)

            # until terminal or deepest board state
            current_score = minimax(temp_board, depth-1, False,heuristic_type)[1]
            
            if current_score > max_value:
                value = current_score
                column = col
           
        return column, value

    else:
        min_value = float("inf")

        #column = random.choice(playable_locations)
        random.shuffle(playable_locations)
        
        for col in playable_locations:
            row = get_row(board, col)

            # Create a temp board
            temp_board = board.copy()

            # simulation
            drop_piece(temp_board, row, col, PLAYER)

            #until terminal or deepest board state
            current_score = minimax(temp_board, depth-1, True,heuristic_type)[1]

            if current_score < min_value:
                value = current_score
                column = col            
        return column, value       

# HUMAN VS HUMAN
def human_vs_human():
    board = create_board()
    is_game_over = False
    turn = 0
    is_Draw = False

    print_board(board)
    while not is_game_over:
        name=get_player_name(turn)
        #  player 1 turn
        if turn == 0:
            col = get_human_input(turn)
            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 1)
                win_state,piece=check_winner(board)
                if win_state and piece==1:                    
                    celebrate_winner(board, turn)                    
                    is_game_over=True
                if win_state and piece==0:
                    is_Draw=True                                                      

        #  player 2 turn
        else:
            col = get_human_input(turn)
            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 2)
                win_state,piece=check_winner(board)
                if win_state and piece==2:                    
                    celebrate_winner(board, turn)                    
                    is_game_over=True
                if win_state and piece==0:
                    is_Draw=True                                        
        if is_Draw:
            print("Draw!")
            is_game_over=True

        print_board(board) 
        turn=change_turn(turn)

# HUMAN VS AI
def human_vs_ai():
    board = create_board()
    is_game_over = False
    turn = 0
    depth=4
    # select heuristic type  
    heuristic_AI=select_heuristic()
    number_of_moves=0

    print( "heuristic function: ",heuristic_AI)
    

    # battle start human vs ai , human first
    print_board(board)

    while not is_game_over:
        number_of_moves+=1
        name=get_player_name(turn)

        #  player 1 turn
        if turn == 0:
            print("Human turn")
            col = get_human_input(turn)

            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 1)
                win_state, piece = check_winner(board)
                turn = 1
                if win_state and piece==1:                      
                    celebrate_winner(board,1)                    
                    is_game_over=True
            else:
                print("Invalid move! Please try again.")
        #  player 2 (AI) turn
        else:
            # AI turn
            print("AI turn")
            
            col, minimax_score = minimax(board, depth, True, heuristic_AI)

            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 2)
                turn = 0
                win_state,piece = check_winner(board)
                if win_state and piece==2:
                    celebrate_winner(board, 2)                    
                    is_game_over=True

        print_board(board) 

    print("---------------------------")
    print("Number of moves: ",number_of_moves,"\nDept: ",depth,"\nheuristic of AI 1: ",heuristic_AI)
# AI VS AI
def ai_vs_ai():
    board = create_board()
    is_game_over = False
    turn = 0
    depth=1
    # select heuristic type  

    heuristic_AI_1 = select_heuristic()
    heuristic_AI_2 = select_heuristic()
    print("AI 1 heuristic: ", heuristic_AI_1, " AI 2 heuristic: ", heuristic_AI_2)

    number_of_moves=0
    
    # battle start human vs ai , human first
    print_board(board)

    while not is_game_over:
        
        number_of_moves+=1
        name=get_player_name(turn)

        #  player 1 turn
        if turn == 0:
            print("AI 1 turn")
            
            col, minimax_score = minimax(board, depth, True, heuristic_AI_1)

            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 1)
                turn = 1
                win_state,piece = check_winner(board)
                if win_state and piece==1:
                    celebrate_winner(board, 1)                    
                    is_game_over=True

        #  player 2 (AI) turn
        else:
            # AI turn
            print("AI 2 turn")
            
            col, minimax_score = minimax(board, depth, True, heuristic_AI_2)

            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 2)
                turn = 0
                win_state,piece = check_winner(board)
                if win_state and piece==2:
                    celebrate_winner(board, 2)                    
                    is_game_over=True

        print_board(board)
    
    print("---------------------------")
    print("Number of moves: ",number_of_moves,"\nDept: ",depth,"\nheuristic of AI 1: ",heuristic_AI_1,"\nheuristic of AI 2: ",heuristic_AI_2)
    

def main():

    # after testing all functions below , create a menu for user to select game mode
    #human_vs_human()
    human_vs_ai()
    #ai_vs_ai()

if __name__ == "__main__":
    main()