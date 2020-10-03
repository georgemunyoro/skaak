# - George Guvamatanga
# - 18 September 2019
import math
import random
import re
from typing import List

from board import Chessboard


class Evaluator(object):
    def __init__(self, board: Chessboard):
        self.board = board

        # initiates board in case of error:
        self.board.init()

    def legal_moves_of_color(self, fen, color) -> List[str]:
        all_moves = self.board.calc_board_position_pos_moves(fen)
        color_pos_moves = []
        for move in all_moves:
            origin = move["origin"]
            if self.board.board_index[origin]["color"] == color:
                color_pos_moves.append(move)

        return color_pos_moves

    def piece_value(self, piece) -> int:
        values = {"p": 100, "n": 350, "b": 350, "r": 525, "q": 1000, "k": 10000}
        piece = piece.lower()
        return values[piece]

    def piece_color(self, piece) -> str:
        if piece == None or piece == "":
            return None
        if re.match("[a-z]+", str(piece)):
            return "b"
        elif re.match("[A-Z]+", str(piece)):
            return "w"

    def calc_pos(self, fen, color) -> int:
        self.board.position(fen)
        self.board.def_piece_colors()

        board_score = 0

        for square in self.board.board_index:
            if self.board.board_index[square]["color"] == color:
                piece_type = self.board.board_index[square]["type"]
                board_score += self.piece_value(piece_type)

        return board_score

    def randomize_list(self, list) -> List[int]:
        index = 0

        completed = []
        random_list = []

        while index != len(list):
            curr_random_item_index = int(random.randrange(0, len(list)))
            if curr_random_item_index in completed:
                pass
            else:
                # random_list[curr_random_item_index] = list[index]
                completed.append(curr_random_item_index)
                index += 1

        rand_list_index = -1
        for ref in completed:
            random_list.append(list[ref])
        return random_list

    def rate_move_rel(self, fen, color) -> int:
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

        return (
            white_score - black_score if (color == "w") else black_score - white_score
        )

    def find_move(self, fen, color) -> int:
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

        return best_move_so_far

    def randomMove(self, fen, color) -> int:
        moves = self.legal_moves_of_color(fen, color)
        moves = self.randomize_list(moves)
        return moves[0]
