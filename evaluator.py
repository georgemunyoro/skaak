# - George Guvamatanga
# - 18 September 2019
import math
import random
import re
import typing as t

from board import Chessboard


class Evaluator(object):
    def __init__(self, board: Chessboard) -> None:
        self.board = board

        # initiates board in case of error:
        self.board.init()

    def legal_moves_of_color(self, fen: str,
                             color: str) -> t.List[t.Dict[str, str]]:
        all_moves = self.board.calc_board_position_pos_moves(fen)
        color_pos_moves = []
        for move in all_moves:
            origin = move["origin"]
            if self.board.board_index[origin]["color"] == color:
                color_pos_moves.append(move)

        return color_pos_moves

    def piece_value(self, piece: str) -> int:
        if piece == "p" or piece == "P":
            return 100
        elif piece == "n" or piece == "N":
            return 350
        elif piece == "b" or piece == "B":
            return 350
        elif piece == "r" or piece == "R":
            return 525
        elif piece == "q" or piece == "Q":
            return 1000
        elif piece == "k" or piece == "K":
            return 10000
        else:
            return 0

    def piece_color(self, piece: str) -> t.Optional[str]:
        if piece == None or piece == "":
            return None
        if re.match("[a-z]+", str(piece)):
            return "b"
        elif re.match("[A-Z]+", str(piece)):
            return "w"

        return None

    def calc_pos(self, fen: str, color: str) -> int:
        self.board.position(fen)
        self.board.def_piece_colors()

        board_score = 0

        for square in self.board.board_index:
            if self.board.board_index[square]["color"] == color:
                piece_type = self.board.board_index[square]["type"]
                board_score += self.piece_value(piece_type)  # type: ignore

        return board_score

    T = t.TypeVar("T")

    def randomize_list(self, the_list: t.List[T]) -> t.List[T]:
        index = 0

        completed = []
        random_list = []

        while index != len(the_list):
            curr_random_item_index = int(random.randrange(0, len(the_list)))
            if curr_random_item_index in completed:
                pass
            else:
                # random_list[curr_random_item_index] = list[index]
                completed.append(curr_random_item_index)
                index += 1

        rand_list_index = -1
        for ref in completed:
            random_list.append(the_list[ref])
        return random_list

    def rate_move_rel(self, fen: str, color: str) -> int:
        opponent = None

        if color == "w":
            opponent = "b"
        else:
            opponent = "w"

        white_score = self.calc_pos(fen, "w")
        black_score = self.calc_pos(fen, "b")

        print("SCORE : ")
        print(white_score - black_score)
        print("--")

        if color == "w":
            return white_score - black_score
        else:
            return black_score - white_score

    def find_move(self, fen: str, color: str) -> t.Dict[str, str]:
        self.board.position(fen)

        og_pos = fen
        TEMP_BOARD = self.board

        best_move_so_far = None
        best_move_score = -1

        for move in self.randomize_list(self.legal_moves_of_color(fen, color)):
            self.board.move(move["origin"], move["dest"])
            if self.rate_move_rel(self.board.fen, color) > best_move_score:
                best_move_score = self.rate_move_rel(self.board.fen, color)
                best_move_so_far = move
            self.board.position(og_pos)

        return best_move_so_far  # type: ignore

    def randomMove(self, fen: str, color: str) -> t.Dict[str, str]:
        moves = self.legal_moves_of_color(fen, color)
        moves = self.randomize_list(moves)
        return moves[0]
