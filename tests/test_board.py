from skaak import chess
from skaak import Chessboard


def test_board_set_starting_fen_by_default():
    board = Chessboard()
    assert board.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_board_repr():
    board = Chessboard()

    board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert str(board) == (
        "\nr n b q k b n r "
        "\np p p p p p p p "
        "\n. . . . . . . . "
        "\n. . . . . . . . "
        "\n. . . . . . . . "
        "\n. . . . . . . . "
        "\nP P P P P P P P "
        "\nR N B Q K B N R "
    )

    board.set_fen("3q4/kPpP4/4b1p1/2PP1n2/K3B3/1p6/8/4N1bN w - - 0 1")
    assert str(board) == (
        "\n. . . q . . . . "
        "\nk P p P . . . . "
        "\n. . . . b . p . "
        "\n. . P P . n . . "
        "\nK . . . B . . . "
        "\n. p . . . . . . "
        "\n. . . . . . . . "
        "\n. . . . N . b N "
    )

    board.set_fen("QBr3N1/1K6/R2ppP2/1n6/P3k3/6p1/1p5P/1b6 w - - 0 1")
    assert str(board) == (
        "\nQ B r . . . N . "
        "\n. K . . . . . . "
        "\nR . . p p P . . "
        "\n. n . . . . . . "
        "\nP . . . k . . . "
        "\n. . . . . . p . "
        "\n. p . . . . . P "
        "\n. b . . . . . . "
    )


def test_board_set_fen():
    board = Chessboard()

    fen_strings = (
        {
            "fen": "2k1b3/5P2/PKp2R1R/pp5P/3P4/8/B5r1/2BN4 w - - 0 1",
            "turn": chess.WHITE,
        },
        {
            "fen": "r5R1/3B4/3p3P/P7/1pN5/2pn1K2/N1k4r/R4n2 b - - 0 1",
            "turn": chess.BLACK,
        },
        {"fen": "2N5/3R4/p3k3/1R3pKp/3qp1b1/8/P6P/5NQn w - - 0 1", "turn": chess.WHITE},
    )

    for position in fen_strings:
        board.set_fen(position["fen"])

        assert board.fen == position["fen"]
        assert board.turn == position["turn"]


def test_board_move():
    board = Chessboard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    moves = (
        chess.Move(
            initial_square=96,
            target_square=64,
            moving_piece="P",
            attacked_piece=".",
            capture=False,
            score=None,
        ),
        chess.Move(
            initial_square=16,
            target_square=48,
            moving_piece="p",
            attacked_piece=".",
            capture=False,
            score=None,
        ),
        chess.Move(
            initial_square=112,
            target_square=48,
            moving_piece="R",
            attacked_piece="p",
            capture=True,
            score=None,
        ),
    )

    for move in moves:
        board.move(move)

        assert move.attacked_piece != board.board[move.target_square]
        assert move.moving_piece == board.board[move.target_square]
        assert board.board[move.initial_square] == "."


def test_board_move_gen():
    board = Chessboard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert board.perft(0) == 1
    assert board.perft(1) == 20
    assert board.perft(2) == 400
    assert board.perft(3) == 8902
    assert board.perft(4) == 197281
    assert board.perft(5) == 4865609


def test_board_undo_move():
    board = Chessboard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    og_board = board.board

    moves = (
        chess.Move(
            initial_square=96,
            target_square=64,
            moving_piece="P",
            attacked_piece=".",
            capture=False,
            score=None,
        ),
        chess.Move(
            initial_square=16,
            target_square=48,
            moving_piece="p",
            attacked_piece=".",
            capture=False,
            score=None,
        ),
        chess.Move(
            initial_square=113,
            target_square=80,
            moving_piece="N",
            attacked_piece=".",
            capture=False,
            score=None,
        ),
    )

    for move in moves:
        board.move(move)
        assert board.board != og_board
        board.undo_move()
        assert board.board == og_board
