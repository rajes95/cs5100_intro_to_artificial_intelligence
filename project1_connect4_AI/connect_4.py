# CS 5100
# Author: Rajesh Sakhamuru
# Version: 10/14/2019

import random
import math

HEIGHT = 6
WIDTH = 7

AI_PIECE = False
PLAYER_PIECE = True


def init_game():
    """
    # Purpose
    This is the only function called by the main() of this program. 
    The board state is initialized and all the slots are made 'None' values.
    Whether the user or the AI goes first is determined randomly.
    The AI exectes their moves via the minimax algorithm and the user executes
    their moves by entering a column number via the user_input funciton.
    The end of the game is determined and indicated as well when it happens.
    # Signature
    init_game :: () => None
    """
    board = create_board_state()
    print_state(board)
    turnCount = random.randint(0, 1)  # randomly picks who goes first
    gameOver = False
    winner = None
    while (not board_full(board)):

        if turnCount % 2 == 0:

            col = user_input(board)

            gameOver = execute_move(col, board, PLAYER_PIECE)

            if gameOver:
                winner = PLAYER_PIECE
                break

            print_state(board)
            turnCount += 1
        else:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

            # Increase depth to raise AI strength (or decrease it to lower strength)
            # 1 is quite easy to beat, as it cannot predict future user moves
                # (it only looks 1 move (its own) into the future)
            # 2 is tough, but beatable
            # 3 and above are extremely difficult to win against
            minimaxValue = minimax(board, 5, AI_PIECE)

            print("AI drops piece into column:", minimaxValue[1] + 1)
#             print("MiniMax value: ", minimaxValue[0])  # useful for diagnosing AI

            gameOver = execute_move(minimaxValue[1], board, AI_PIECE)

            if gameOver:
                winner = AI_PIECE
                break

            print_state(board)
            turnCount += 1

    end_game(board, winner)

    return


def create_board_state():
    """
    # Purpose
    This function creates a list to represent the game 'state'.  This may be 
    most easily represented as a list of lists
    # Signature
    create_board_state :: () => [[None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None]]
    """
    game_state = []
    i = 6
    while i > 0:
        game_state += [[None, None, None, None, None, None, None]]
        i -= 1
    return game_state


def print_state(state):
    """
    # Purpose
    Prints out a visual represntation of the game state that is passed to it
    as a parameter.
    # Signature
    print_state :: (state) => visual state print output
    # Example
    print_state :: ([[None, None, None, True, False, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]]) =>
                                                                |1|2|3|4|5|6|7|
                                                                _______________
                                                                | | | | | | | |
                                                                | | | | | | | |
                                                                | | | | | | | |
                                                                | | | | | | | |
                                                                | | | | | | | |
                                                                | | | |1|0| | |
     
    """
    print("|1|2|3|4|5|6|7|")
    print("_______________")
    for r in range(HEIGHT - 1, -1, -1):
        print("|", end="")
        count = 0
        for p in state[r]:
            if p is None:
                print(" |", end="")
            elif p is True:
                print("1|", end="")
            elif p is False:
                print("0|", end="")
            count += 1
        print()
    print()


def user_input(state):
    """
    # Purpose
    Takes user input, and only accepts a move into the valid columns. Will catch
    input error.
    # Signature
    user_input :: (state) => col # column number of user input    
    """

    valid_moves = get_valid_moves(state)

    valid_moves = [n + 1 for n in valid_moves]

    try:
        col = int(input("USER, enter column number: "))
        print()
        if col not in valid_moves:
            raise ValueError
        col = col - 1
    except ValueError:
        print("ERROR: Please input a valid column number.")
        print("Valid columns are: ", valid_moves, end="\n\n")

        col = user_input(state)

    return col


def get_valid_moves(state):
    """
    # Purpose
    This function returns a list of column numbers in a given state that a user 
    or AI could put a piece into and make a legal move. It is a list of Columns 
    that are not full yet.
    # Signature 
    get_valid_moves:: (state) => [1,2,3,4,5,6 or 7 (or multiple of them)]
    """
    valid_moves = []

    for n in range(WIDTH):
        if state[5][n] is None:
            valid_moves.append(n)

    return valid_moves


