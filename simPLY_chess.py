
import sys
from itertools import count

NAME: str = "simPLY_chess"
AUTHOR: str = "andrewharabor"
VERSION: str = "v0.1.0 2023"

##################################
# CONSTANTS AND GLOBAL VARIABLES #
##################################

# Corner squares
A1: int = 91
H1: int = 98
A8: int = 21
H8: int = 28

# Cardinal directions
NORTH: int = -10
EAST: int = 1
SOUTH: int = 10
WEST: int = -1

# Directions for each piece type
PIECE_DIRECTIONS: dict[str, list[int]] = {
    "P": [NORTH, NORTH + NORTH, NORTH + WEST, NORTH + EAST],
    "N": [NORTH + NORTH + EAST, NORTH + NORTH + WEST, EAST + EAST + NORTH, EAST + EAST + SOUTH, SOUTH + SOUTH + EAST, SOUTH + SOUTH + WEST, WEST + WEST + SOUTH, WEST + WEST + NORTH],
    "B": [NORTH + EAST, SOUTH + EAST, SOUTH + WEST, NORTH + WEST],
    "R": [NORTH, EAST, SOUTH, WEST],
    "Q": [NORTH, EAST, SOUTH, WEST, NORTH + EAST, SOUTH + EAST, SOUTH + WEST, NORTH + WEST],
    "K": [NORTH, EAST, SOUTH, WEST, NORTH + EAST, SOUTH + EAST, SOUTH + WEST, NORTH + WEST]
}

# Initial board setup
# 10 x 12 board for easy detection of moves that go off the edge of the board
# Note that here and everywhere else, uppercase letters are used for the current player's pieces and will not necessarily mean white pieces
INITIAL_POSITION: str = (
    "         \n"  # 0 - 9
    "         \n"  # 10 - 19
    " rnbqkbnr\n"  # 20 - 29
    " pppppppp\n"  # 30 - 39
    " ........\n"  # 40 - 49
    " ........\n"  # 50 - 59
    " ........\n"  # 60 - 69
    " ........\n"  # 70 - 79
    " PPPPPPPP\n"  # 80 - 89
    " RNBQKBNR\n"  # 90 - 99
    "         \n"  # 100 - 109
    "         \n"  # 110 - 119
)
INITIAL_CASTLING: list[bool] = [False, False]  # [queenside, kingside]
INITIAL_OPPONENT_CASTLING: list[bool] = [False, False]  # [queenside, kingside]
INITIAL_EN_PASSANT: int = 0  # square where en passant is possible for us
INITIAL_KING_PASSANT: int = 0  # square the king "passes through" when castling (the square the rook is moved to), used to detect castling through check
INITIAL_COLOR: str = "w"  # the current player's color

# Initialize current board setup
global position, castling, opponent_castling, en_passant, king_passant, color
position: str = INITIAL_POSITION
castling: list[bool] = INITIAL_CASTLING[:]
opponent_castling: list[bool] = INITIAL_OPPONENT_CASTLING[:]
en_passant: int = INITIAL_EN_PASSANT
king_passant: int = INITIAL_KING_PASSANT
color: str = INITIAL_COLOR

# Transposition table, used to store previously calculated positions and keep track of the best move
TRANSPOSITION_TABLE: dict[str, tuple[int, int, str, str]] = {}

# Piece values and piece square tables for the middlegame and endgame
# Used to evaluate the position in terms of material and piece placement
MIDGAME_PAWN_VALUE: int = 100
MIDGAME_KNIGHT_VALUE: int = 411
MIDGAME_BISHOP_VALUE: int = 445
MIDGAME_ROOK_VALUE: int = 582
MIDGAME_QUEEN_VALUE: int = 1250
MIDGAME_KING_VALUE: int = 60000

MIDGAME_PIECE_VALUES: dict[str, int] = {
    "": 0,
    "P": MIDGAME_PAWN_VALUE,
    "N": MIDGAME_KNIGHT_VALUE,
    "B": MIDGAME_BISHOP_VALUE,
    "R": MIDGAME_ROOK_VALUE,
    "Q": MIDGAME_QUEEN_VALUE,
    "K": MIDGAME_KING_VALUE
}

MIDGAME_PAWN_TABLE: list[int] = [
    1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250,
     120,  163,   74,  116,   83,  154,   41,  -13,
      -7,    9,   32,   38,   79,   68,   30,  -24,
     -17,   16,    7,   26,   28,   15,   21,  -28,
     -33,   -2,   -6,   20,   26,    7,   12,  -30,
     -32,   -5,   -5,  -12,    4,    4,   40,  -15,
     -43,   -1,  -24,  -23,  -33,   29,   46,  -27,
       0,    0,    0,    0,    0,    0,    0,    0,
]

