"""
Name: Monte Carlo Tic-Tac-Toe
Author: jraleman
Year: 2014
"""

try:
    import poc_ttt_gui
    import poc_ttt_provided as provided
except ImportError:
    import assets.poc_ttt_gui as poc_ttt_gui
    import assets.poc_ttt_provided as provided
import random

# Constants for Monte Carlo simulator
NTRIALS = 10
MCMATCH = 1.0
MCOTHER = 1.0

def mc_trial(board, player):
    """
    Takes a current board and the next player to move.
    """
    while board.check_win() == None:
        random_move = random.randrange(len(board.get_empty_squares()))
        next_move = board.get_empty_squares()[random_move]
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Function to update the scores.
    """
    if board.check_win() == player :
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += MCMATCH
                else:
                    scores[row][col] -= MCOTHER
    elif board.check_win() == None or board.check_win() == provided.DRAW:
        return
    else:
        for row_index in range(board.get_dim()):
            for col_index in range(board.get_dim()):
                if board.square(row_index, col_index) == player:
                    scores[row_index][col_index] -= MCMATCH
                else:
                    scores[row_index][col_index] += MCOTHER

def mc_move(board, player, trials):
    """
    The function should use the Monte Carlo simulation described above to
    return a move for the machine player in the form of a tuple.
    """
    number = trials
    scores = [[[] for row in range(board.get_dim())] \
    for col in range(board.get_dim())]

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            scores[row][col] = 0

    while number:
        board1 = board.clone()
        mc_trial(board1, player)
        mc_update_scores(scores, board1, player)
        number -= 1

    next_move = get_best_move(board, scores)
    return next_move

def get_best_move(board, scores):
    """
    Choose the square with the highest score as the nest move.
    """
    # No available moves.
    if len(board.get_empty_squares()) == 0:
        return
    available = []
    for move in board.get_empty_squares():
        available.append(scores[move[0]][move[1]])
    best = max(available)
    poss_moves = []
    index = 0
    while index < len(available):
        if available[index] == best:
            poss_moves.append(board.get_empty_squares()[index])
        index += 1
    return random.choice(poss_moves)

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
