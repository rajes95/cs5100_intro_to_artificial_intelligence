# Author: Rajesh Sakhamuru
# Version: 4/14/2019

import turtle
import random
import math

SQUARE = 50
UPPER_BOUNDARY = 125
LEFT_BOUNDARY = -175
RIGHT_BOUNDARY = 175
LOWER_BOUNDARY = -175
ORIGIN_X = 20
ORIGIN_Y = 0
HEIGHT = 6
WIDTH = 7
MAX_POS_Y_HEIGHT = 100

starting_piece = True
global game_state
global pos  # global pos is useful for end_game()
# function and for win condition testing.


def init_game():
    draw_board()
    create_board_state()
    create_game_listener()
    run_game()


def draw_board():
    ''' Function: draw_board
        Parameters: n, an int for # of squares
        Returns: nothing
        Does: Draws an nxn board with a yellow background
    '''

    turtle.setup(8 * SQUARE + SQUARE, 8 * SQUARE + SQUARE)
    turtle.screensize(HEIGHT * SQUARE, WIDTH * SQUARE)
    turtle.bgcolor('White')

    # Create the turtle to draw the board
    connect.penup()
    connect.speed(0)
    connect.hideturtle()

    # Line color is black, fill color is yellow
    connect.color("black", "yellow")

    # Move the turtle to the upper left corner
    corner = -WIDTH * SQUARE / 2
    connect.setposition(corner, corner)

    # Draw the yellow background
    connect.begin_fill()
    for i in range(4):
        connect.pendown()
        if i % 2 == 0:
            connect.forward(SQUARE * WIDTH)
        else:
            connect.forward(SQUARE * HEIGHT)
        connect.left(90)

    connect.end_fill()

    # Draw the horizontal lines
    for i in range(WIDTH):
        connect.setposition(corner, SQUARE * i + corner)
        draw_lines(connect, WIDTH)

    # Draw the vertical lines
    connect.left(90)
    for i in range(8):
        connect.setposition(SQUARE * i + corner, corner)
        draw_lines(connect, HEIGHT)


def draw_lines(turt, n):
    turt.pendown()
    turt.forward(SQUARE * n)
    turt.penup()


def create_board_state():
    """
    # Purpose
    This function takes the globally defined gate_state, and uses it to
    represent the game 'state'.  This may be most easily represented as a
    list of list
    # Signature
    create_board_state :: () => [[None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None]]
    """
    global game_state
    game_state = []
    i = 6
    while i > 0:
        game_state += [[None, None, None, None, None, None, None]]
        i -= 1
    return game_state


def create_game_listener():
    startMove = random.randint(0, 1)  # randomly chooses whether the AI or human goes first
    if startMove == 0:
        move_ai()

    turtle.onscreenclick(execute_move)


def execute_move(x, y):
    winner = False
    fullBoard = False
    pos_x = translate_pos(x)
    if pos_x > 175 or pos_x < -175:
        return print("ERROR: Column out of bounds", str(pos_x))

    pos_y = push_down_piece((pos_x, MAX_POS_Y_HEIGHT))
    valid_move = validate_move((pos_x, pos_y))
    if valid_move:
        draw_piece(pos_x, pos_y)
        winner = evaluate_for_winner(int(pos_x), int(pos_y))
        fullBoard = evaluate_for_full_board()
        if not winner and not fullBoard:
            move_ai()

# def generate_ai_move(state, piece):
# 
#     num = random.randint(0, 6)
#     return num  # column for the AI to put the piece into


def move_ai():

    state = game_state.copy()
    player = starting_piece
#     column = generate_ai_move(state, player)
    minimaxValue = minimax(state, 5, player)
    
    print(minimaxValue[0],minimaxValue[1])
    
    column = minimaxValue[1]

    column *= SQUARE
    x = (LEFT_BOUNDARY + 25) + column

    pos_x = translate_pos(x)
    pos_y = push_down_piece((pos_x, MAX_POS_Y_HEIGHT))
    valid_move = validate_move((pos_x, pos_y))
    if valid_move:
        draw_piece(pos_x, pos_y)
        evaluate_for_winner(int(pos_x), int(pos_y))
        evaluate_for_full_board()
    else:
        move_ai()