MIDGAME_KNIGHT_TABLE: list[int] = [
    -204, -109,  -41,  -60,   74, -118,  -18, -130,
     -89,  -50,   88,   44,   28,   76,    9,  -21,
     -57,   73,   45,   79,  102,  157,   89,   54,
     -11,   21,   23,   65,   45,   84,   22,   27,
     -16,    5,   20,   16,   34,   23,   26,  -10,
     -28,  -11,   15,   12,   23,   21,   30,  -20,
     -35,  -65,  -15,   -4,   -1,   22,  -17,  -23,
    -128,  -26,  -71,  -40,  -21,  -34,  -23,  -28,
]

MIDGAME_BISHOP_TABLE: list[int] = [
     -35,    5, -100,  -45,  -30,  -51,    9,  -10,
     -32,   20,  -22,  -16,   37,   72,   22,  -57,
     -20,   45,   52,   49,   43,   61,   45,   -2,
      -5,    6,   23,   61,   45,   45,    9,   -2,
      -7,   16,   16,   32,   41,   15,   12,    5,
       0,   18,   18,   18,   17,   33,   22,   12,
       5,   18,   20,    0,    9,   26,   40,    1,
     -40,   -4,  -17,  -26,  -16,  -15,  -48,  -26,
]

MIDGAME_ROOK_TABLE: list[int] = [
      39,   51,   39,   62,   77,   11,   38,   52,
      33,   39,   71,   76,   98,   82,   32,   54,
      -6,   23,   32,   44,   21,   55,   74,   20,
     -29,  -13,    9,   32,   29,   43,  -10,  -24,
     -44,  -32,  -15,   -1,   11,   -9,    7,  -28,
     -55,  -30,  -20,  -21,    4,    0,   -6,  -40,
     -54,  -20,  -24,  -11,   -1,   13,   -7,  -87,
     -23,  -16,    1,   21,   20,    9,  -45,  -32,
]

MIDGAME_QUEEN_TABLE: list[int] = [
     -34,    0,   35,   15,   72,   54,   52,   55,
     -29,  -48,   -6,    1,  -20,   70,   34,   66,
     -16,  -21,    9,   10,   35,   68,   57,   70,
     -33,  -33,  -20,  -20,   -1,   21,   -2,    1,
     -11,  -32,  -11,  -12,   -2,   -5,    4,   -4,
     -17,    2,  -13,   -2,   -6,    2,   17,    6,
     -43,  -10,   13,    2,   10,   18,   -4,    1,
      -1,  -22,  -11,   12,  -18,  -30,  -38,  -61,
]

MIDGAME_KING_TABLE: list[int] = [
     -79,   28,   20,  -18,  -68,  -41,    2,   16,
      35,   -1,  -24,   -9,  -10,   -5,  -46,  -35,
     -11,   29,    2,  -20,  -24,    7,   27,  -27,
     -21,  -24,  -15,  -33,  -37,  -30,  -17,  -44,
     -60,   -1,  -33,  -48,  -56,  -54,  -40,  -62,
     -17,  -17,  -27,  -56,  -54,  -37,  -18,  -33,
       1,    9,  -10,  -78,  -52,  -20,   11,   10,
     -18,   44,   15,  -66,   10,  -34,   29,   17,
]

MIDGAME_PIECE_SQUARE_TABLES: dict[str, list[int]] = {
    "P": MIDGAME_PAWN_TABLE,
    "N": MIDGAME_KNIGHT_TABLE,
    "B": MIDGAME_BISHOP_TABLE,
    "R": MIDGAME_ROOK_TABLE,
    "Q": MIDGAME_QUEEN_TABLE,
    "K": MIDGAME_KING_TABLE,
}

# Pad the midgame tables with zeros to make them 10x12
for piece in "PNBRQK":
    new_table: list[int] = []
    blank_row: list[int] = [0] * 10
    new_table += blank_row + blank_row
    for row in range(0, 64, 8):
        new_table += [0] + MIDGAME_PIECE_SQUARE_TABLES[piece][row:row + 8] + [0]
    new_table += blank_row + blank_row
    MIDGAME_PIECE_SQUARE_TABLES[piece] = new_table

ENDGAME_PAWN_VALUE: int = 115
ENDGAME_KNIGHT_VALUE: int = 343
ENDGAME_BISHOP_VALUE: int = 362
ENDGAME_ROOK_VALUE: int = 624
ENDGAME_QUEEN_VALUE: int = 1141
ENDGMAE_KING_VALUE: int = 60000

ENDGAME_PIECE_VALUES: dict[str, int] = {
    "": 0,
    "P": ENDGAME_PAWN_VALUE,
    "N": ENDGAME_KNIGHT_VALUE,
    "B": ENDGAME_BISHOP_VALUE,
    "R": ENDGAME_ROOK_VALUE,
    "Q": ENDGAME_QUEEN_VALUE,
    "K": ENDGMAE_KING_VALUE,
}

