#include <iostream>
#include <vector>

using namespace std;

typedef struct MoveList {
    int moves[128];
    int index;
};

class Board {
public:
    MoveList generate_moves(std::string fen);
};

MoveList Board::generate_moves(std::string fen) {
    MoveList Moves;
    return Moves;
}

extern "C" {
    Board* Board_New() {
        return new Board();
    }

    MoveList board_gen_moves(Board* board, std::string fen) {
        return board->generate_moves(fen);
    }
}
