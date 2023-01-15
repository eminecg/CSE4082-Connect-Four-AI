# CSE4082 ARTIFICIAL INTELLIGENCE ASSIGNMENT 2

# Connect-Four

Connect-Four is a tic-tac-toe-like two-player game in which players alternately place pieces on a vertical board 8 columns across and 7 rows high. The objective of the game is to be the first player to obtain four pieces in a horizontal, vertical, or diagonal line. The game is implemented in python, and it can be played in three different modes:

- Human player vs Human player
- Human player vs AI player
- AI player vs AI player

For the AI player, the minimax algorithm with alpha-beta pruning is implemented. Additionally, three evaluation (heuristic) methods (h1, h2, and h3) are provided, which can be configured to be used by the AI player. The complexity of the AI player can be configured by adjusting the number of plies (i.e., the depth of the tree) and the evaluation heuristic to be used.

## Getting Started

To run the game, you will need to have python3 and the following libraries installed:

- numpy
- random
- math

To run the game, you can simply execute the command:

python .\connectFour.py

## AI Player Configuration

The complexity of the AI player can be configured by adjusting the number of plies (i.e., the depth of the tree) and the evaluation heuristic to be used. The available evaluation heuristics are:

H1:

Calcuates score of consequetive pieces of each player then returns the difference
Calculates conseutives as 2, 3, 4 pieces for the player
For 2 conseutive pieces, multiply number of occurence by 100
For 3 conseutive pieces, multiply number of occurence by 1000
For 4 conseutive pieces, multiply number of occurence by 10000000000

H2:

Used weight matrix, score is added with the weight values of each index of the board for max player, and subtracted for min player

Calculates score of consequetive pieces of each player then returns the difference to add to the score

H3:

Calculates score of consequetive pieces and the consequtive starting index lists for each consequetive type for each player

Check the center score of each consequetive type list if it not empty and add it to the score for the max player

Check the center score of each consequetive type list if it not empty and subtract it from the score for the min player

Get the difference between the max player score and the min player score to return it

## Authors

- Emine Çığ
- Ahsen Yağmur Kahyaoğlu