ENDGAME_PAWN_TABLE: list[int] = [
    1141, 1141, 1141, 1141, 1141, 1141, 1141, 1141,
     217,  211,  193,  163,  179,  161,  201,  228,
     115,  122,  104,   82,   68,   65,  100,  102,
      39,   29,   16,    6,   -2,    5,   21,   21,
      16,   11,   -4,   -9,   -9,  -10,    4,   -1,
       5,    9,   -7,    1,    0,   -6,   -1,  -10,
      16,   10,   10,   12,   16,    0,    2,   -9,
       0,    0,    0,    0,    0,    0,    0,    0,
]

ENDGAME_KNIGHT_TABLE: list[int] = [
     -71,  -46,  -16,  -34,  -38,  -33,  -77, -121,
     -30,  -10,  -30,   -2,  -11,  -30,  -29,  -63,
     -29,  -24,   12,   11,   -1,  -11,  -23,  -50,
     -21,    4,   27,   27,   27,   13,   10,  -22,
     -22,   -7,   20,   30,   20,   21,    5,  -22,
     -28,   -4,   -1,   18,   12,   -4,  -24,  -27,
     -51,  -24,  -12,   -6,   -2,  -24,  -28,  -54,
     -35,  -62,  -28,  -18,  -27,  -22,  -61,  -78,
]

ENDGAME_BISHOP_TABLE: list[int] = [
     -17,  -26,  -13,  -10,   -9,  -11,  -21,  -29,
     -10,   -5,    9,  -15,   -4,  -16,   -5,  -17,
       2,  -10,    0,   -1,   -2,    7,    0,    5,
      -4,   11,   15,   11,   17,   12,    4,    2,
      -7,    4,   16,   23,    9,   12,   -4,  -11,
     -15,   -4,   10,   12,   16,    4,   -9,  -18,
     -17,  -22,   -9,   -1,    5,  -11,  -18,  -33,
     -28,  -11,  -28,   -6,  -11,  -20,   -6,  -21,
]

ENDGAME_ROOK_TABLE: list[int] = [
      16,   12,   22,   18,   15,   15,   10,    6,
      13,   16,   16,   13,   -4,    4,   10,    4,
       9,    9,    9,    6,    5,   -4,   -6,   -4,
       5,    4,   16,    1,    2,    1,   -1,    2,
       4,    6,   10,    5,   -6,   -7,  -10,  -13,
      -5,    0,   -6,   -1,   -9,  -15,  -10,  -20,
      -7,   -7,    0,    2,  -11,  -11,  -13,   -4,
     -11,    2,    4,   -1,   -6,  -16,    5,  -24,
]

ENDGAME_QUEEN_TABLE: list[int] = [
     -11,   27,   27,   33,   33,   23,   12,   24,
     -21,   24,   39,   50,   71,   30,   37,    0,
     -24,    7,   11,   60,   57,   43,   23,   11,
       4,   27,   29,   55,   70,   49,   70,   44,
     -22,   34,   23,   57,   38,   41,   48,   28,
     -20,  -33,   18,    7,   11,   21,   12,    6,
     -27,  -28,  -37,  -20,  -20,  -28,  -44,  -39,
     -40,  -34,  -27,  -52,   -6,  -39,  -24,  -50,
]

ENDGAME_KING_TABLE: list[int] = [
     -90,  -43,  -22,  -22,  -13,   18,    5,  -21,
     -15,   21,   17,   21,   21,   46,   28,   13,
      12,   21,   28,   18,   24,   55,   54,   16,
     -10,   27,   29,   33,   32,   40,   32,    4,
     -22,   -5,   26,   29,   33,   28,   11,  -13,
     -23,   -4,   13,   26,   28,   20,    9,  -11,
     -33,  -13,    5,   16,   17,    5,   -6,  -21,
     -65,  -41,  -26,  -13,  -34,  -17,  -29,  -52,
]

ENDGAME_PIECE_SQUARE_TABLES: dict[str, list[int]] = {
    "P": ENDGAME_PAWN_TABLE,
    "N": ENDGAME_KNIGHT_TABLE,
    "B": ENDGAME_BISHOP_TABLE,
    "R": ENDGAME_ROOK_TABLE,
    "Q": ENDGAME_QUEEN_TABLE,
    "K": ENDGAME_KING_TABLE,
}

# Pad the endgame tables with zeros to make them 10x12
for piece in "PNBRQK":
    blank_row: list[int] = [0] * 10
    new_table: list[int] = []
    new_table += blank_row + blank_row
    for row in range(0, 64, 8):
        new_table += [0] + ENDGAME_PIECE_SQUARE_TABLES[piece][row:row + 8] + [0]
    new_table += blank_row + blank_row
    ENDGAME_PIECE_SQUARE_TABLES[piece] = new_table