def get_valid_moves(state):
    validMoves = []
    for i in range(WIDTH):
        i *= SQUARE
        x = (LEFT_BOUNDARY + 25) + i
        pos_x = translate_pos(x)
        pos_y = push_down_piece((pos_x, MAX_POS_Y_HEIGHT))
        valid_move = validate_move((pos_x, pos_y))
        if valid_move:
            validMoves.append(pos_x)

    return validMoves


def is_terminal_state(state, player):

    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r][c + 1] == state[r][c + 2] == state[r][c + 3] is player:
                return True

    for r in range(HEIGHT - 3):
        for c in range(WIDTH):
            if state[r][c] == state[r + 1][c] == state[r + 2][c] == state[r + 3][c] is player:
                return True

    for r in range(3, HEIGHT):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r - 1][c + 1] == state[r - 2][c + 2] == state[r - 3][c + 3] is player:
                return True

    for r in range(HEIGHT - 3):
        for c in range(WIDTH - 3):
            if state[r][c] == state[r + 1][c + 1] == state[r + 2][c + 2] == state[r + 3][c + 3] is player:
                return True

    return False


def minimax(state, depth, player, alpha=-math.inf, beta=math.inf):
    validMoves = get_valid_moves(state)
    gameOver = is_terminal_state(state, player)


    if depth == 0 or gameOver:

        value = eval_state(state, player)

        return (value, 3 )
    if player:
        value = -math.inf
        col = random.choice(validMoves)
        for pos_x in validMoves:
            stateCopy = state.copy()
            pos_y = push_down_piece_AI((pos_x, MAX_POS_Y_HEIGHT), stateCopy)
            stateCopy[get_row_index(pos_y)][get_column_index(pos_x)] = True
            tempVal = minimax(stateCopy, depth - 1,False, alpha, beta)[0]
            if value < tempVal:
                value = tempVal
                col = pos_x
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return (value, ((col-20)/50)+4)
    else:  # other player
        value = math.inf
        col = random.choice(validMoves)
        for pos_x in validMoves:
            stateCopy = state.copy()
            pos_y = push_down_piece_AI((pos_x, MAX_POS_Y_HEIGHT), stateCopy)
            stateCopy[get_row_index(pos_y)][get_column_index(pos_x)] = False
            tempVal = minimax(stateCopy, depth - 1, True, alpha, beta)[0]
            if value > tempVal:
                value = tempVal
                col = pos_x
            if value < alpha:
                alpha = value
            if alpha >= beta:
                break
        return (value, ((col-20)/50)+4)


def push_down_piece_AI(pos, state):

    pos_x, pos_y = pos
    if state[get_row_index(pos_y)][get_column_index(pos_x)] is not None:
        return pos_y + 50
    elif get_row_index(pos_y) == 0:
        return pos_y
    else:
        return push_down_piece_AI((pos_x, pos_y - 50), state)


def eval_state(state, player):
    score = 0
    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            window = state[r][c:c + 4]
            if (window.count(player) == 4):
                score += 1000
            if (window.count(player) == 3 and window.count(None) == 1):
                score += 10
            if (window.count(player) == 2 and window.count(None) == 2):
                score += 4

    return score


def print_state(state):

    for r in range(HEIGHT - 1, -1, -1):
        for p in state[r]:
            if p is None:
                print("-", end="")
            elif p is True:
                print("1", end="")
            elif p is False:
                print("2", end="")
        print()
    print()


def push_down_piece(pos):
    global game_state
    pos_x, pos_y = pos
    if game_state[get_row_index(pos_y)][get_column_index(pos_x)] is not None:
        return pos_y + 50
    elif get_row_index(pos_y) == 0:
        return pos_y
    else:
        return push_down_piece((pos_x, pos_y - 50))


