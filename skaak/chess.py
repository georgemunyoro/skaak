STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

WHITE = 0
BLACK = 1

EMPTY = "."

NORTH, EAST, SOUTH, WEST = -16, 1, 16, -1

PIECES = "rnbqkpRNBQKP"


def convert_x88_board_ref_to_san(x88_board_ref: int) -> str:
    pos_rank = 8 - (x88_board_ref // 16)
    pos_file = "abcdefgh"[x88_board_ref % 16]
    return f"{pos_file}{pos_rank}"


class Move:
    def __init__(self, **kwargs):
        self.initial_square: int = kwargs.pop("initial_square", None)
        self.target_square: int = kwargs.pop("target_square", None)
        self.moving_piece: int = kwargs.pop("moving_piece", None)
        self.attacked_piece: int = kwargs.pop("attacked_piece", None)
        self.capture: bool = kwargs.pop("capture", None)
        self.score: int = kwargs.pop("score", None)
        self.pseudo: bool = kwargs.pop("pseudo", None)

    def __repr__(self) -> str:
        return f"{convert_x88_board_ref_to_san(self.initial_square)}{convert_x88_board_ref_to_san(self.target_square)}"


RANKS = "abcdefgh"

MOVES = {
    "P": (
        NORTH,
        NORTH + NORTH,
        NORTH + EAST,
        NORTH + WEST,
    ),
    "p": (
        SOUTH,
        SOUTH + SOUTH,
        SOUTH + EAST,
        SOUTH + WEST,
    ),
    "n": (
        NORTH + NORTH + EAST,
        NORTH + EAST + EAST,
        NORTH + WEST + WEST,
        SOUTH + SOUTH + EAST,
        NORTH + NORTH + WEST,
        SOUTH + EAST + EAST,
        WEST + SOUTH + SOUTH,
        WEST + WEST + SOUTH,
    ),
    "k": (
        NORTH,
        NORTH + EAST,
        NORTH + WEST,
        SOUTH,
        SOUTH + WEST,
        SOUTH + EAST,
        EAST,
        WEST,
    ),
    "q": (
        NORTH,
        NORTH + EAST,
        NORTH + WEST,
        SOUTH,
        SOUTH + WEST,
        SOUTH + EAST,
        EAST,
        WEST,
    ),
    "b": (
        NORTH + EAST,
        NORTH + WEST,
        SOUTH + WEST,
        SOUTH + EAST,
    ),
    "r": (
        NORTH,
        SOUTH,
        EAST,
        WEST,
    ),
}


class InvalidMove(Exception):
    pass