# Checkmate scores
CHECKMATE_UPPER: int = MIDGAME_KING_VALUE + 10 * MIDGAME_QUEEN_VALUE
CHECKMATE_LOWER: int = MIDGAME_KING_VALUE - 10 * MIDGAME_QUEEN_VALUE

# Game phase constants (used to interpolate between midgame and endgame evaluations)
PAWN_PHASE: int = 0
KNIGHT_PHASE: int = 1
BISHOP_PHASE: int = 1
ROOK_PHASE: int = 2
QUEEN_PHASE: int = 4
TOTAL_PHASE: int = 16 * PAWN_PHASE + 4 * KNIGHT_PHASE + 4 * BISHOP_PHASE + 4 * ROOK_PHASE + 2 * QUEEN_PHASE


###############
# BOARD LOGIC #
###############

def generate_moves(position: str, castling: list[bool], en_passant: int) -> list[tuple[int, int, str, str]]:
    """Generates all pseudo-legal moves for a given position. Returns as a list:
    [start_square, end_square, piece_captured, promotion_piece]."""
    move_list: list[tuple[int, int, str, str]] = []
    for start_square in range(len(position)):
        if position[start_square].isupper():  # piece is current player's
            piece_moved: str = position[start_square]
            for direction in PIECE_DIRECTIONS[piece_moved]:
                for end_square in count(start_square + direction, direction):
                    piece_captured: str = position[end_square]
                    if piece_captured.isspace() or piece_captured.isupper():  # off the board or ally piece
                        break
                    if piece_moved == "P":
                        if direction in [NORTH, NORTH + NORTH] and piece_captured != ".":  # pawn push onto occupied square
                            break
                        if direction == NORTH + NORTH and (start_square < A1 + NORTH or position[start_square + NORTH] != "."):  # double pawn push from invalid rank
                            break
                        if direction in [NORTH + WEST, NORTH + EAST] and piece_captured == "." and end_square + SOUTH != en_passant:  # invalid en passant capture
                            break
                        if A8 <= end_square <= H8:  # pawn promotion
                            for promotion_piece in "QRBN":
                                move_list.append((start_square, end_square, piece_captured, promotion_piece))
                            break
                    move_list.append((start_square, end_square, piece_captured, ""))
                    if piece_moved in "PNK" or piece_captured.islower():  # non-sliding piece or capture
                        break
                    if start_square == A1 and position[end_square + EAST] == "K" and castling[0]:  # the piece is a rook on a1, and the king is on e1 with empty squares in between, and queenside castling is allowed
                        move_list.append((end_square + EAST, end_square + WEST, piece_captured, ""))
                    if  start_square == H1 and position[end_square + WEST] == "K" and castling[1]:  # the piece is a rook on h1, and the king is on e1 with empty squares in between, and kingside castling is allowed
                        move_list.append((end_square + WEST, end_square + EAST, piece_captured, ""))

    return move_list


def make_move(move: tuple[int, int, str, str], position: str, castling: list[bool], opponent_castling: list[bool], en_passant: int, king_passant: int) -> tuple[str, list[bool], list[bool], int, int]:
    """Makes a move on the given position."""
    list_position: list[str] = list(position)
    start_square: int = move[0]
    end_square: int = move[1]
    promotion_piece: str = move[3]
    piece_moved: str = list_position[start_square]
    king_passant = 0
    en_passant = 0
    if start_square == A1:  # queenside rook moved
        castling[0] = False
    if start_square == H1:  # kingside rook moved
        castling[1] = False
    if end_square == A8:  # opponent queenside rook captured
        opponent_castling[0] = False
    if end_square == H8:  # opponent kingside rook captured
        opponent_castling[1] = False
    if piece_moved == "K":
        king_passant = 0
        castling[0] = False
        castling[1] = False
        if start_square - end_square == 2:  # queenside castling
            king_passant = (start_square + end_square) // 2
            list_position[A1], list_position[king_passant] = list_position[king_passant], list_position[A1]
        if end_square - start_square == 2:  # kingside castling
            king_passant = (start_square + end_square) // 2
            list_position[H1], list_position[king_passant] = list_position[king_passant], list_position[H1]
    elif piece_moved == "P":
        if end_square + SOUTH == en_passant:  # en passant capture
            list_position[end_square + SOUTH] = "."
        if A8 <= end_square <= H8:  # pawn promotion
            list_position[end_square] = promotion_piece
        if end_square - start_square == NORTH + NORTH:  # double pawn push
            en_passant = end_square + SOUTH
    list_position[start_square] = "."
    list_position[end_square] = piece_moved
    position = "".join(list_position)
    return position, castling, opponent_castling, en_passant, king_passant


