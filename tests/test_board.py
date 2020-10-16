from skaak import Chessboard


def test_board_set_starting_fen_by_default():
    board = Chessboard()
    assert board.fen == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

def test_board_repr():
    board = Chessboard()

    board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert str(board) == (
                        '\nr n b q k b n r '
                        '\np p p p p p p p '
                        '\n. . . . . . . . '
                        '\n. . . . . . . . '
                        '\n. . . . . . . . '
                        '\n. . . . . . . . '
                        '\nP P P P P P P P '
                        '\nR N B Q K B N R '
                    )

    board.set_fen('3q4/kPpP4/4b1p1/2PP1n2/K3B3/1p6/8/4N1bN w - - 0 1')
    assert str(board) == (
                        '\n. . . q . . . . '
                        '\nk P p P . . . . '
                        '\n. . . . b . p . '
                        '\n. . P P . n . . '
                        '\nK . . . B . . . '
                        '\n. p . . . . . . '
                        '\n. . . . . . . . '
                        '\n. . . . N . b N '
                    )

    board.set_fen('QBr3N1/1K6/R2ppP2/1n6/P3k3/6p1/1p5P/1b6 w - - 0 1')
    assert str(board) == (
                        '\nQ B r . . . N . '
                        '\n. K . . . . . . '
                        '\nR . . p p P . . '
                        '\n. n . . . . . . '
                        '\nP . . . k . . . '
                        '\n. . . . . . p . '
                        '\n. p . . . . . P '
                        '\n. b . . . . . . '
                    )

def test_board_set_fen():
    pass

def test_board_move():
    pass

def test_board_undo_move():
    pass
