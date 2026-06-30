"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x = 0
    o = 0
    for column in board:
        for item in column:
            if item == "X":
                x += 1
            elif item == "O":
                o += 1

    if x == o:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    row = 0
    while True:
        if row == 3:
            return set(possible_actions)
        column = 0
        while True:
            if column == 3:
                break
            if board[row][column] == None:
                possible_actions.append((row, column))
            column += 1
        row += 1


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    class InvalidActionError(Exception):
        pass
    if board[action[0]][action[1]] != None:
        raise InvalidActionError("Attempted to move in an occupied space")
    elif action[0] < 0 or action[1] < 0 or action[0] > 2 or action[1] > 2:
        raise InvalidActionError("Attempted to move out of bounds")
    new_board = [row.copy() for row in board]
    turn = player(new_board)
    if turn == "X":
        new_board[action[0]][action[1]] = "X"
    else:
        new_board[action[0]][action[1]] = "O"
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    index = 0
    while True:
        if index == 0:
            winning_player = "X"
        elif index == 1:
            winning_player = "O"
        else:
            break

        win_condition_found = False
        # Check for win conditions around the center point

        if board[1][1] == winning_player:
            if board[0][0] == winning_player and board[2][2] == winning_player:
                win_condition_found = True
            elif board[2][0] == winning_player and board[0][2] == winning_player:
                win_condition_found = True

        if win_condition_found == False:
            # Check for the other win conditions
            variable_distance = 0
            mode = "horizontal"
            row = 0
            column = 1
            while True:
                if mode == "horizontal":

                    # Switch the loop to check fo vertical win conditions
                    if variable_distance == 3:
                        mode = "vertical"
                        row = 1
                        variable_distance = 0
                        column = variable_distance
                    else:
                        # Check the next horizontal win condtition
                        row = variable_distance
                else:
                    # No win conditions found.
                    if variable_distance == 3:
                        break

                    # Check for the next vertical win condition
                    else:
                        column = variable_distance

                # Check to see if the source square is the right player
                if board[row][column] == winning_player:

                    # Check for horizontal win conditions
                    if mode == "horizontal":
                        if board[row][column-1] == winning_player and board[row][column+1] == winning_player:
                            win_condition_found = True
                            break

                    # Check for vertical win conditions
                    else:
                        if board[row-1][column] == winning_player and board[row + 1][column] == winning_player:
                            win_condition_found = True
                            break
                variable_distance += 1

        # A winner is found, return it.
        if win_condition_found == True:
            return winning_player
        else:
            index += 1

    # There is no winner, so return NONE.
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_found = False

    # Check to see if there are any EMPTY squares
    for row in board:
        for item in row:

            # If there is an EMPTY square, break
            if item == EMPTY:
                empty_found = True
                break

    # If no EMPTY squares are found, the game is over
    if empty_found == False:
        return True

    # If there is empty squares, check for a winner
    else:
        new_winner = winner(board)

        # If there is any winner, the game is over
        if new_winner != None:
            return True

        # If there are empty squares and no winnerm the game is NOT over.
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    new_winner = winner(board)

    # X is the winner, so return 1
    if new_winner == "X":
        return 1

    # O is the winner, so return -1
    elif new_winner == "O":
        return -1

    # There is no winner, so return 0
    return 0


class Node():
    # 'move' should be a list as follows: [player, [row, column]]
    # The second item in the list is a pair of coordinates for the last move.
    def __init__(self, move, board):
        self.move = move
        self.board = board


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    Moves should have a list of of lists formated as follows:
    [[node...,], game score]

    Moves should only contain the set of nodes that have the HIGHEST score possible at the end
    """

    # Check to see if the game is alread over
    if terminal(board) == True:
        return None

    current_player = player(board)

    def make_move(board):
        if terminal(board):
            if winner(board) == current_player:
                return 1
            elif winner(board) == None:
                return 0
            else:
                return -1

        score = None
        possible_moves = actions(board)
        new_player = player(board)
        for move in possible_moves:
            new_score = make_move(result(board, move))
            if score == None:
                score = new_score
                continue
            if new_player != current_player:
                if new_score == -1:
                    return -1
                elif score > new_score:
                    score = new_score
            elif new_player == current_player:
                if new_score == 1:
                    return 1
                elif score < new_score:
                    score = new_score
        return score

    best_move = [[], -2]
    possible_moves = actions(board)
    for move in possible_moves:
        move_score = make_move(result(board, move))
        if move_score == 1:
            return tuple(move)
        elif move_score > best_move[1]:
            best_move = [move, move_score]
    return tuple(best_move[0])
