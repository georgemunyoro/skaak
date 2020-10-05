import math
import re
import typing as t


class Chessboard(object):
    STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    # def __init__(self, fen: str = Chessboard.STARTING_FEN) -> None:

    def __init__(self, fen: str = STARTING_FEN) -> None:
        self.board_index: t.Dict[str, t.Dict[str, t.
                                             Union[None, str, int]]] = {}
        self.files = "abcdefgh"
        self.fen = fen

        # - Initializing functions
        self.init()

    def __repr__(self):
        self.draw_ascii()

    def init(self) -> None:
        # - Keeps track of which square is being worked on :
        square_index = 1
        file_index = 1

        while square_index <= 64:

            # - Data used to define the square
            square_rank = 8 - int(square_index / 8)
            square_file = self.files[file_index - 1]

            if square_index % 8 == 0:
                square_rank += 1

            if square_rank < 1:
                break

            square_ref = "{file}{rank}".format(file=square_file,
                                               rank=square_rank)

            self.board_index[square_ref] = {
                "index": square_index,
                "color": None,
                "type": None,
            }

            if file_index % 8 == 0:
                file_index = 1
            else:
                file_index += 1

            square_index

    def get_rank_squares(self, rank: int) -> t.List[str]:
        squares: t.List[str] = []
        for square in self.board_index:
            if str(square)[1] == str(rank):
                squares.append(str(square))
        return squares

    def draw_rank(self, rank: int) -> str:
        result: t.List[str] = []
        squares = self.get_rank_squares(rank)
        for square in squares:
            if self.board_index[square]["type"] != None:
                result.append(self.board_index[square]["type"])  # type: ignore
            else:
                result.append("-")
        drawing = ""
        for square in result:
            drawing += square
            drawing += "    "
        return drawing

    def draw_ascii(self) -> None:
        rank_index = 8
        while rank_index >= 1:
            print("")
            print("{rank}   |   {rank_drawing}".format(
                rank=rank_index, rank_drawing=self.draw_rank(rank_index)))
            print("")
            rank_index -= 1
        print("-" * 44)
        print("")
        print("        a    b    c    d    e    f    g    h".upper())

    def reset_board_position(self) -> None:
        self.position(Chessboard.STARTING_FEN)

    def get_ref_from_index(self, index: int) -> str:
        for square in self.board_index:
            if int(self.board_index[str(square)]
                   ["index"]) == index:  # type: ignore
                return str(square)
        else:
            # mypy complaining about it not returning in all cases.  # mypy complaining about it not returning in all cases.
            raise IndexError("index not found")

    def def_piece_colors(self) -> None:
        for square in self.board_index:
            self.board_index[str(square)]["color"] = self.def_square_color(
                str(square))

    def position(self, fen: str) -> None:
        square_index = 1
        self.fen = fen
        fen = self.parse_fen(fen)

        for char in fen:
            if char == "1":
                self.board_index[self.get_ref_from_index(
                    square_index)]["type"] = None

            elif char == "/":
                square_index = square_index
                square_index -= 1

            elif re.match("[a-zA-Z]+", char):
                self.board_index[self.get_ref_from_index(
                    square_index)]["type"] = char

            square_index += 1

    def parse_fen(self, fen: str) -> str:
        resulting_fen = ""
        for char in fen:
            if re.match("[0-9]+", char):
                resulting_fen += "1" * int(char)
            else:
                resulting_fen += char
        return resulting_fen

    def highlight_moves(self, squares: t.List[t.Optional[str]]) -> None:
        for square in squares:
            if square == None:
                pass
            else:
                if self.board_index[str(square)]["type"] == None:
                    self.board_index[str(square)]["type"] = "*"
                else:
                    # type: ignore
                    self.board_index[str(square)]["type"] += "*"

    def def_square_color(self, square: str) -> t.Optional[str]:
        piece = self.board_index[str(square)]["type"]
        if piece == None:
            return None
        if re.match("[a-z]+", str(piece)):
            self.board_index[str(square)]["color"] = "b"
        elif re.match("[A-Z]+", str(piece)):
            self.board_index[str(square)]["color"] = "w"
        return self.board_index[str(square)]["color"]  # type: ignore

    def clean_moves(self, origin: str,
                    moves: t.List[t.Optional[str]]) -> t.List[str]:
        clean_moves: t.List[str] = []
        for move in moves:
            if move == None:
                pass
            else:
                if (self.board_index[str(origin)]["color"] == self.board_index[
                        str(move)]["color"]):
                    pass
                else:
                    clean_moves.append(str(move))
        return clean_m

    def calc_board_position_pos_moves(self,
                                      fen: str) -> t.List[t.Dict[str, str]]:
        moves: t.List[t.Dict[str, str]] = []
        self.position(fen)
        for square in self.board_index:
            piece = self.board_index[str(square)]["type"]
            color = self.board_index[str(square)]["color"]
            possible_moves = self.calc_piece_pos_moves(piece, str(square),
                                                       color)  # type: ignore
            for move in possible_moves:
                move_obect = {
                    "origin": "{origin}".format(origin=str(square)),
                    "dest": "{dest}".format(dest=str(move)),
                }
                moves.append(move_obect)
        return moves

    def calc_piece_pos_moves(self, piece: str, pos: str,
                             color: str) -> t.List[t.Optional[str]]:
        possible_moves: t.List[t.Optional[str]] = []
        # - Calculates moves for a knight (N / n)
        if piece == "n" or piece == "N":
            position_index = int(
                self.board_index[pos]["index"])  # type: ignore

            possible_moves.append(self.get_ref_from_index(position_index - 17))
            possible_moves.append(self.get_ref_from_index(position_index - 15))
            possible_moves.append(self.get_ref_from_index(position_index - 10))
            possible_moves.append(self.get_ref_from_index(position_index - 6))
            possible_moves.append(self.get_ref_from_index(position_index + 6))
            possible_moves.append(self.get_ref_from_index(position_index + 10))
            possible_moves.append(self.get_ref_from_index(position_index + 15))
            possible_moves.append(self.get_ref_from_index(position_index + 17))

            if pos[0] == "a" or pos[0] == "b":
                possible_moves[4] = None
                possible_moves[2] = None
                if pos[0] == "a":
                    possible_moves[0] = None
                    possible_moves[6] = None

            if pos[0] == "g" or pos[0] == "h":
                possible_moves[3] = None
                possible_moves[5] = None
                if pos[0] == "h":
                    possible_moves[1] = None
                    possible_moves[7] = None

            if pos[1] == "7" or pos[1] == "8":
                possible_moves[0] = None
                possible_moves[1] = None
                if pos[1] == "8":
                    possible_moves[2] = None
                    possible_moves[3] = None

            if pos[1] == "1" or pos[1] == "2":
                possible_moves[6] = None
                possible_moves[7] = None
                if pos[1] == "h":
                    possible_moves[4] = None
                    possible_moves[5] = None

        # - Calculates moves for a bishop (B / b)
        if piece == "b" or piece == "B":
            og_pos_index: int = self.board_index[pos]["index"]  # type: ignore

            valid = True
            index = og_pos_index
            curr_square = index - 9
            diag_index = 9

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                else:
                    possible_moves.append(square_ref)
                    # type: ignore
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 9
                    elif directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7

        # - Calculates moves for a rook (R / r)
        if piece == "r" or piece == "R":
            og_pos_index = self.board_index[pos]["index"]  # type: ignore

            valid = True
            index = og_pos_index
            curr_square = index - 8

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                else:
                    possible_moves.append(square_ref)
                    # type: ignore
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 8
                    elif directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1

        # - Calculates moves for a queen (Q / q)
        if piece == "q" or piece == "Q":
            og_pos_index = self.board_index[pos]["index"]  # type: ignore

            valid = True
            index = og_pos_index
            curr_square = index - 8

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                else:
                    possible_moves.append(square_ref)
                    # type: ignore
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 8
                    elif directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1

            valid = True
            index = og_pos_index
            curr_square = index - 9

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                else:
                    possible_moves.append(square_ref)
                    # type: ignore
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 9
                    elif directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7

        # - Calculates moves for a king (K / k)
        if piece == "k" or piece == "K":
            square_index = int(self.board_index[pos]["index"])  # type: ignore
            possible_moves.append(self.get_ref_from_index(square_index - 9))
            possible_moves.append(self.get_ref_from_index(square_index - 8))
            possible_moves.append(self.get_ref_from_index(square_index - 7))
            possible_moves.append(self.get_ref_from_index(square_index - 1))
            possible_moves.append(self.get_ref_from_index(square_index + 1))
            possible_moves.append(self.get_ref_from_index(square_index + 7))
            possible_moves.append(self.get_ref_from_index(square_index + 8))
            possible_moves.append(self.get_ref_from_index(square_index + 9))

            if pos[0] == "a":
                possible_moves[0] = None
                possible_moves[3] = None
                possible_moves[5] = None

            if pos[0] == "h":
                possible_moves[2] = None
                possible_moves[4] = None
                possible_moves[7] = None

            if pos[1] == "1":
                possible_moves[5] = None
                possible_moves[6] = None
                possible_moves[7] = None

            if pos[1] == "8":
                possible_moves[0] = None
                possible_moves[1] = None
                possible_moves[2] = None

            # safe_possible_moves = []
            possible_moves = self.clean_moves(pos,
                                              possible_moves)  # type: ignore

            # 	for move in possible_moves:
            # 		if(self.safe(move)): safe_possible_moves.append(move)

            # 	possible_moves = safe_possible_moves

        # - Calculates moves for a pawn (P / p)
        if piece == "p" or piece == "P":
            piece_index: int = self.board_index[pos]["index"]  # type: ignore

            if color == "w":

                one_ahead_index = int(piece_index) - 8
                two_ahead_index = int(piece_index) - 16

                l_diag = None
                r_diag = None

                if pos[1] != "8":
                    if pos[0 != "a"]:
                        # type: ignore
                        l_diag = int(self.board_index[pos]["index"]) - 9

                    if pos[0 != "h"]:
                        # type: ignore
                        r_diag = int(self.board_index[pos]["index"]) - 7

                l_diag = self.get_ref_from_index(l_diag)
                r_diag = self.get_ref_from_index(r_diag)

                if pos[1] == "2":
                    if (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] == None
                            and self.board_index[self.get_ref_from_index(
                                one_ahead_index)]["type"] == None):
                        possible_moves.append(
                            self.get_ref_from_index(one_ahead_index))
                        possible_moves.append(
                            self.get_ref_from_index(two_ahead_index))
                        return possible_moves
                    elif (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] != None
                          and self.board_index[self.get_ref_from_index(
                              one_ahead_index)]["type"] == None):
                        possible_moves.append(
                            self.get_ref_from_index(one_ahead_index))
                        return possible_moves
                    elif (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] == None
                          and self.board_index[self.get_ref_from_index(
                              one_ahead_index)]["type"] != None):
                        return []
                if r_diag != None:
                    if (self.board_index[r_diag]["color"] !=
                            self.board_index[pos]["color"]
                            and self.board_index[r_diag]["type"] != None):
                        possible_moves.append(r_diag)

                if l_diag != None:
                    if (self.board_index[l_diag]["color"] !=
                            self.board_index[pos]["color"]
                            and self.board_index[l_diag]["type"] != None):
                        possible_moves.append(l_diag)

                if (self.board_index[self.get_ref_from_index(one_ahead_index)]
                    ["type"] == None):
                    possible_moves.append(
                        self.get_ref_from_index(one_ahead_index))
                elif (self.board_index[self.get_ref_from_index(
                        two_ahead_index)]["type"] != None):
                    return []
            elif color == "b":

                one_ahead_index = int(piece_index) + 8
                two_ahead_index = int(piece_index) + 16

                l_diag = None
                r_diag = None

                if pos[1] != "1":
                    if pos[0 != "a"]:
                        # type: ignore
                        l_diag = int(self.board_index[pos]["index"]) + 7

                    if pos[0 != "h"]:
                        # type: ignore
                        r_diag = int(self.board_index[pos]["index"]) + 9

                l_diag = self.get_ref_from_index(l_diag)
                r_diag = self.get_ref_from_index(r_diag)

                if pos[1] == "7":
                    if (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] == None
                            and self.board_index[self.get_ref_from_index(
                                one_ahead_index)]["type"] == None):
                        possible_moves.append(
                            self.get_ref_from_index(one_ahead_index))
                        possible_moves.append(
                            self.get_ref_from_index(two_ahead_index))
                        return possible_moves
                    elif (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] != None
                          and self.board_index[self.get_ref_from_index(
                              one_ahead_index)]["type"] == None):
                        possible_moves.append(
                            self.get_ref_from_index(one_ahead_index))
                        return possible_moves
                    elif (self.board_index[self.get_ref_from_index(
                            two_ahead_index)]["type"] == None
                          and self.board_index[self.get_ref_from_index(
                              one_ahead_index)]["type"] != None):
                        return []
                if r_diag != None:
                    if (self.board_index[r_diag]["color"] !=
                            self.board_index[pos]["color"]
                            and self.board_index[r_diag]["type"] != None):
                        possible_moves.append(r_diag)

                if l_diag != None:
                    if (self.board_index[l_diag]["color"] !=
                            self.board_index[pos]["color"]
                            and self.board_index[l_diag]["type"] != None):
                        possible_moves.append(l_diag)

                if (self.board_index[self.get_ref_from_index(one_ahead_index)]
                    ["type"] == None):
                    possible_moves.append(
                        self.get_ref_from_index(one_ahead_index))
                elif (self.board_index[self.get_ref_from_index(
                        one_ahead_index)]["type"] != None):
                    return []

        possible_moves = self.clean_moves(pos, possible_moves)  # type: ignore
        return possible_moves

    def safe(self, square):
        attacked_squares = self.legal_moves()
        for i in attacked_squares:
            if square == i:
                return False
        return True

    def legal_moves(self) -> t.List[str]:
        legal_moves = []
        moves = self.calc_board_position_pos_moves(self.fen)
        for move in moves:
            for origin in move:
                legal_moves.append(move[origin])
        return legal_moves

    def is_edge_square(self, square: str) -> bool:
        if (str(square)[0] == "a" or str(square)[0] == "h"
                or str(square)[1] == "8" or str(square)[1] == "1"):
            return True
        else:
            return False

    def legal(self, move: t.Dict[str, str]) -> bool:
        if move in self.calc_board_position_pos_moves(self.fen):
            return True
        return False

    def move(self, origin: str, dest: str) -> None:
        move = {"{origin}".format(origin=origin): "{dest}".format(dest=dest)}
        if self.legal(move):
            self.board_index[dest]["type"] = self.board_index[origin]["type"]
            self.board_index[dest]["color"] = self.board_index[origin]["color"]

            self.board_index[origin]["color"] = None
            self.board_index[origin]["type"] = None

            self.fen = self.create_fen()
        else:
            return

    def create_fen(self) -> str:
        dirty_fen = ""
        clean_fen = ""
        index = 1
        s_index = 0
        for square in self.board_index:
            if self.board_index[square]["type"] == None:
                dirty_fen += "x"
            else:
                dirty_fen += self.board_index[square]["type"]  # type: ignore

            if index == 8:
                dirty_fen += "/"
                index = 1
            else:
                index += 1

        for char in dirty_fen:
            if char == "x":
                s_index += 1
            else:
                if char != "x" and s_index > 0:
                    clean_fen += str(s_index)
                    clean_fen += char
                    s_index = 0
                else:
                    clean_fen += char

        return clean_fen


