import skaak
import chess
import sys


def convert(move):
    fr = (move.from_square // 8) + 1
    ff = "abcdefgh"[move.from_square % 8]
    tr = (move.to_square // 8) + 1
    tf = "abcdefgh"[move.to_square % 8]
    return f"{ff}{fr}{tf}{tr}"


def main():
    with open('./tests/FEN/endgames.txt') as fen_file:
        # for fen in fen_file.readlines():
        for fen in ["8/5pkp/1n4p1/1P6/3K2P1/2N4P/8/8 w - - 0 70"]:
            s_board = skaak.Chessboard(fen)
            c_board = chess.Board(fen)

            # print(s_board)
            # print(c_board)

            s_moves = s_board.legal_moves
            c_moves = c_board.legal_moves

            s_moves = [str(move) for move in s_moves]
            c_moves = [move.uci() for move in c_moves]

            # print(sorted(s_moves))
            # print(sorted(c_moves))

            if len(c_moves) != len(s_moves):
                print(fen)
                print(s_board)
                print(sorted(s_moves))
                print(c_board)
                print(sorted(c_moves))
                print(len(c_moves), len(s_moves))

                missing_moves = [
                    move for move in c_moves if move not in s_moves]
                false_moves = [move for move in s_moves if move not in c_moves]

                print("\nMissing Moves:")
                for move in missing_moves:
                    print(move)

                print("\nFalse Moves:")
                for move in false_moves:
                    print(move)

                print(s_board.generate_fen())


if __name__ == "__main__":
    # main()
    #
    for i in range(1, 6):
        x = skaak.Chessboard()
        print(x.perft(i))
#
