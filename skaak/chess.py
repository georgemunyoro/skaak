from collections import namedtuple

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

WHITE = 0
BLACK = 1

EMPTY = "."

NORTH, EAST, SOUTH, WEST = -16, 1, 16, -1

Move = namedtuple(
    "Move",
    "initial_square target_square moving_piece attacked_piece capture score")

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
        SOUTH + WEST + EAST,
        SOUTH + EAST + EAST,
        EAST + EAST + SOUTH,
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
