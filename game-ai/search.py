def make_negamax(terminal_value, heuristic_value, children):
    # This should probably be cached in a future version
    def negamax(node, depth, alpha, beta, color):
        tval = terminal_value(node)
        if tval != None:
            return color * tval
        elif depth == 0:
            hval = heuristic_value(node)
            return color * hval
        else:
            for child in children(node):
                val = - negamax(child, depth - 1, - beta, - alpha, - color)
                if val >= beta:
                    return val
                if val > alpha:
                    alpha = val
            return alpha
    return negamax