"""
=======
import re
import math


class Chessboard(object):
    STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self, fen=STARTING_FEN):
        self.board_index = {}
        self.files = "abcdefgh"
        self.fen = fen

        # - Initializing functions
        self.init()

    def init(self):
        # - Keeps track of which square is being worked on :
        square_index = 1
        file_index = 1

        while square_index <= 64:

            # - Data used to define the square
            square_rank = 8 - int(square_index / 8)
            square_file = self.files[file_index - 1]

            if square_index % 8 == 0:
                square_rank += 1

            if square_rank < 1:
                break

            square_ref = "{file}{rank}".format(file=square_file, rank=square_rank)
            self.board_index[square_ref] = {"index": square_index, "color": None, "type": None}

            if file_index % 8 == 0:
                file_index = 1
            else:
                file_index += 1

            square_index += 1

    def get_rank_squares(self, rank):
        squares = []
        for square in self.board_index:
            if str(square)[1] == str(rank):
                squares.append(str(square))
        return squares

    def draw_rank(self, rank):
        result = []
        squares = self.get_rank_squares(rank)
        for square in squares:
            if self.board_index[square]["type"] != None:
                result.append(self.board_index[square]["type"])
            else:
                result.append("-")
        drawing = ""
        for square in result:
            drawing += square
            drawing += "    "
        return drawing

    def draw_ascii(self):
        rank_index = 8
        while rank_index >= 1:
            print("")
            print(
                "{rank}   |   {rank_drawing}".format(rank=rank_index, rank_drawing=self.draw_rank(rank_index))
            )
            print("")
            rank_index -= 1
        print("-" * 44)
        print("")
        print("        a    b    c    d    e    f    g    h".upper())

    def reset_board_position(self):
        self.position(Chessboard.STARTING_FEN)

    def get_ref_from_index(self, index):
        for square in self.board_index:
            if int(self.board_index[str(square)]["index"]) == index:
                return str(square)

    def def_piece_colors(self):
        for square in self.board_index:
            self.board_index[str(square)]["color"] = self.def_square_color(str(square))

    def position(self, fen):
        square_index = 1
        self.fen = fen
        fen = self.parse_fen(fen)

        for char in fen:
            if char == "1":
                self.board_index[self.get_ref_from_index(square_index)]["type"] = None

            elif char == "/":
                square_index = square_index
                square_index -= 1

            elif re.match("[a-zA-Z]+", char):
                self.board_index[self.get_ref_from_index(square_index)]["type"] = char

            square_index += 1

    def parse_fen(self, fen):
        resulting_fen = ""
        for char in fen:
            if re.match("[0-9]+", char):
                resulting_fen += "1" * int(char)
            else:
                resulting_fen += char
        return resulting_fen

    def highlight_moves(self, squares):
        for square in squares:
            if square == None:
                pass
            else:
                if self.board_index[str(square)]["type"] == None:
                    self.board_index[str(square)]["type"] = "*"
                else:
                    self.board_index[str(square)]["type"] += "*"

    def def_square_color(self, square):
        piece = self.board_index[str(square)]["type"]
        if piece == None:
            return None
        if re.match("[a-z]+", str(piece)):
            self.board_index[str(square)]["color"] = "b"
        elif re.match("[A-Z]+", str(piece)):
            self.board_index[str(square)]["color"] = "w"
        return self.board_index[str(square)]["color"]

    def clean_moves(self, origin, moves):
        clean_moves = []
        for move in moves:
            if move == None:
                pass
            else:
                if self.board_index[str(origin)]["color"] == self.board_index[str(move)]["color"]:
                    pass
                else:
                    clean_moves.append(str(move))
        return clean_moves

    def calc_board_position_pos_moves(self, fen):
        moves = []
        chessboard.position(fen)
        for square in self.board_index:
            piece = self.board_index[str(square)]["type"]
            color = self.board_index[str(square)]["color"]
            possible_moves = self.calc_piece_pos_moves(piece, str(square), color)
            for move in possible_moves:
                move_object = {
                    "origin": "{origin}".format(origin=str(square)),
                    "dest": "{dest}".format(dest=str(move)),
                }
                moves.append(move_object)
        return moves

    def calc_piece_pos_moves(self, piece, pos, color):
        possible_moves = []

        # - Calculates moves for a knight (N / n)
        if piece == "n" or piece == "N":
            position_index = int(self.board_index[pos]["index"])

            possible_moves.append(self.get_ref_from_index(position_index - 17))
            possible_moves.append(self.get_ref_from_index(position_index - 15))
            possible_moves.append(self.get_ref_from_index(position_index - 10))
            possible_moves.append(self.get_ref_from_index(position_index - 6))
            possible_moves.append(self.get_ref_from_index(position_index + 6))
            possible_moves.append(self.get_ref_from_index(position_index + 10))
            possible_moves.append(self.get_ref_from_index(position_index + 15))
            possible_moves.append(self.get_ref_from_index(position_index + 17))

            if pos[0] == "a" or pos[0] == "b":
                possible_moves[4] = None
                possible_moves[2] = None
                if pos[0] == "a":
                    possible_moves[0] = None
                    possible_moves[6] = None

            if pos[0] == "g" or pos[0] == "h":
                possible_moves[3] = None
                possible_moves[5] = None
                if pos[0] == "h":
                    possible_moves[1] = None
                    possible_moves[7] = None

            if pos[1] == "7" or pos[1] == "8":
                possible_moves[0] = None
                possible_moves[1] = None
                if pos[1] == "8":
                    possible_moves[2] = None
                    possible_moves[3] = None

            if pos[1] == "1" or pos[1] == "2":
                possible_moves[6] = None
                possible_moves[7] = None
                if pos[1] == "h":
                    possible_moves[4] = None
                    possible_moves[5] = None

        # - Calculates moves for a bishop (B / b)
        if piece == "b" or piece == "B":
            og_pos_index = self.board_index[pos]["index"]

            valid = True
            index = og_pos_index
            curr_square = index - 9
            diag_index = 9

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                else:
                    possible_moves.append(square_ref)
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 9
                    elif directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7

        # - Calculates moves for a rook (R / r)
        if piece == "r" or piece == "R":
            og_pos_index = self.board_index[pos]["index"]

            valid = True
            index = og_pos_index
            curr_square = index - 8

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                else:
                    possible_moves.append(square_ref)
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 8
                    elif directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1

        # - Calculates moves for a queen (Q / q)
        if piece == "q" or piece == "Q":
            og_pos_index = self.board_index[pos]["index"]

            valid = True
            index = og_pos_index
            curr_square = index - 8

            og_color = self.board_index[pos]["color"]

            op_color = None
            if og_color == "w":
                op_color = "b"
            else:
                op_color = "w"

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1
                else:
                    possible_moves.append(square_ref)
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 8
                    elif directions == 1:
                        curr_square = index + 8
                    elif directions == 2:
                        curr_square = index - 1
                    elif directions == 3:
                        curr_square = index + 1

            valid = True
            index = og_pos_index
            curr_square = index - 9

            directions = 0

            while valid:
                if directions == 4:
                    break
                if curr_square < 1 or curr_square > 64:
                    break
                square_ref = str(self.get_ref_from_index(curr_square))
                if self.board_index[square_ref]["color"] == og_color:
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.board_index[square_ref]["color"] == op_color:
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                elif self.is_edge_square(square_ref):
                    possible_moves.append(square_ref)
                    directions += 1
                    index = og_pos_index
                    if directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7
                else:
                    possible_moves.append(square_ref)
                    index = self.board_index[square_ref]["index"]
                    if directions == 0:
                        curr_square = index - 9
                    elif directions == 1:
                        curr_square = index + 9
                    elif directions == 2:
                        curr_square = index - 7
                    elif directions == 3:
                        curr_square = index + 7

        # - Calculates moves for a king (K / k)
        if piece == "k" or piece == "K":
            square_index = int(self.board_index[pos]["index"])

            possible_moves.append(self.get_ref_from_index(square_index - 9))
            possible_moves.append(self.get_ref_from_index(square_index - 8))
            possible_moves.append(self.get_ref_from_index(square_index - 7))
            possible_moves.append(self.get_ref_from_index(square_index - 1))
            possible_moves.append(self.get_ref_from_index(square_index + 1))
            possible_moves.append(self.get_ref_from_index(square_index + 7))
            possible_moves.append(self.get_ref_from_index(square_index + 8))
            possible_moves.append(self.get_ref_from_index(square_index + 9))

            if pos[0] == "a":
                possible_moves[0] = None
                possible_moves[3] = None
                possible_moves[5] = None

            if pos[0] == "h":
                possible_moves[2] = None
                possible_moves[4] = None
                possible_moves[7] = None

            if pos[1] == "1":
                possible_moves[5] = None
                possible_moves[6] = None
                possible_moves[7] = None

            if pos[1] == "8":
                possible_moves[0] = None
                possible_moves[1] = None
                possible_moves[2] = None

            safe_possible_moves = []
            possible_moves = self.clean_moves(pos, possible_moves)

            # 	for move in possible_moves:
            # 		if(self.safe(move)): safe_possible_moves.append(move)

            # 	possible_moves = safe_possible_moves

        # - Calculates moves for a pawn (P / p)
        if piece == "p" or piece == "P":
            piece_index = self.board_index[pos]["index"]

            if color == "w":

                one_ahead_index = int(piece_index) - 8
                two_ahead_index = int(piece_index) - 16

                l_diag = None
                r_diag = None

                if pos[1] != "8":
                    if pos[0 != "a"]:
                        l_diag = int(self.board_index[pos]["index"]) - 9

                    if pos[0 != "h"]:
                        r_diag = int(self.board_index[pos]["index"]) - 7

                l_diag = self.get_ref_from_index(l_diag)
                r_diag = self.get_ref_from_index(r_diag)

                if pos[1] == "2":
                    if (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] == None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None
                    ):
                        possible_moves.append(self.get_ref_from_index(one_ahead_index))
                        possible_moves.append(self.get_ref_from_index(two_ahead_index))
                        return possible_moves
                    elif (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] != None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None
                    ):
                        possible_moves.append(self.get_ref_from_index(one_ahead_index))
                        return possible_moves
                    elif (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] == None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] != None
                    ):
                        return []
                if r_diag != None:
                    if (
                        self.board_index[r_diag]["color"] != self.board_index[pos]["color"]
                        and self.board_index[r_diag]["type"] != None
                    ):
                        possible_moves.append(r_diag)

                if l_diag != None:
                    if (
                        self.board_index[l_diag]["color"] != self.board_index[pos]["color"]
                        and self.board_index[l_diag]["type"] != None
                    ):
                        possible_moves.append(l_diag)

                if self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None:
                    possible_moves.append(self.get_ref_from_index(one_ahead_index))
                elif self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] != None:
                    return []
            elif color == "b":

                one_ahead_index = int(piece_index) + 8
                two_ahead_index = int(piece_index) + 16

                l_diag = None
                r_diag = None

                if pos[1] != "1":
                    if pos[0 != "a"]:
                        l_diag = int(self.board_index[pos]["index"]) + 7

                    if pos[0 != "h"]:
                        r_diag = int(self.board_index[pos]["index"]) + 9

                l_diag = self.get_ref_from_index(l_diag)
                r_diag = self.get_ref_from_index(r_diag)

                if pos[1] == "7":
                    if (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] == None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None
                    ):
                        possible_moves.append(self.get_ref_from_index(one_ahead_index))
                        possible_moves.append(self.get_ref_from_index(two_ahead_index))
                        return possible_moves
                    elif (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] != None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None
                    ):
                        possible_moves.append(self.get_ref_from_index(one_ahead_index))
                        return possible_moves
                    elif (
                        self.board_index[self.get_ref_from_index(two_ahead_index)]["type"] == None
                        and self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] != None
                    ):
                        return []
                if r_diag != None:
                    if (
                        self.board_index[r_diag]["color"] != self.board_index[pos]["color"]
                        and self.board_index[r_diag]["type"] != None
                    ):
                        possible_moves.append(r_diag)

                if l_diag != None:
                    if (
                        self.board_index[l_diag]["color"] != self.board_index[pos]["color"]
                        and self.board_index[l_diag]["type"] != None
                    ):
                        possible_moves.append(l_diag)

                if self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] == None:
                    possible_moves.append(self.get_ref_from_index(one_ahead_index))
                elif self.board_index[self.get_ref_from_index(one_ahead_index)]["type"] != None:
                    return []

        possible_moves = self.clean_moves(pos, possible_moves)
        return possible_moves

    def safe(self, square):
        attacked_squares = self.legal_moves()
        for i in attacked_squares:
            if square == i:
                return False
        return True

    def legal_moves(self):
        legal_moves = []
        moves = self.calc_board_position_pos_moves(self.fen)
        for move in moves:
            for origin in move:
                legal_moves.append(move[origin])
        return legal_moves

    def is_edge_square(self, square):
        if str(square)[0] == "a" or str(square)[0] == "h" or str(square)[1] == "8" or str(square)[1] == "1":
            return True
        else:
            return False

    def legal(self, move):
        if move in self.calc_board_position_pos_moves(board.fen):
            return True
        return False

    def move(self, origin, dest):
        move = {"{origin}".format(origin=origin): "{dest}".format(dest=dest)}
        if self.legal(move):
            self.board_index[dest]["type"] = self.board_index[origin]["type"]
            self.board_index[dest]["color"] = self.board_index[origin]["color"]

            self.board_index[origin]["color"] = None
            self.board_index[origin]["type"] = None

            self.fen = self.create_fen()
        else:
            return

    def create_fen(self):
        dirty_fen = ""
        clean_fen = ""
        index = 1
        s_index = 0
        for square in self.board_index:
            if self.board_index[square]["type"] == None:
                dirty_fen += "x"
            else:
                dirty_fen += self.board_index[square]["type"]

            if index == 8:
                dirty_fen += "/"
                index = 1
            else:
                index += 1

        for char in dirty_fen:
            if char == "x":
                s_index += 1
            else:
                if char != "x" and s_index > 0:
                    clean_fen += str(s_index)
                    clean_fen += char
                    s_index = 0
                else:
                    clean_fen += char

        return clean_fen
"""
