"""
Name: Mini-max Tic-Tac-Toe Player
Author: jraleman
Year: 2014
"""

try:
    import poc_ttt_gui
    import poc_ttt_provided as provided
except ImportError:
    import assets.poc_ttt_gui as poc_ttt_gui
    import assets.poc_ttt_provided as provided

# Scoring values.
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    Returns a tuple with two elements. The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # Base case.
    if board.check_win() is not None:
        return SCORES[board.check_win()], (-1, -1)

    # Worst possible initial values.
    result = (-1, (-1, -1))

    # Depth first search along the tree.
    for move in board.get_empty_squares():
        copied_board = board.clone()
        copied_board.move(move[0], move[1], player)
        score, _ = mm_move(copied_board, provided.switch_player(player))

        # Best possible choice found.
        if score * SCORES[player] == 1:
            return score, move

        # Update the initial values
        elif score * SCORES[player] > result[0]:
            result = (score, move)
        elif result [0] == -1:
            result = (result[0], move)

    return result [0] * SCORES[player], result[1]


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    # Returned illegal move (-1, -1).
    assert move[1] != (-1, -1)
    return move[1]

provided.play_game(move_wrapper, 1, False)
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
