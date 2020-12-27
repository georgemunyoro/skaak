from skaak import chess


def test_convert_x88_board_ref_to_san():
    assert chess.convert_x88_board_ref_to_san(100) == "e2"
    assert chess.convert_x88_board_ref_to_san(113) == "b1"
    assert chess.convert_x88_board_ref_to_san(119) == "h1"
    assert chess.convert_x88_board_ref_to_san(18)  == "c7"
    assert chess.convert_x88_board_ref_to_san(22)  == "g7"
    assert chess.convert_x88_board_ref_to_san(7)   == "h8"
    assert chess.convert_x88_board_ref_to_san(0)   == "a8"
    assert chess.convert_x88_board_ref_to_san(71)  == "h4"
    assert chess.convert_x88_board_ref_to_san(86)  == "g3"
    assert chess.convert_x88_board_ref_to_san(98)  == "c2"
