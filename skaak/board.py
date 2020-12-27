from itertools import count
from typing import List

import skaak.chess as chess


class Chessboard:
    """
    Representation of the classic Chessboard and it's rules
    """

    def __init__(self, fen: str = chess.STARTING_FEN, **kwargs) -> None:
        self.fen: str = chess.STARTING_FEN

        self.board: str = ""
        self.castling: str = ""
        self.en_pas: str = ""

        self.history: List[Chessboard] = [0] * 2048

        self.full: int = 0
        self.half: int = 0
        self.set_fen(fen)

    @property
    def white_king_position(self) -> int:
        try:
            return self.board.index("K")
        except:
            return -1

    @property
    def black_king_position(self) -> int:
        try:
            return self.board.index("k")
        except:
            return -1

    @property
    def legal_moves(self) -> List[chess.Move]:
        return self.generate_legal_moves()

    def __repr__(self) -> str:
        """Returns the ASCII representation of the current state of the board"""
        ascii_repr: str = ""

        for i, char in enumerate(self.board):
            if i % 16 == 0:
                ascii_repr += "\n"

            if i & 0x88 == 0:
                ascii_repr += char + " "

        return ascii_repr

    @staticmethod
    def _128_index_to_san(index: int) -> str:
        """Converts index of square on 128 board representation to SAN(Standard Algebraic Notation)"""
        file = 8 - (index // 16)
        rank = chess.RANKS[index % 16]
        return f"{rank}{file}"

    @staticmethod
    def _draw_indexed_board(highlighted_squares: List[int] = []) -> None:
        for i in range(128):
            if i & 0x88 != 0:
                continue
            if i % 8 == 0:
                print("\n")
            if i in highlighted_squares:
                i = "*"
            print("{:>4}".format(i), end=" ")
        print("\n")

    def move(self, move: chess.Move) -> None:
        self.history[self.half] = self.generate_fen()
        self.turn ^= 1

        if (0x88 & move.initial_square) != 0:
            raise chess.InvalidMove(
                f"Invalid Move : {move.moving_piece} from square {move.initial_square} to square {move.target_square}, occupied by {move.attacked_piece}"
            )

        temp = list(self.board)

        if (0x88 & move.target_square) == 0:
            temp[move.target_square] = move.moving_piece

        temp[move.initial_square] = chess.EMPTY
        self.board = "".join(temp)

        self.half += 1

    def undo_move(self) -> None:
        self.half -= 1
        self.set_fen(self.history[self.half])

    def get_square_color(self, square: int) -> int:
        """Returns the color of the piece on a given square"""
        if self.board[square] == chess.EMPTY:
            return None

        if self.board[square].isupper():
            return chess.WHITE
        return chess.BLACK

    def is_square_attacked(self, square: int) -> bool:
        if square & 0x88 != 0:
            return None

        if (self.board[square] != chess.EMPTY) and self.get_square_color(
            square
        ) != self.turn:
            return None

        for direction in chess.MOVES["r"]:
            for i in count(square + direction, direction):
                if (i & 0x88) != 0:
                    break
                if (self.board[i].isupper() and self.turn == chess.WHITE) or (
                    self.board[i].islower() and self.turn == chess.BLACK
                ):
                    break

                if self.board[i].lower() in "rq":
                    return True
                elif self.board[i] == chess.EMPTY:
                    continue
                else:
                    break

        for direction in chess.MOVES["b"]:
            for i in count(square + direction, direction):
                if (i & 0x88) != 0:
                    break
                if (
                    self.board[i].isupper()
                    and self.turn == chess.WHITE
                    or self.board[i].islower()
                    and self.turn == chess.BLACK
                ):
                    break

                if self.board[i].lower() in "bq":
                    return True
                elif self.board[i] == chess.EMPTY:
                    continue
                else:
                    break

        if self.turn == chess.WHITE:
            if (
                self.board[square + chess.NORTH + chess.EAST] == "p"
                or self.board[square + chess.NORTH + chess.WEST] == "p"
            ):
                return True
        elif self.turn == chess.BLACK:
            if (
                self.board[square + chess.SOUTH + chess.EAST] == "P"
                or self.board[square + chess.SOUTH + chess.WEST] == "P"
            ):
                return True

        non_sliding_pieces = ["k", "n"]
        for piece_type in non_sliding_pieces:
            for i in chess.MOVES[piece_type]:
                if (square + i) & 0x88 == 0:
                    if (
                        self.board[square + i] == piece_type.lower()
                        and self.turn == chess.WHITE
                    ) or (
                        self.board[square + i] == piece_type.upper()
                        and self.turn == chess.BLACK
                    ):
                        return True

        return False

    def generate_fen(self) -> str:
        """Generates a board state in the form of an FEN string"""
        fen = ""
        empty_square_count = 0
        for i, j in enumerate(self.board):
            if (i & 0x88) != 0:
                if empty_square_count > 0:
                    fen += str(empty_square_count)
                    empty_square_count = 0
                continue
            if i % 8 == 0 and i != 0:
                fen += "/"
            if j in chess.PIECES:
                if empty_square_count > 0:
                    fen += str(empty_square_count)
                    empty_square_count = 0
                fen += j
            elif j == chess.EMPTY:
                empty_square_count += 1

        return (
            fen
            + f' {"wb"[self.turn]} {self.castling} {self.en_pas} {self.half} {self.full}'
        )

    def generate_legal_moves(self) -> List[chess.Move]:
        for move in self.generate_pseudo_moves():
            self.move(move)
            self.turn ^= 1
            if not self.in_check() and (
                self.white_king_position != -1 or self.black_king_position != -1
            ):
                yield (move)
            self.turn ^= 1
            self.undo_move()

    def generate_pseudo_moves(self) -> List[chess.Move]:
        """Generates moves that may more may not be potentially harmful to the king"""

        for square, piece in enumerate(self.board):
            if (square & 0x88) != 0:
                continue

            if self.turn == chess.WHITE and not piece.isupper():
                continue
            elif self.turn == chess.BLACK and not piece.islower():
                continue

            for direction in chess.MOVES[piece.lower() if piece != "P" else piece]:
                for j in count(square + direction, direction):

                    # Check if the square is offboard
                    if (j & 0x88) != 0:
                        break

                    # Ensure the piece at the square is not of the same color
                    if self.board[square].isupper() and self.board[j].isupper():
                        break
                    elif self.board[square].islower() and self.board[j].islower():
                        break

                    if piece.lower() == "p":
                        if (
                            self.turn == chess.WHITE
                            and direction == (chess.NORTH * 2)
                            and (
                                square // 16 != 6
                                or self.board[square + chess.NORTH] != chess.EMPTY
                            )
                        ) or (
                            self.turn == chess.BLACK
                            and direction == (chess.SOUTH * 2)
                            and (
                                square // 16 != 1
                                or self.board[square + chess.SOUTH] != chess.EMPTY
                            )
                        ):
                            break
                        if (j % 16 != square % 16) and self.board[j] in "-.":
                            break
                        if (j % 16 == square % 16) and self.board[j] not in "-.":
                            break
                        if (j // 8 - square // 8) ** 1 == 1 and self.board[
                            j - ((j // 8 - square // 8) * 8)
                        ] != "":
                            break

                    yield (
                        chess.Move(
                            initial_square=square,
                            target_square=j,
                            moving_piece=self.board[square],
                            attacked_piece=self.board[j],
                            capture=(self.board[j] not in "-."),
                            score=0,
                        )
                    )

                    if self.board[j] not in "-." or piece.lower() in "knp":
                        break

    def in_check(self) -> bool:
        return (
            self.is_square_attacked(self.white_king_position)
            if self.turn == chess.WHITE
            else self.is_square_attacked(self.black_king_position)
        )

    def perft(self, depth: int) -> int:
        legal_moves = self.legal_moves
        nodes = 0

        if depth == 0:
            return 1

        for move in legal_moves:
            self.move(move)
            nodes += self.perft(depth - 1)
            self.undo_move()

        return nodes

    def set_fen(self, fen: str) -> None:
        """Sets the current board state to match that of the given FEN string"""

        board, turn, castling, en_pas, half, full = fen.split()

        temp = ""
        for char in board:
            if char.isdigit():
                temp += "." * int(char)
            elif char == "/":
                temp += "-" * 8
            elif char.lower() in "rnbqkp":
                temp += char
        temp += "-" * 8

        self.board = temp
        self.turn = chess.WHITE if turn == "w" else chess.BLACK

        self.castling = castling
        self.en_pas = en_pas
        self.half = int(half)
        self.full = int(full)

        self.fen = fen


if __name__ == "__main__":
    mb = Chessboard()
    for i in range(10):
        print(mb.perft(i))
