STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

WHITE = 0
BLACK = 1

EMPTY = "."

NORTH, EAST, SOUTH, WEST = -16, 1, 16, -1

PIECES = "rnbqkpRNBQKP"

class Move:
    def __init__(self, **kwargs):
        self.initial_square: int = kwargs.pop('initial_square', None)
        self.target_square: int = kwargs.pop('target_square', None)
        self.moving_piece: int = kwargs.pop('moving_piece', None)
        self.attacked_piece: int = kwargs.pop('attacked_piece', None)
        self.capture: bool = kwargs.pop('capture', None)
        self.score: int = kwargs.pop('score', None)
        self.pseudo: bool = kwargs.pop('pseudo', None)

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
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
