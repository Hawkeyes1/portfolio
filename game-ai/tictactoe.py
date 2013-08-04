from search import make_negamax
from play import command_line_play

lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

# Always compute values from point of view of x's position.
# I.e. a win for x = 1, a win for y = -1
def terminal_value(board):
    for line in lines:
        if all(board[i] == 'x' for i in line):
            return 1
        if all(board[i] == 'o' for i in line):
            return -1
    if '.' not in board:
        return 0
    return None

def heuristic_value(board):
    total = 0
    for line in lines:
        xnum = sum(1 for i in line if board[i] == 'x')
        onum = sum(1 for i in line if board[i] == 'o')
        if xnum > onum:
            total += 1
        elif xnum < onum:
            total -= 1
    return total / 16.0

def to_str(board):
    return "{}{}{}\n{}{}{}\n{}{}{}".format(*board)

def empty_positions(board):
    return [i for i in range(9) if board[i] == "."]


def children(board):
    empty_pos = empty_positions(board)
    if len(empty_pos)%2:
        symbol = 'x'
    else:
        symbol = 'o'
    out = []
    for i in empty_pos:
        newlist = list(board)
        newlist[i] = symbol
        out.append(newlist)
    return out

negamax = make_negamax(terminal_value, heuristic_value, children)

def ask(board):
    # No error checking!
    i = int(raw_input("Your move?"))
    board[i] = 'o'
    return board

import sys
try:
    depth = int(sys.argv[1])
except:
    print "Usage: python tictactoe.py depth\n\ntry depth=5"
    sys.exit(0)
instructions = 'To enter your move, use the coordinates:\n012\n345\n678'
initial_board='.........'
command_line_play(initial_board,instructions,children,terminal_value,ask,\
                to_str,depth,negamax)