def execute_move(col, state, player):
    """
    # Purpose
    This function passes the move by the indicated player onto the board after 
    calculating the correct row to place it onto using push_down_piece(). It also
    checks if the move made is the winning move or not and returns the bool value. 
    # Signature
    execute_move:: (col,state,player_piece) => bool
    """
    gameOver = False
    row = push_down_piece(col, state)
    play_piece(col, row, state, player)
    if is_winning_move((col, row), state):
        print_state(state)
        gameOver = True
    return gameOver


def push_down_piece(c, state):
    """
    # Purpose
    Returns highest None space row-number in 'state' in column 'c'.
    # Signature
    push_down_piece :: (column, game_state) => (row_number)
    """
    for r in range(HEIGHT):
        if state[r][c] == None:
            return r


def play_piece(col, row, state, player):
    """
    # Purpose
    Places the piece at the indicated location onto the state provided.
    # Signature
    play_piece :: (col,row,state,player) => None
    """
    state[row][col] = player


def is_winning_move(pos, state):
    """
    # Purpose
    Tests the squares in the state, only the ones near enough to the played piece to possibly 
    create a win, in the horizontal, vertical and diagonal directions. 
    # Signature
    is_winning_move :: (pos,state) => boolean
    """
    return is_horizontal_win(pos, state) or is_vertical_win(pos, state) or is_diagonal_win(pos, state)


def is_horizontal_win(pos, state):
    """
    # Purpose:
      This method determines if a position creates a winning combination of pieces horizontally
    # Signature:
      is_horizontal_win :: ((Integer, Integer)) => Boolean
    # Examples:
      game_state = [[None, None, False, True, True, True, True],
                    [None, None, False, False, False, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]]
      is_horizontal_win :: ((6, 0)) => True

      game_state = [[None, None, False, False, True, False, None],
      [None, None, True, True, False, True, None],
      [None, None, False, False, False, False, None],
      [None, None, True, True, True, None, None],
      [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None]]
      is_horizontal_win :: ((6, 2)) => True
    """
    indY = pos[1]
    isWin = False
    for n in range(len(state[indY]) - 3):
        if state[indY][n] == state[indY][n + 1] == state[indY][n + 2]\
           == state[indY][n + 3] is not None:
            isWin = True
    return isWin


def is_vertical_win(pos, state):
    """
    # Purpose:
      This method determines if a position creates a winning combination of pieces vertically
    # Signature:
      is_vertical_win :: ((Integer, Integer)) => Boolean
    # Examples:

      game_state = [[False, True, None, None, None, None, None], [False, True, None, None, None,
      None, None], [False, True, None, None, None, None, None],
      [False, None, None, None, None, None, None],
      [None, None, None, None, None, None, None], [None, None, None, None, None, None, None]]
      is_vertical_win :: ((0, 3)) => True

      game_state = [[None, None, False, True, True, True, True], [None, None, False, False,
      False, None, None], [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None], [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None]]
      is_vertical_win :: ((6, 0)) => False
    """

    indX = pos[0]
    indY = pos[1]
    isWin = False
    if indY >= 3:
        if state[indY][indX] == state[indY - 1][indX] == \
           state[indY - 2][indX] == state[indY - 3][indX] is not None:
            isWin = True
    return isWin


def is_diagonal_win(pos, state):
    """
    # Purpose:
      This method determines if the most recently placed piece creates a diagonal
      winning combination of pieces. Checks for both left to right and right to left
      diagonal combinations.
    # Signature:
      is_diagonal_win :: ((Integer, Integer)) => Boolean
    # Examples:

      game_state = [[False, True, True, True, None, None, None], [True, False, False, True,
      None, None, None], [False, True, True, False, None, None, None],
      [None, False, False, True, None, None, None], [None, True, False, False, None, None, None],
      [None, None, None, False, None, None, None]]
      is_diagonal_win :: ((3, 5)) => True

      game_state = [[False, False, False, True, False, None, None],
      [True, True, False, False, False, None, None],
      [False, False, True, True, None, None, None], [True, True, True, None, None, None, None],
      [False, True, None, None, None, None, None], [True, None, None, None, None, None, None]]
      is_diagonal_win :: ((3, 3)) => True

    """
    isWin = False
    if is_right_to_left_win(pos, state) or is_left_to_right_win(pos, state):
        isWin = True
    return isWin