def rotate_position(position: str, castling: list[bool], opponent_castling: list[bool], en_passant: int, king_passant: int) -> tuple[str, list[bool], list[bool], int, int]:
    """Rotates the board 180 degrees and swaps the case of the pieces so that it is from the opponent's point of view.
    Typically called after make_move() since our engine always looks from the current player's point of view."""
    en_passant = 119 - en_passant
    king_passant = 119 - king_passant
    castling, opponent_castling = opponent_castling, castling
    list_position: list[str] = list(position)
    for i in range(60):  # only need to loop through half the board since we're swapping two squares at a time
        if not list_position[i].isspace():
            list_position[119 - i], list_position[i] = list_position[i].swapcase(), list_position[119 - i].swapcase()
    position = "".join(list_position)
    return position, castling, opponent_castling, en_passant, king_passant


def king_in_check(position: str, king_passant: int) -> bool:
    """Finds if the opponent's king is in check or if they were in check before castling. Typically called after
    make_move() and rotate_position() to see if the move was legal."""
    king_position: int = position.find("k") if "k" in position else 0  # after rotating the board, our king "becomes the opponent's king" ("k") in that position
    if king_position == 0:
        return True

    # Since we call find_check() after make_move(), we check to see if the move we just made was castling.
    # If it was, we use the king passant square and the original king position to see if they were attacked.
    # If they were, it means that the castling move was illegal.
    castled: bool = False
    original_king_position: int = 0
    if king_passant in [23, 25]:
        original_king_position = 24
        castled = True
    elif king_passant in [24, 26]:
        original_king_position = 25
        castled = True
    move_list: list[tuple[int, int, str, str]] = generate_moves(position, castling, 0)
    for move in move_list:
        if move[1] == king_position or move[1] == king_passant:
            return True

        if castled and move[1] == original_king_position:
            return True

    return False


########################
# EVALUATION FUNCTIONS #
########################

