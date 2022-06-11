'''
Board class for the game of TicTacToe - 4.

Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Based on the board for the game of Othello by Eric P. Nichols and tictacToe by Evgeny Tyurin.

'''
# from bkcharts.attributes import color
from turtle import position
import numpy as np


class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    __jumps = [(2,2),(2,0),(2,-2),(0,-2),(-2,-2),(-2,0),(-2,2),(0,2)]

    def __init__(self, n = 5):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.

        # 1 indicates a hunter and -1 indicates a hare

        self.pieces = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 0, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ]

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def color_positions(self, color):
        "Returns the position of a piece on the board as a tuple"

        pos = np.argwhere(np.array(self.pieces) == color).tolist()

        return pos

    def legal_move(self, position):
        "Returns if a move is legal"
        return (
            (position[0] >= 0) and (position[0] < 5) 
            and (position[1] >= 0) and (position[1] < 5) 
            and self.pieces[position[0]][position[1]] == 0
        )

    def get_moves(self, piece_pos, color):
        """
        Return posible next positions based on the type of piece, its position on the board, and the board itself
        ---
        Returns a numpy array of posible moves
        """

        if (piece_pos[0] + piece_pos[1]) % 2 == 0:
            movement_set = np.array(
                [
                    (-1,-1), (0,-1), (1,-1),
                    (-1, 0),         (1, 0), 
                    (-1, 1), (0, 1), (1, 1)
                ]
            )
        else:
            movement_set = np.array(
                [
                            (0,-1),
                    (-1, 0),         (1, 0), 
                            (0, 1),
                ]
            )

        initial_legal_moves = [(m[0]+piece_pos[0], m[1]+piece_pos[1]) for m in movement_set if self.legal_move([m[0]+piece_pos[0], m[1]+piece_pos[1]])]

        return initial_legal_moves

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for hunters, -1 for hare)
        @param color not used and came from previous version.        
        """

        pieces_pos = self.color_positions(color)

        moves = set()

        for p in pieces_pos:

            ms = self.get_moves(p, color)

            if len(ms)>0:
                for m in ms:
                    moves.add((p[0], p[1], m[0], m[1]))

        return list(moves)

    def has_legal_moves(self, player=-1):

        return len(self.get_legal_moves(player)) > 0
    
    def is_win(self, color):
        """Check whether the given player has blocked the other player
        """

        return len(self.get_legal_moves(-color)) == 0 or len(self.color_positions(-color)) < 9

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        start_0, start_1, end_0, end_1 = move

        self.pieces[start_0][start_1] = 0
        self.pieces[end_0][end_1] = color

if __name__ == "__main__":
    
    b = Board()

    print(b.get_legal_moves(1))