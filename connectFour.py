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
    return board[ROW_COUNT-1][col] == 0


def get_row(board, col):
    
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

# flips the board to drop all piaces to the bottom
def print_board(board):
    print("-----------------------------")
    temp=numpy.flip(board, 0).copy()
    for row in range(ROW_COUNT):
        print("|", end=" ")
        for col in range(COL_COUNT):
            print(temp[row][col], end=" ")
        print("|")

    print("  0 1 2 3 4 5 6 7")
    print("-----------------------------")



def possible_drop_locations(board):
    playable_locations = []
    for col in range(COL_COUNT):
        if is_playable(board, col):
            playable_locations.append(col)
    return playable_locations
    
# check the game is won or not, give different name to this function
def check_winner(board):
    print("check_winner")

    players = {1,2}


    for piece in players:
        
        # vertical four check
        for col in range(COL_COUNT):
            for row in range(ROW_COUNT-3):            
                if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                    return True, piece


        # horizontal four check
        for col in range(COL_COUNT-3):
            for row in range(ROW_COUNT):
                if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                    return True, piece

        # pozitive diagonal four check
        for col in range(COL_COUNT-3):
            for row in range(ROW_COUNT-3):
                if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                    return True, piece

        # negative diagonal four check
        for col in range(COL_COUNT-3):
            for row in range(3, ROW_COUNT):
                if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                    return True, piece       
    print("No winner")

    if len(possible_drop_locations(board)) <= 0:
        return True, 0
    else:
        return False, -1

# change turn function
def change_turn(turn):
    turn += 1
    turn = turn % 2  ##for which player is turn

    print("current turn:",turn)

    return turn


# funtion for celebrating the winner
def celebrate_winner(board, turn):
    print_board(board)    
    print("***************")
    print("\n    "+get_player_name(turn)+"\n     Wins !!\nCongratulations!\n")
    print("***************")

# return name of the player 
def get_player_name(turn):
    if turn == 0:
        return "Player 1 "
    else:
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


# Huristic ideas

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

    combine H1 and H2
    sum all the socre 
    return the score

    or 

    find the max score of H1 and H2
    return the max score

'''


weight_matrix = [
    [3, 4, 5, 7, 6, 5, 4, 3],
    [4, 6, 8, 10, 10, 8, 6, 4],
    [5, 8, 11, 13, 13, 11, 8, 5],
    [7, 10, 13, 16, 16, 13, 10, 7],
    [5, 8, 11, 13, 13, 11, 8, 5],
    [4, 6, 8, 10, 10, 8, 6, 4],
    [3, 4, 5, 7, 6, 5, 4, 3]
    ]


def huristic_2(board, piece):
    print("huristic_2")
    score=0
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == piece:
                score += weight_matrix[row][col]
            else:
                score -= weight_matrix[row][col]
    
    return score
    


def  huristic_1(board, piece):
    print("huristic_1")


def huristic_3(board, piece):
    print("huristic_3")

def select_huristic( ):    
    while True:
        huristic = int(input("Select huristic function (1-3): "))
        
        if huristic == 1:
            return  "huristic_1"
        elif huristic == 2:
            return "huristic_2"
        elif huristic == 3:
            return "huristic_3"
        else:
            print("Invalid input! Please try again.")
  


#def huristic_2(board, piece):
#def huristic__3(board, piece):        


# minimax algorithm
def minimax(board, depth,maximizingPlayer,huristic_type):
    
    playable_locations = possible_drop_locations(board)
        

    # Check if game is over or not
    is_terminal, winner = check_winner(board)
    if depth == 0 or is_terminal:
        # if game over
        if is_terminal:
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
            # huristic selection part

            # If depth equals 0 return evaluation score
            #if huristic_type == "huristic_1":
            #    return (None, huristic_1(board, AI))
            #elif huristic_type == "huristic_2":
            #    return (None, huristic_2(board, AI))
            #elif huristic_type == "huristic_3":
            #    return (None, huristic_3(board, AI))

            return (None, huristic_2(board, AI))

    if maximizingPlayer:
        max_value = float("-inf")
        
        column = random.choice(playable_locations)
        
        for col in playable_locations:
            row = get_row(board, col)

            # Create a temp board
            temp_board = board.copy()

            # simulation
            drop_piece(temp_board, row, col, AI)

            # until terminal or deepest board state
            current_score = minimax(temp_board, depth-1, False,huristic_type)[1]
            
            if current_score > max_value:
                value = current_score
                column = col
           
        return column, value

    else:
        value = float("inf")
        column = random.choice(playable_locations)
        for col in playable_locations:
            row = get_row(board, col)

            # Create a temp board
            temp_board = board.copy()

            # simulation
            drop_piece(temp_board, row, col, PLAYER)

            #until terminal or deepest board state
            min_score = minimax(temp_board, depth-1, True,huristic_type)[1]

            if min_score < value:
                value = min_score
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
    # select huristic type  
    huristic = select_huristic()
    print("huristic: ", huristic)

    # battle start human vs ai , human first
    print_board(board)

    while not is_game_over:
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
                    celebrate_winner(board, turn)                    
                    is_game_over=True
            else:
                print("Invalid move! Please try again.")
        #  player 2 (AI) turn
        else:
            # AI turn
            print("AI turn")
            
            col, minimax_score = minimax(board, depth, True, huristic)

            if is_playable(board, col):
                row = get_row(board, col)
                drop_piece(board, row, col, 2)
                turn = 0
                win_state,piece = check_winner(board)
                if win_state and piece==2:
                    celebrate_winner(board, turn)                    
                    is_game_over=True

        print_board(board) 

        
    
   

# AI VS AI


def main():

    # after testing all functions below , create a menu for user to select game mode
    #human_vs_human()
    human_vs_ai()
    #ai_vs_ai()

if __name__ == "__main__":
    main()