def game_phase(position: str) -> int:
    """Evaluates the current game phase though piece counts."""
    phase: int = TOTAL_PHASE
    phase -= (position.count("P") + position.count("p")) * PAWN_PHASE
    phase -= (position.count("N") + position.count("n")) * KNIGHT_PHASE
    phase -= (position.count("B") + position.count("b")) * BISHOP_PHASE
    phase -= (position.count("R") + position.count("r")) * ROOK_PHASE
    phase -= (position.count("Q") + position.count("q")) * QUEEN_PHASE
    return (phase * 256 + (TOTAL_PHASE // 2)) // TOTAL_PHASE


def interpolate_evaluations(midgame_score: int, endgame_score: int, phase: int) -> int:
    """Uses the game phase to interpolate between the midgame and endgame scores."""
    return ((midgame_score * (256 - phase)) + (endgame_score * phase)) // 256


def evaluate_position_midgame(position: str) -> int:
    """Evaluates the given position for the side-to-move using the midgame piece values and piece-square tables."""
    score: int = 0
    for square, piece in enumerate(position):
        if piece.isupper():  # ally piece
            score += MIDGAME_PIECE_VALUES[piece] + MIDGAME_PIECE_SQUARE_TABLES[piece][square]
        elif piece.islower():  # opponent piece
            score -= MIDGAME_PIECE_VALUES[piece.upper()] + MIDGAME_PIECE_SQUARE_TABLES[piece.upper()][119 - square]
    return score


def evaluate_position_endgame(position: str) -> int:
    """Evaluates the given position for the side-to-move using the endgame piece values and piece-square tables."""
    score: int = 0
    for square, piece in enumerate(position):
        if piece.isupper():  # ally piece
            score += ENDGAME_PIECE_VALUES[piece] + ENDGAME_PIECE_SQUARE_TABLES[piece][square]
        elif piece.islower():  # opponent piece
            score -= ENDGAME_PIECE_VALUES[piece.upper()] + ENDGAME_PIECE_SQUARE_TABLES[piece.upper()][119 - square]
    return score


def evaluate_position(position: str) -> int:
    """Evaluates the given position for the side-to-move by interpolating between the midgame and endgame evaluations."""
    midgame_score: int = evaluate_position_midgame(position)
    endgame_score: int = evaluate_position_endgame(position)
    phase: int = game_phase(position)
    return interpolate_evaluations(midgame_score, endgame_score, phase)


def evaluate_move(move: tuple[int, int, str, str], position: str, en_passant: int) -> int:
    """Evaluates the given move for the side-to-move and returns a score."""
    phase: int = game_phase(position)
    start_square: int = move[0]
    end_square: int = move[1]
    piece_moved: str = position[start_square]
    piece_captured: str = move[2]
    promotion_piece: str = move[3]
    midgame_move_score: int = MIDGAME_PIECE_SQUARE_TABLES[piece_moved][end_square] - MIDGAME_PIECE_SQUARE_TABLES[piece_moved][start_square]
    endgame_move_score: int = ENDGAME_PIECE_SQUARE_TABLES[piece_moved][end_square] - ENDGAME_PIECE_SQUARE_TABLES[piece_moved][start_square]
    score: int = interpolate_evaluations(midgame_move_score, endgame_move_score, phase)
    if piece_captured.islower():  # capture
        midgame_capture_score: int = MIDGAME_PIECE_VALUES[piece_captured.upper()] + MIDGAME_PIECE_SQUARE_TABLES[piece_captured.upper()][119 - end_square]
        endgame_capture_score: int = ENDGAME_PIECE_VALUES[piece_captured.upper()] + ENDGAME_PIECE_SQUARE_TABLES[piece_captured.upper()][119 - end_square]
        score += interpolate_evaluations(midgame_capture_score, endgame_capture_score, phase)
    if piece_moved == "K" and abs(start_square - end_square) == 2:  # castling
        midgame_castle_score: int = MIDGAME_PIECE_SQUARE_TABLES["R"][(start_square + end_square) // 2] - MIDGAME_PIECE_SQUARE_TABLES["R"][A1 if end_square < start_square else H1]
        endgame_castle_score: int = ENDGAME_PIECE_SQUARE_TABLES["R"][(start_square + end_square) // 2] - ENDGAME_PIECE_SQUARE_TABLES["R"][A1 if end_square < start_square else H1]
        score += interpolate_evaluations(midgame_castle_score, endgame_castle_score, phase)
    if piece_moved == "P":
        if A8 <= end_square <= H8:  # pawn promotion
            midgame_promotion_score: int = MIDGAME_PIECE_SQUARE_TABLES[promotion_piece][end_square] - MIDGAME_PIECE_SQUARE_TABLES["P"][end_square] + MIDGAME_PIECE_VALUES[promotion_piece] - MIDGAME_PIECE_VALUES["P"]
            endgame_promotion_score: int = ENDGAME_PIECE_SQUARE_TABLES[promotion_piece][end_square] - ENDGAME_PIECE_SQUARE_TABLES["P"][end_square] + ENDGAME_PIECE_VALUES[promotion_piece] - ENDGAME_PIECE_VALUES["P"]
            score += interpolate_evaluations(midgame_promotion_score, endgame_promotion_score, phase)
        if end_square + SOUTH == en_passant:
            midgame_en_passant_score: int = MIDGAME_PIECE_SQUARE_TABLES["P"][119 - (end_square + SOUTH)]
            endgame_en_passant_score: int = ENDGAME_PIECE_SQUARE_TABLES["P"][119 - (end_square + SOUTH)]
            score += interpolate_evaluations(midgame_en_passant_score, endgame_en_passant_score, phase)
    return score


################
# SEARCH LOGIC #
################


def quiescent_search(depth: int, alpha: int, beta: int, position: str, castling: list[bool], opponent_castling: list[bool], en_passant: int, king_passant: int) -> int:
    """Performs a quiescent search (searches captures only until a quiet position or max depth is reached) with delta
    pruning on the given position and returns the score found after the search."""
    stand_pat: int = evaluate_position(position)
    if depth == 0:  # while using quiescent search with depth reduces its effectiveness, the search takes too long otherwise
        return stand_pat

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat
    move_list: list[tuple[int, int, str, str]] = generate_moves(position, castling[:], en_passant)
    move_list.sort(key=lambda move: evaluate_move(move, position, en_passant), reverse=True)
    for move in move_list:
        if move[2].islower():  # capture
            new_position: tuple[str, list[bool], list[bool], int, int] = make_move(move, position, castling[:], opponent_castling[:], en_passant, king_passant)
            new_position = rotate_position(*new_position)
            if not king_in_check(new_position[0], new_position[4]): # if the move doesn't result in our king being in check (legal move)
                delta: int = 200
                if stand_pat + ENDGAME_PIECE_VALUES[move[2].upper()] + ENDGAME_PIECE_VALUES[move[3]] + delta > alpha:  # delta pruning
                    score: int = -quiescent_search(depth - 1, -beta, -alpha, *new_position)
                    if score >= beta:
                        return beta

                    if score > alpha:
                        alpha = score
    return alpha


def nega_max_search(depth: int, alpha: int, beta: int, position: str, castling: list[bool], opponent_castling: list[bool], en_passant: int, king_passant: int) -> int:
    """Performs a negamax search with alpha-beta pruning on the given position and returns the score of the best
    possible move for the side-to-move."""
    global root_call_move_list, root_call_depth
    if depth == 0:
        return quiescent_search(root_call_depth * 4, alpha, beta, position, castling[:], opponent_castling[:], en_passant, king_passant)

    killer_move: tuple[int, int, str, str] | None = TRANSPOSITION_TABLE.get(str(position))  # get move if we already searched this position
    if (depth != root_call_depth) and (killer_move is not None):  # using killer move at root depth defeats the purpose of iterative deepening
        return evaluate_position(position)

    else:
        moves: list[tuple[int, tuple[int, int, str, str]]] = []  # list of tuples containing the score and move
        if depth == root_call_depth:
            move_list: list[tuple[int, int, str, str]] = root_call_move_list  # use the sorted move list from the root call
        else:
            move_list: list[tuple[int, int, str, str]] = generate_moves(position, castling[:], en_passant)
            move_list.sort(key=lambda move: evaluate_move(move, position, en_passant), reverse=True)
        best_move: tuple[int, int, str, str] = (0, 0, "", "")
        for move in move_list:
            new_position: tuple[str, list[bool], list[bool], int, int] = make_move(move, position, castling[:], opponent_castling[:], en_passant, king_passant)
            new_position = rotate_position(*new_position)
            if not king_in_check(new_position[0], new_position[4]):  # if the move doesn't result in our king being in check (legal move)
                score: int = -nega_max_search(depth - 1, -beta, -alpha, *new_position)
                moves.append((score, move))
                if score >= beta:
                    return beta  # fail-hard beta cutoff

                if score > alpha:
                    alpha = score
                    best_move = move
        if len(moves) == 0:  # if there are no legal moves, it's either checkmate or stalemate.
            if depth == root_call_depth:
                root_call_move_list = []
            new_position = rotate_position(position, castling[:], opponent_castling[:], en_passant, king_passant)
            if king_in_check(new_position[0], 0):
                return -CHECKMATE_LOWER - depth

            else:
                return 0

        else:
            if depth == root_call_depth:  # only sort moves at the root
                moves.sort(key=lambda pair: pair[0], reverse=True)
                root_call_move_list = [pair[1] for pair in moves]
            if depth > 1 and best_move != (0, 0, "", ""):  # if depth is higher, this could be increased for a more accurate transposition table
                TRANSPOSITION_TABLE[str(position)] = best_move
            return alpha


root_call_move_list: list[tuple[int, int, str, str]]
root_call_depth: int

def search_position(depth: int, position: str, castling: list[bool], opponent_castling: list[bool], en_passant: int, king_passant: int) -> tuple[int, int, str, str]:
    """Searches the given position and returns the best move found. Acts as root call for negamax search with
    alpha-beta pruning with quiescent search with delta pruning within an iterative deepening framework that utilizes
    aspiration windows."""
    global root_call_move_list, root_call_depth
    root_call_move_list = generate_moves(position, castling[:], en_passant)
    root_call_move_list.sort(key=lambda move: evaluate_move(move, position, en_passant), reverse=True)
    root_call_depth = 1
    root_call_alpha: int = -CHECKMATE_UPPER  # for our aspiration windows so that we look for a score within a certain range
    root_call_beta: int = CHECKMATE_UPPER  # set initial bounds for search which we update after each iteration
    root_call_score: int = 0
    while root_call_depth <= depth:
        root_call_score = nega_max_search(root_call_depth, root_call_alpha, root_call_beta, position, castling[:], opponent_castling[:], en_passant, king_passant)
        if len(root_call_move_list) == 0:  # current position is checkmate or stalemate, return empty move
            return (0, 0, "", "")
        if root_call_score >= root_call_beta:  # search resulted in fail-hard beta cutoff so we need to re-search
            root_call_alpha = -CHECKMATE_UPPER  # reset bounds for re-search
            root_call_beta = CHECKMATE_UPPER
        else:
            root_call_alpha = root_call_score - (MIDGAME_PAWN_VALUE // 2)  # set new bounds for search
            root_call_beta = root_call_score + (MIDGAME_PAWN_VALUE // 2)
            root_call_depth += 1  # only increase depth if we don't need to re-search
    return root_call_move_list[0]  # ordered in descending order so the first move is the best


################
# UCI PROTOCOL #
################

def parse_coordinates(coordinate: str) -> int:
    """Converts a coordinate string (e.g. "a1") to an integer matching an index in the board representation."""
    file: int = ord(coordinate[0]) - ord("a")
    rank: int = int(coordinate[1]) - 1
    return A1 + file - 10 * rank


def render_coordinates(index: int) -> str:
    """Converts an index in the board representation to a coordinate string (e.g. "a1")."""
    rank: int = (index - A1) // 10
    file: int = (index - A1) % 10
    return chr(ord("a") + file) + str(1 - rank)


def load_fen(fen: str) -> tuple[str, list[bool], list[bool], int, int, str]:
    """Configures the board according to the given FEN string and returns the board information."""
    list_position: list[str] = [" "] * 120
    fields: list[str] = fen.split(" ")
    rows: list[str] = fields[0].split("/")
    for row in range(8):
        index: int = A8 + (10 * row)
        for piece in rows[row]:
            if piece in "PNBRQKpnbrqk":
                list_position[index] = piece
                index += 1
            elif piece in "12345678":
                for _ in range(int(piece)):
                    list_position[index] = "."
                    index += 1
    for new_line_index in [9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119]:
        list_position[new_line_index] = "\n"
    castling_rights = fields[2]
    position = "".join(list_position)
    castling: list[bool] = [True if "Q" in castling_rights else False, True if "K" in castling_rights else False]
    opponent_castling: list[bool] = [True if "q" in castling_rights else False, True if "k" in castling_rights else False]
    en_passant: int = parse_coordinates(fields[3]) if fields[3] != "-" else 0
    king_passant: int = 0
    color = fields[1]
    if color == "b":
        position, castling, opponent_castling, en_passant, king_passant = rotate_position(position, castling, opponent_castling, en_passant, king_passant)
    return position, castling, opponent_castling, en_passant, king_passant, color


def send_response(response: str) -> None:
    """Sends the given response to the stdout, flushing the buffer."""
    sys.stdout.write(response + "\n")
    sys.stdout.flush()


def main() -> None:
    """The main UCI protocol loop responsible for parsing commands and sending responses. Sets up the board and
    calls the search function when instructed."""
    global position, castling, opponent_castling, en_passant, king_passant, color
    while True:
        command: str = sys.stdin.readline().strip()
        tokens: list[str] = command.split()
        if tokens[0] == "uci":
            send_response(f"id name {NAME} {VERSION}")
            send_response(f"id author {AUTHOR}")
            send_response("uciok")
        elif tokens[0] == "isready":
            send_response("readyok")
        elif tokens[0] == "quit":
            sys.exit()
        elif tokens[0] == "ucinewgame":
            TRANSPOSITION_TABLE.clear()
        elif tokens[0] == "position":
            if tokens[1] == "startpos":
                position = INITIAL_POSITION
                castling = INITIAL_CASTLING[:]
                opponent_castling = INITIAL_OPPONENT_CASTLING[:]
                en_passant = INITIAL_EN_PASSANT
                king_passant = INITIAL_KING_PASSANT
                color = INITIAL_COLOR
            elif tokens[1] == "fen":
                fen: str = " ".join(tokens[2:8])
                position, castling, opponent_castling, en_passant, king_passant, color = load_fen(fen)
            if "moves" in tokens:
                moves_index: int = tokens.index("moves") + 1
                moves: list[str] = tokens[moves_index:]
                ply: int = 0
                for ply, move in enumerate(moves):
                    start_square: int = parse_coordinates(move[:2])
                    end_square: int = parse_coordinates(move[2:4])
                    promotion_piece: str = move[4:].upper()
                    if color == "b":  # if black to move, flip the coordinates
                        start_square = 119 - start_square
                        end_square = 119 - end_square
                    if ply % 2 == 1:  # opponent's move so we flip the coordinates, then rotate the board before and after making the move
                        start_square = 119 - start_square
                        end_square = 119 - end_square
                        position, castling, opponent_castling, en_passant, king_passant = rotate_position(position, castling, opponent_castling, en_passant, king_passant)
                        position, castling, opponent_castling, en_passant, king_passant = make_move((start_square, end_square, ".", promotion_piece), position, castling, opponent_castling, en_passant, king_passant)
                        position, castling, opponent_castling, en_passant, king_passant = rotate_position(position, castling, opponent_castling, en_passant, king_passant)
                    else:  # our move so we just make it
                        position, castling, opponent_castling, en_passant, king_passant = make_move((start_square, end_square, ".", promotion_piece), position, castling, opponent_castling, en_passant, king_passant)
                if ply % 2 == 0:  # rotate the board after the last move was made and switch the color
                    position, castling, opponent_castling, en_passant, king_passant = rotate_position(position, castling, opponent_castling, en_passant, king_passant)
                    if color == "w":
                        color = "b"
                    elif color == "b":
                        color = "w"
            king_passant = 0
        elif tokens[0] == "go":
            best_move: tuple[int, int, str, str] = search_position(4, position, castling, opponent_castling, en_passant, king_passant)
            start_square: int = best_move[0]
            end_square: int = best_move[1]
            promotion_piece: str = best_move[3]
            if color == "b":
                start_square = 119 - start_square
                end_square = 119 - end_square
            if best_move == (0, 0, "", ""):
                move_string: str = "0000"
            else:
                move_string: str = render_coordinates(start_square) + render_coordinates(end_square) + promotion_piece.lower()
            send_response(f"bestmove {move_string}")


if __name__ == "__main__":
    main()
