from search import make_negamax
from play import command_line_play

# Represent board as a matrix board[i][j]


# Always compute values from point of view of x's position.
# I.e. a win for x = 1, a win for o = -1

lines = []
# Vertical lines
for i in range(7):
    for j in range(3):
        lines.append([(i,x) for x in range(j,j+4)])
for j in range(6):
    for i in range(4):
        lines.append([(x,j) for x in range(i,i+4)])
for i in range(4):
    for j in range(3):
        lines.append([(i+x,j+x) for x in range(4)])
for i in range(3,7):
    for j in range(3):
        lines.append([(i-x,j+x) for x in range(4)])
num_lines = float(len(lines))


def terminal_value(board):
    for line in lines:
        if all(board[i][j] == 'x' for (i,j) in line):
            return 1
        if all(board[i][j] == 'o' for (i,j) in line):
            return -1
    if any(col[-1] == '_' for col in board):
        return None
    return 0


def heuristic_value(board):
    total = 0
    for line in lines:
        a = sum(1 for (i,j) in line if board[i][j] == 'x')
        b = sum(1 for (i,j) in line if board[i][j] == 'o')
        if a == 0:
            total -= b**2
        elif b == 0:
            total += a**2
    return total / (16*num_lines)


def to_str(board):
    vals = [' ' for loop in range(42)]
    for i in range(7):
        vals[i::7] = reversed(board[i])
    return '''1 2 3 4 5 6 7
{} {} {} {} {} {} {}
{} {} {} {} {} {} {}
{} {} {} {} {} {} {}
{} {} {} {} {} {} {}
{} {} {} {} {} {} {}
{} {} {} {} {} {} {}'''.format(*vals)

def insert(board,i,symbol):
    assert type(i) is int
    assert i in range(7)
    assert board[i][-1] == '_'
    j = min([j for j in range(6) if board[i][j] == '_'])
    board = list(list(x) for x in board)
    board[i][j] = symbol
    return board


def children(board):
    total = 0
    for col in board:
        for elem in col:
            if elem == 'x':
                total += 1
            elif elem == 'o':
                total -= 1
    if total == 0:
        symbol = 'x'
    elif total == 1:
        symbol = 'o'
    out = []
    for i in range(7):
        if board[i][-1] == '_':
            out.append(insert(board,i,symbol))
    return out

negamax = make_negamax(terminal_value, heuristic_value, children)

def ask(board):
    i = None
    while i == None:
        try:
            i = int(raw_input("Your move?"))
            return insert(board,i-1,'o')
        except:
            i = None

if __name__ == '__main__':
    import sys
    try:
        depth = int(sys.argv[1])
    except:
        print "Usage: python connect-four.py depth\n\ntry depth=5"
        sys.exit(0)
    instructions = 'For Connect Four rules, search online.'
    initial_board=[['_']*6 for loop in range(7)]
    command_line_play(initial_board,instructions,children,terminal_value,ask,\
                    to_str,depth,negamax)


