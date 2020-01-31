# Author: Rajesh Sakhamuru
# Version: 4/14/2019


import unittest
import connect_four


class connectFourTests(unittest.TestCase):

    def testCreateBoardState(self):  # is board state created correctly?
        """
        GIVEN: nothing
        WHEN: create_board_state() function is called
        THEN: a [7][6] list of lists of None values is created
        """
        expected = [[None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]]
        boardState = connect_four.create_board_state()
        self.assertEqual(boardState, expected)

    def testIsHorizontalWin1(self):  # horizontal win BLACK
        """
        GIVEN: a game_state with a horizontal win, and the coordinates of the last placed piece
        WHEN: is_horizontal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, False, True, True, True, True],
                                   [None, None, False, False, False, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        isWin = connect_four.is_horizontal_win((170, -150))
        self.assertEqual(isWin, True)

    def testIsHorizontalWin2(self):  # horizontal win RED
        """
        GIVEN: a game_state with a horizontal win, and the coordinates of the last placed piece
        WHEN: is_horizontal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, False, False, True, False, None],
                                   [None, None, True, True, False, True, None],
                                   [None, None, False, False, False, False, None],
                                   [None, None, True, True, True, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        isWin = connect_four.is_horizontal_win((120, -50))
        self.assertEqual(isWin, True)

    def testIsHorizontalWin3(self):  # full board horizontal win
        """
        GIVEN: a game_state with a horizontal win, and the coordinates of the last placed piece
        WHEN: is_horizontal_win((x, y)) is called
        THEN: True is returned (even if the board is full)
        """
        connect_four.game_state = [[False, True, False, False, False, True, False],
                                   [False, False, True, True, True, False, True],
                                   [True, True, False, False, False, True, False],
                                   [False, False, True, True, True, False, True],
                                   [True, True, False, False, False, True, False],
                                   [False, True, True, True, True, False, True]]
        isWin = connect_four.is_horizontal_win((-80, 100))
        self.assertEqual(isWin, True)

    def testIsHorizontalWin4(self):  # Only 1 piece on board. not any win.
        """
        GIVEN: a game_state without any win, and the coordinates of the last placed piece
        WHEN: is_horizontal_win((x, y)) is called
        THEN: False is returned
        """
        connect_four.game_state = [[None, None, False, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        isWin = connect_four.is_horizontal_win((-30, -150))
        self.assertEqual(isWin, False)

    def testIsHorizontalWin5(self):  # Not a horizontal win
        """
        GIVEN: a game_state without a horizontal win, and the coordinates of the last placed piece
        WHEN: is_horizontal_win((x, y)) is called
        THEN: False is returned
        """
        connect_four.game_state = [[False, True, True, True, None, None, None],
                                   [None, False, False, True, None, None, None],
                                   [None, True, False, False, None, None, None],
                                   [None, None, None, False, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        isHorWin = connect_four.is_horizontal_win((20, 0))
        self.assertEqual(isHorWin, False)

    def testIsVerticalWin1(self):  # possible red vertical win
        """
        GIVEN: a game_state with a vertical win, and the coordinates of the last placed piece
        WHEN: is_vertical_win((x,y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[False, True, None, None, None, None, None],
                                   [False, True, None, None, None, None, None],
                                   [False, True, None, None, None, None, None],
                                   [False, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (-130, 0)
        isVerWin = connect_four.is_vertical_win(connect_four.pos)
        self.assertEqual(isVerWin, True)

    def testIsVerticalWin2(self):  # Not a vertical win (horizontal win)
        """
        GIVEN: a game_state without a vertical win, and the coordinates of the last placed piece
        WHEN: is_vertical_win((x,y)) is called
        THEN: False is returned
        """
        connect_four.game_state = [[None, None, False, True, True, True, True],
                                   [None, None, False, False, False, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (170, -150)
        isVerWin = connect_four.is_vertical_win(connect_four.pos)
        self.assertEqual(isVerWin, False)

    def testIsVerticalWin3(self):  # Full board vertical win
        """
        GIVEN: a game_state with a vertical win, and the coordinates of the last placed piece
               and a full board,
        WHEN: is_vertical_win((x,y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[True, False, False, True, True, False, True],
                                   [False, True, True, False, False, False, True],
                                   [True, False, False, True, True, True, False],
                                   [False, True, False, True, False, False, True],
                                   [True, False, False, True, True, True, False],
                                   [False, False, True, True, False, False, True]]
        connect_four.pos = (20, 100)
        isVerWin = connect_four.is_vertical_win(connect_four.pos)
        self.assertEqual(isVerWin, True)

    def testIsVerticalWin4(self):  # top left corner vertical win
        """
        GIVEN: a game_state with a vertical win, and the coordinates of the last placed piece
        WHEN: is_vertical_win((x,y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[True, False, False, None, None, None, None],
                                   [False, False, None, None, None, None, None],
                                   [True, None, None, None, None, None, None],
                                   [True, None, None, None, None, None, None],
                                   [True, None, None, None, None, None, None],
                                   [True, None, None, None, None, None, None]]
        connect_four.pos = (-130, 100)
        isVerWin = connect_four.is_vertical_win(connect_four.pos)
        self.assertEqual(isVerWin, True)

    def testIsVerticalWin5(self):  # bottom right vertical win
        """
        GIVEN: a game_state with a vertical win, and the coordinates of the last placed piece
        WHEN: is_vertical_win((x,y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, None, None, None, True, False],
                                   [None, None, None, None, None, True, False],
                                   [None, None, None, None, None, True, False],
                                   [None, None, None, None, None, None, False],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (170, 0)
        isVerWin = connect_four.is_vertical_win(connect_four.pos)
        self.assertEqual(isVerWin, True)

    def testIsDiagonalWin1(self):  # (0,0) left to right diagonal
        """
        GIVEN: a game_state with a diagonal win from the bottom left to top right
               from 0,0 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[False, True, True, True, None, None, None],
                                   [None, False, False, True, None, None, None],
                                   [None, True, False, False, None, None, None],
                                   [None, None, None, False, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (20, 0)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin2(self):  # (6,5) l2r diag
        """
        GIVEN: a game_state with a diagonal win from the bottom left to top right
               from 6,5 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, None, False, True, True, True],
                                   [None, None, None, True, False, False, True],
                                   [None, None, None, False, True, True, False],
                                   [None, None, None, None, False, False, True],
                                   [None, None, None, None, True, False, False],
                                   [None, None, None, None, None, None, False]]
        connect_four.pos = (170, 100)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin3(self):  # (3,5) l2r diag
        """
        GIVEN: a game_state with a diagonal win from the bottom left to top right
               from 3,5 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[False, True, True, True, None, None, None],
                                   [True, False, False, True, None, None, None],
                                   [False, True, True, False, None, None, None],
                                   [None, False, False, True, None, None, None],
                                   [None, True, False, False, None, None, None],
                                   [None, None, None, False, None, None, None]]
        connect_four.pos = (20, 100)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin4(self):  # (6,3) l2r diag
        """
        GIVEN: a game_state with a diagonal win from the bottom left to top right
               from 6,3 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, False, True, False, False, False],
                                   [None, None, None, None, True, True, False],
                                   [None, None, None, None, False, True, True],
                                   [None, None, None, None, None, None, True],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (170, 0)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin5(self):  # (0,3) r2l diag
        """
        GIVEN: a game_state with a diagonal win from the bottom right to top left
               from 0,3 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[True, True, True, False, None, None, None],
                                   [True, False, False, None, None, None, None],
                                   [False, False, True, None, None, None, None],
                                   [False, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (-130, 0)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin6(self):  # (0,5) r2l diag
        """
        GIVEN: a game_state with a diagonal win from the bottom right to top left
               from 0,5 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[False, False, False, True, False, None, None],
                                   [True, True, False, False, False, None, None],
                                   [False, False, True, True, None, None, None],
                                   [True, True, True, None, None, None, None],
                                   [False, True, None, None, None, None, None],
                                   [True, None, None, None, None, None, None]]
        connect_four.pos = (20, -50)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin7(self):  # (6,0) r2l diag
        """
        GIVEN: a game_state with a diagonal win from the bottom right to top left
               from 6,0 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, None, True, True, True, False],
                                   [None, None, None, False, False, False, None],
                                   [None, None, None, True, False, True, None],
                                   [None, None, None, False, True, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        connect_four.pos = (170, -150)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testIsDiagonalWin8(self):  # (6,2) r2l diag
        """
        GIVEN: a game_state with a diagonal win from the bottom right to top left
               from 6,2 , and the turtle coordinates of the center of that square
        WHEN: is_diagonal_win((x, y)) is called
        THEN: True is returned
        """
        connect_four.game_state = [[None, None, False, True, False, False, False],
                                   [None, None, False, True, False, False, True],
                                   [None, None, None, False, True, True, True],
                                   [None, None, None, True, False, True, None],
                                   [None, None, None, False, True, None, None],
                                   [None, None, None, True, None, None, None]]
        connect_four.pos = (20, 100)
        isDiagWin = connect_four.is_diagonal_win(connect_four.pos)
        self.assertEqual(isDiagWin, True)

    def testBoardFull1(self):  # full board
        """
        GIVEN: a game_state with a full board
        WHEN: board_full() is called
        THEN: True is returned
        """
        connect_four.game_state = [[False, True, False, False, False, True, False],
                                   [True, False, True, True, True, False, True],
                                   [False, True, False, False, False, True, False],
                                   [True, False, True, True, True, False, True],
                                   [False, True, False, False, False, True, False],
                                   [True, False, True, True, True, False, True]]
        isFull = connect_four.board_full()
        self.assertEqual(isFull, True)

    def testBoardFull2(self):  # board not full
        """
        GIVEN: a game_state without a full board
        WHEN: board_full() is called
        THEN: False is returned
        """
        connect_four.game_state = [[None, None, False, False, False, True, None],
                                   [None, None, True, True, False, True, None],
                                   [None, None, False, False, False, True, None],
                                   [None, None, True, True, False, None, None],
                                   [None, None, None, None, None, None, None],
                                   [None, None, None, None, None, None, None]]
        isFull = connect_four.board_full()
        self.assertEqual(isFull, False)

if __name__ == "__main__":
    unittest.main(exit=False)