def is_right_to_left_win(pos, state):
    """
    # Purpose
      This method determines if a position creates a winning diagonal combination of pieces, from the
      bottom right to the top left
    # Signature
      is_right_to_left_win :: ((Integer, Integer)) => Integer
    """
    indX = pos[0]  # col
    indY = pos[1]  # row
    isWin = False
    if (indX + indY >= 3) and (indX + indY <= 8):
        diag = indY + indX + 1
        if diag <= 6:
            for n in range(diag - 3):
                if state[n][diag - n - 1] == state[n + 1][diag - n - 2]\
                   == state[n + 2][diag - n - 3] == state[n + 3][diag - n - 4] is not None:
                    isWin = True
        else:
            newDiag = indX + indY
            for n in range(8 - (newDiag - 4) - 3):
                if state[newDiag - 6 + n][6 - n] == \
                   state[newDiag - 5 + n][5 - n] == state[newDiag - 4 + n][4 - n] == \
                   state[newDiag - 3 + n][3 - n] is not None:
                    isWin = True
    return isWin


def is_left_to_right_win(pos, state):
    """
    # Purpose
      This method determines if a position creates a winning diagonal combination
      of pieces, from the bottom left to the top right
    # Signature
      is_left_to_right_win :: ((Integer, Integer)) => Integer
    """
    indX = pos[0]
    indY = pos[1]
    isWin = False
    if indY >= indX and (indY - indX) <= 2:
        diff = indY - indX
        for n in range(3 - diff):
            if state[diff + n][n] == state[diff + n + 1][n + 1]\
               == state[diff + n + 2][n + 2]\
               == state[diff + n + 3][n + 3] is not None:
                isWin = True
    elif indY < indX and (indX - indY) <= 3:
        diff = indX - indY
        for n in range(4 - diff):
            if state[n][diff + n] == state[n + 1][diff + n + 1]\
               == state[n + 2][diff + n + 2]\
               == state[n + 3][diff + n + 3] is not None:
                isWin = True
    return isWin


def board_full(state):
    """
    # Purpose
      This function determines if the board is full
    # Signature
      board_full :: (board) => Boolean
    # Example:
      state = [[False, True, False, False, False, True, False],
      [True, False, True, True, True, False, True],
      [False, True, False, False, False, True, False], [True, False, True, True, True,
      False, True], [False, True, False, False, False, True, False],
      [True, False, True, True, True, False, True]]
      connect_four.board_full :: (state) => True
    """

    NotTie = True
    for n in range(len(state[5])):
        if state[5][n] is None:
            NotTie = False
            break
    return NotTie


def minimax(state, depth, player, alpha=-math.inf, beta=math.inf):
    """
    # Purpose
    The minimax algorithm traverses all potential beneficial moves from the 
    given state, 'depth' number of moves into the future, and uses the evaluation
    of those future states to determine,which column for the AI to move their peice
    into. 
    
    Alpha/Beta pruning is used to prevent expanding branches which are definitly
    not going to be picked by the algorithm. 
    
    The Cutting off search goes to a maximum depth as indicated by the 'depth'
    parameter.
    
    The value and column of the best move are returned as a tuple 
    
    # Signature
    minimax  :: (state,depth,player,alpha,beta) => (value, column)
    """
    validMoves = get_valid_moves(state)
    random.shuffle(validMoves)
    gameOver = is_terminal_state(state, AI_PIECE)

    if depth == 0 or gameOver or len(validMoves) == 0:
        value = eval_state(state, AI_PIECE)
        return (value, None)

    if player:  # USER
        value = math.inf
        column = random.choice(validMoves)
        for col in validMoves:

            stateCopy = [l.copy() for l in state.copy()]

            row = push_down_piece(col , stateCopy)
            play_piece(col, row, stateCopy, PLAYER_PIECE)
            tempVal = minimax(stateCopy, depth - 1, AI_PIECE, alpha, beta)[0]

            if value > tempVal:
                value = tempVal
                column = col

            # alpha/beta pruning
            if value < beta:
                beta = value
            if alpha >= beta:
                break

        return (value, column)

    else:  # AI PLAYER (because AI_PIECE is False)
        value = -math.inf
        column = random.choice(validMoves)

        for col in validMoves:

            stateCopy = [l.copy() for l in state.copy()]

            row = push_down_piece(col, stateCopy)
            play_piece(col, row, stateCopy, AI_PIECE)

            tempVal = minimax(stateCopy, depth - 1, PLAYER_PIECE, alpha, beta)[0]

            if value < tempVal:
                value = tempVal
                column = col

            # alpha/beta pruning
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break

        return (value, column)