def translate_pos(x):
    if x < 0:
        pos_x = (-((-x + SQUARE / 2) // SQUARE) * SQUARE) + 20
    else:
        pos_x = (((x + SQUARE / 2) // SQUARE) * SQUARE) + 20
    return pos_x


def validate_move(pos):
    x, y = pos

    temp_x = get_column_index(x)
    temp_y = get_row_index(y)
    return pos_in_bounds(x, y) and game_state[temp_y][temp_x] is None


def pos_in_bounds(x, y):
    return RIGHT_BOUNDARY > x > LEFT_BOUNDARY and LOWER_BOUNDARY < y < UPPER_BOUNDARY


def get_column_index(x):
    if x // SQUARE >= 0:
        temp_x = int(x // SQUARE + 3)
    elif -x // SQUARE == 0:
        temp_x = 2
    elif -x // SQUARE == 1:
        temp_x = 1
    else:
        temp_x = 0

    return temp_x


def get_row_index(y):
    if y // SQUARE >= 0:
        temp_y = int(y // SQUARE + 3)
    elif -y // SQUARE == 3:
        temp_y = 0
    elif -y // SQUARE == 2:
        temp_y = 1
    else:
        temp_y = 2

    return temp_y


def draw_piece(x, y):
    global starting_piece, game_state
    if starting_piece:
        connect.color("black", "Red")
        starting_piece = False
        game_state[get_row_index(y)][get_column_index(x)] = False
    else:
        connect.color("black", "black")
        starting_piece = True
        game_state[get_row_index(y)][get_column_index(x)] = True
    connect.setposition(x, y)
    connect.pendown()
    connect.begin_fill()
    connect.circle(20)
    connect.end_fill()
    connect.penup()

#     print_state(game_state)
#     print(eval_state(game_state, starting_piece))
#     print(get_valid_moves(game_state))

def evaluate_for_winner(x, y):
    """
    # Purpose:
    # Signature:
    # Examples:
    """
    global game_state
    global pos
    pos = (x, y)

    gameOver = is_winning_move(pos)
    if gameOver:
        end_game()
        return gameOver


def is_winning_move(pos):
    return is_horizontal_win(pos) or is_vertical_win(pos) or is_diagonal_win(pos)


def is_horizontal_win(pos):
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
      is_horizontal_win :: ((170, -150)) => True

      game_state = [[None, None, False, False, True, False, None],
      [None, None, True, True, False, True, None],
      [None, None, False, False, False, False, None],
      [None, None, True, True, True, None, None],
      [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None]]
      is_horizontal_win :: ((120, -50)) => True
    """
    global game_state
    indY = get_row_index(pos[1])
    isWin = False
    for n in range(len(game_state[indY]) - 3):
        if game_state[indY][n] == game_state[indY][n + 1] == game_state[indY][n + 2]\
           == game_state[indY][n + 3] is not None:
            isWin = True
    return isWin


def is_vertical_win(pos):
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
      is_vertical_win :: ((-130, 0)) => True

      game_state = [[None, None, False, True, True, True, True], [None, None, False, False,
      False, None, None], [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None], [None, None, None, None, None, None, None],
      [None, None, None, None, None, None, None]]
      is_vertical_win :: ((170, -150)) => False
    """
    global game_state
    indX = get_column_index(pos[0])
    indY = get_row_index(pos[1])
    isWin = False
    if indY >= 3:
        if game_state[indY][indX] == game_state[indY - 1][indX] == \
           game_state[indY - 2][indX] == game_state[indY - 3][indX] is not None:
            isWin = True
    return isWin


def is_diagonal_win(pos):
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
      is_diagonal_win :: ((20, 100)) => True

      game_state = [[False, False, False, True, False, None, None],
      [True, True, False, False, False, None, None],
      [False, False, True, True, None, None, None], [True, True, True, None, None, None, None],
      [False, True, None, None, None, None, None], [True, None, None, None, None, None, None]]
      is_diagonal_win :: ((20, -50)) => True

    """
    isWin = False
    if is_right_to_left_win(pos) or is_left_to_right_win(pos):
        isWin = True
    return isWin


def is_right_to_left_win(pos):
    """
    # Purpose
      This method determines if a position creates a winning diagonal combination of pieces, from the
      bottom right to the top left
    # Signature
      is_right_to_left_win :: ((Integer, Integer)) => Integer
    """
    global game_state
    indX = get_column_index(pos[0])
    indY = get_row_index(pos[1])
    isWin = False
    if (indX + indY >= 3) and (indX + indY <= 8):
        diag = indY + indX + 1
        if diag <= 6:
            for n in range(diag - 3):
                if game_state[n][diag - n - 1] == game_state[n + 1][diag - n - 2]\
                   == game_state[n + 2][diag - n - 3] == game_state[n + 3][diag - n - 4] is not None:
                    isWin = True
        else:
            newDiag = indX + indY
            for n in range(8 - (newDiag - 4) - 3):
                if game_state[newDiag - 6 + n][6 - n] == \
                   game_state[newDiag - 5 + n][5 - n] == game_state[newDiag - 4 + n][4 - n] == \
                   game_state[newDiag - 3 + n][3 - n] is not None:
                    isWin = True
    return isWin


def is_left_to_right_win(pos):
    """
    # Purpose
      This method determines if a position creates a winning diagonal combination
      of pieces, from the bottom left to the top right
    # Signature
      is_left_to_right_win :: ((Integer, Integer)) => Integer
    """
    indX = get_column_index(pos[0])
    indY = get_row_index(pos[1])
    isWin = False
    if indY >= indX and (indY - indX) <= 2:
        diff = indY - indX
        for n in range(3 - diff):
            if game_state[diff + n][n] == game_state[diff + n + 1][n + 1]\
               == game_state[diff + n + 2][n + 2]\
               == game_state[diff + n + 3][n + 3] is not None:
                isWin = True
    elif indY < indX and (indX - indY) <= 3:
        diff = indX - indY
        for n in range(4 - diff):
            if game_state[n][diff + n] == game_state[n + 1][diff + n + 1]\
               == game_state[n + 2][diff + n + 2]\
               == game_state[n + 3][diff + n + 3] is not None:
                isWin = True
    return isWin


def evaluate_for_full_board():
    gameOver = board_full()
    if gameOver:
        end_game()
        return gameOver


def board_full():
    """
    # Purpose
      This function determines if the board is full
    # Signature
      board_full :: () => Boolean
    # Example:
      connect_four.game_state = [[False, True, False, False, False, True, False],
      [True, False, True, True, True, False, True],
      [False, True, False, False, False, True, False], [True, False, True, True, True,
      False, True], [False, True, False, False, False, True, False],
      [True, False, True, True, True, False, True]]
      connect_four.board_full :: () => True
    """
    global game_state
    NotTie = True
    for n in range(len(game_state[5])):
        if game_state[5][n] is None:
            NotTie = False
            break
    return NotTie


def end_game():
    """
    # Purpose:
      This function is called after a game ending move is made. It prints to
      the turtle screen the outcome of the match and calls functions which allow
      the game to be restarted.
    # Signature:
      end_game:: () => ()
    """
    global starting_piece
    global pos
    turtle.onscreenclick(None)
    connect.speed(0)
    connect.penup()
    connect.setposition(-70, 170)
    connect.pendown()
    if board_full() and not is_winning_move(pos):
        connect.write("The game is over, Tie!!!!")
    elif starting_piece:
        connect.write("The game is over, BLACK wins!!!!")
    else:
        connect.write("The game is over, RED wins!!!!")
    draw_end_buttons()
    turtle.onscreenclick(playAgain)


def draw_end_buttons():
    """
    # Purpose:
      Draws the buttons for play again, and exit after a game is over.
    # Signature:
      draw_end_buttons:: () => ()
    """
    connect.penup()
    connect.setposition(-110, 130)
    connect.pendown()
    connect.color("green", "green")
    connect.begin_fill()
    connect.setposition(-110, 165)
    connect.setposition(-25, 165)
    connect.setposition(-25, 130)
    connect.setposition(-110, 130)
    connect.end_fill()
    connect.color("red", "red")
    connect.penup()
    connect.setposition(25, 130)
    connect.pendown()
    connect.begin_fill()
    connect.setposition(25, 165)
    connect.setposition(110, 165)
    connect.setposition(110, 130)
    connect.setposition(25, 130)
    connect.end_fill()
    connect.color("black")
    connect.penup()
    connect.setposition(-98, 140)
    connect.pendown()
    connect.write("PLAY AGAIN")
    connect.penup()
    connect.setposition(58, 140)
    connect.pendown()
    connect.write("EXIT")
    connect.hideturtle()


def playAgain(x, y):
    """
    # Purpose:
      If the Play Again or Exit buttons are pressed, the apporopriate
      action is taken.
    # Signature:
      playAgain :: (int, int) => ()
    # Example:
      playAgain :: (100, 145) => resets turtle and reinitializes game.
    """
    if x >= -110 and x <= -25 and y >= 130 and y <= 165:
        connect.reset()
        connect.setposition(0, 0)
        connect.ht()
        init_game()
    elif x >= 25 and x <= 110 and y >= 130 and y <= 165:
        turtle.bye()


def run_game():
    try:
        turtle.done()
    except:
        pass


def main():
    init_game()


if '__main__' == __name__:
    connect = turtle.Turtle()
    main()