def is_terminal_state(state, player):
    """
    # Purpose
    This function takes a state and a player value, and returns a boolean 
    value indicating whether or not that state is a winning state for the
    indicated player. This function is used to identify terminal states in the 
    minimax algorithm.
    # Signature
    is_terminal_state :: (state, player_piece) => boolean
    """
    # test all horizontals
    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r][c + 1] == state[r][c + 2] == state[r][c + 3] is player:
                return True
    # test all verticals
    for r in range(HEIGHT - 3):
        for c in range(WIDTH):
            if state[r][c] == state[r + 1][c] == state[r + 2][c] == state[r + 3][c] is player:
                return True

    # test all diagonals
    for r in range(3, HEIGHT):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r - 1][c + 1] == state[r - 2][c + 2] == state[r - 3][c + 3] is player:
                return True

    for r in range(HEIGHT - 3):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r + 1][c + 1] == state[r + 2][c + 2] == state[r + 3][c + 3] is player:
                return True

    return False


def eval_state(state, player):
    """
    # Purpose
    Evalates states visited by the minimax algorithm for their float value to the 
    player indicated. The algorithm awards points based on position of the player
    and the the player's opponent. Horizontal, vertical, diagonal, and winning positions
    all are scored, as well as lower rows and center rows being worth more than other 
    rows.
    # Signature
    eval_state :: (state, player) => value 
    
    """
    value = 0

    if is_terminal_state(state, player):
        value += 10000
    if is_terminal_state(state, not player):
        value -= 100000

    # AI favors center columns and lower rows
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if state[r][c] == player:
                value += 3 - math.fabs(3 - c)
                value += 5 - r

    # Consecutive horizontals are given value here
    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            chunk = state[r][c:c + 4]
            if (chunk.count(player) == 3 and chunk.count(None) == 1):
                value += 20
            if (chunk.count(player) == 2 and chunk.count(None) == 2):
                value += 8
            if chunk.count(not player) == 3 and chunk.count(None) == 1:
                value -= 20

    # Consecutive verticals are given value
    for c in range(WIDTH):
        columnArray = []
        for i in range(HEIGHT):
            columnArray.append(state[i][c])
        for r in range(HEIGHT - 3):
            chunk = columnArray[r:r + 3]
            if (chunk.count(player) == 3 and chunk.count(None) == 1):
                value += 19
            if (chunk.count(player) == 2 and chunk.count(None) == 2):
                value += 7
            if chunk.count(not player) == 3 and chunk.count(None) == 1:
                value -= 16

    # Consecutive diagonals are given value
    for r in range(3, HEIGHT):
        for c in range(WIDTH - 3):
            chunk = []
            chunk.append(state[r][c])
            chunk.append(state[r - 1][c + 1])
            chunk.append(state[r - 2][c + 2])
            chunk.append(state[r - 3][c + 3])
            if (chunk.count(player) == 3 and chunk.count(None) == 1):
                value += 18
            if (chunk.count(player) == 2 and chunk.count(None) == 2):
                value += 6
            if chunk.count(not player) == 3 and chunk.count(None) == 1:
                value -= 15

    for r in range(HEIGHT - 3):
        for c in range(WIDTH - 3):
            chunk = []
            chunk.append(state[r][c])
            chunk.append(state[r + 1][c + 1])
            chunk.append(state[r + 2][c + 2])
            chunk.append(state[r + 3][c + 3])
            if (chunk.count(player) == 3 and chunk.count(None) == 1):
                value += 18
            if (chunk.count(player) == 2 and chunk.count(None) == 2):
                value += 6
            if chunk.count(not player) == 3 and chunk.count(None) == 1:
                value -= 15

    return value


def end_game(board, winner):
    """
    # Purpose
    When the game is over, this function takes the winner, and board state,
    and prints the result of the game, Win, lose or tie.
    """
    if winner is None:
        if board_full(board):
            print("GAME OVER. RESULT IS A TIE.")
    elif winner:
        print("GAME OVER. USER wins.")
    else:
        print("GAME OVER. AI wins.")


def main():
    """
    # Purpose
    Runs the init_game() function and in effect the entirety of the program.
    """
    init_game()
    return


main()
