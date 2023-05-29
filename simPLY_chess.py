
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

# Piece square tables, used to evaluate the position through the positioning of the pieces
# For black, the tables are rotated
PIECE_SQUARE_TABLES: dict[str, list[int]] = {
    'P': [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0, 929, 929, 929, 929, 929, 929, 929, 929,   0,  # while pawns can't reach the last rank, the engine disregards promotion if this row is set to zeros
            0,  78,  83,  86,  73, 102,  82,  85,  90,   0,
            0,   7,  29,  21,  44,  40,  31,  44,   7,   0,
            0, -17,  16,  -2,  15,  14,   0,  15, -13,   0,
            0, -26,   3,  10,   9,   6,   1,   0, -23,   0,
            0, -22,   9,   5, -11, -10,  -2,   3, -19,   0,
            0, -31,   8,  -7, -37, -36, -14,   3, -31,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0],

    'N': [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0, -66, -53, -75, -75, -10, -55, -58, -70,   0,
            0,  -3,  -6, 100, -36,   4,  62,  -4, -14,   0,
            0,  10,  67,   1,  74,  73,  27,  62,  -2,   0,
            0,  24,  24,  45,  37,  33,  41,  25,  17,   0,
            0,  -1,   5,  31,  21,  22,  35,   2,   0,   0,
            0, -18,  10,  13,  22,  18,  15,  11, -14,   0,
            0, -23, -15,   2,   0,   2,   0, -23, -20,   0,
            0, -74, -23, -26, -24, -19, -35, -22, -69,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0],

    'B': [  0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,  -59, -78, -82, -76, -23,-107, -37, -50,  0,
            0,  -11,  20,  35, -42, -39,  31,   2, -22,  0,
            0,   -9,  39, -32,  41,  52, -10,  28, -14,  0,
            0,   25,  17,  20,  34,  26,  25,  15,  10,  0,
            0,   13,  10,  17,  23,  17,  16,   0,   7,  0,
            0,   14,  25,  24,  15,   8,  25,  20,  15,  0,
            0,   19,  20,  11,   6,   7,   6,  20,  16,  0,
            0,   -7,   2, -15, -12, -14, -15, -10, -10,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0],

    'R': [  0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,   35,  29,  33,   4,  37,  33,  56,  50,  0,
            0,   55,  29,  56,  67,  55,  62,  34,  60,  0,
            0,   19,  35,  28,  33,  45,  27,  25,  15,  0,
            0,    0,   5,  16,  13,  18,  -4,  -9,  -6,  0,
            0,  -28, -35, -16, -21, -13, -29, -46, -30,  0,
            0,  -42, -28, -42, -25, -25, -35, -26, -46,  0,
            0,  -53, -38, -31, -26, -29, -43, -44, -53,  0,
            0,  -30, -24, -18,   5,  -2, -18, -31, -32,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0],

    'Q': [  0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    6,   1,  -8,-104,  69,  24,  88,  26,  0,
            0,   14,  32,  60, -10,  20,  76,  57,  24,  0,
            0,   -2,  43,  32,  60,  72,  63,  43,   2,  0,
            0,    1, -16,  22,  17,  25,  20, -13,  -6,  0,
            0,  -14, -15,  -2,  -5,  -1, -10, -20, -22,  0,
            0,  -30,  -6, -13, -11, -16, -11, -16, -27,  0,
            0,  -36, -18,   0, -19, -15, -15, -21, -38,  0,
            0,  -39, -30, -31, -13, -31, -36, -34, -42,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0],

    'K': [  0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    4,  54,  47, -99, -99,  60,  83, -62,  0,
            0,  -32,  10,  55,  56,  56,  55,  10,   3,  0,
            0,  -62,  12, -57,  44, -67,  28,  37, -31,  0,
            0,  -55,  50,  11,  -4, -19,  13,   0, -49,  0,
            0,  -55, -43, -52, -28, -51, -47,  -8, -50,  0,
            0,  -47, -42, -43, -79, -64, -32, -29, -32,  0,
            0,   -4,   3, -14, -50, -57, -18,  13,   4,  0,
            0,   17,  30,  -3, -14,   6,  -1,  40,  18,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0,
            0,    0,   0,   0,   0,   0,   0,   0,   0,  0]
}

# Piece values, used for material evaluation
PIECE_VALUES: dict[str, int] = {
    "": 0,
    "P": 100,
    "N": 280,
    "B": 320,
    "R": 479,
    "Q": 929,
    "K": 60000,
}

# Checkmate scores
CHECKMATE_UPPER = PIECE_VALUES["K"] + 10 * PIECE_VALUES["Q"]
CHECKMATE_LOWER = PIECE_VALUES["K"] - 10 * PIECE_VALUES["Q"]


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


def find_check(position: str, king_passant: int) -> bool:
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

def evaluate_position(position: str) -> int:
    """Evaluates the given position for the side-to-move and returns a score. Only considers basic positional evaluation
    (piece-square tables) and piece material point-values."""
    score: int = 0
    for square, piece in enumerate(position):
        if piece.isupper():  # ally piece
            score += PIECE_VALUES[piece] + PIECE_SQUARE_TABLES[piece][square]
        elif piece.islower():  # opponent piece
            score -= PIECE_VALUES[piece.upper()] + PIECE_SQUARE_TABLES[piece.upper()][119 - square]
    return score

def evaluate_move(move: tuple[int, int, str, str], position: str, en_passant: int) -> int:
    """Evaluates the given move for the side-to-move and returns a score."""
    start_square: int = move[0]
    end_square: int = move[1]
    piece_moved: str = position[start_square]
    piece_captured: str = move[2]
    promotion_piece: str = move[3]
    score: int = PIECE_SQUARE_TABLES[piece_moved][end_square] - PIECE_SQUARE_TABLES[piece_moved][start_square]
    if piece_captured.islower():  # capture
        score += PIECE_SQUARE_TABLES[piece_captured.upper()][119 - end_square]
    if piece_moved == "K" and abs(start_square - end_square) == 2:  # castling
        score += PIECE_SQUARE_TABLES["R"][(start_square + end_square) // 2] - PIECE_SQUARE_TABLES["R"][A1 if end_square < start_square else H1]
    if piece_moved == "P":
        if A8 <= end_square <= H8:  # pawn promotion
            score += PIECE_SQUARE_TABLES[promotion_piece][end_square] - PIECE_SQUARE_TABLES["P"][end_square]
            score += PIECE_VALUES[promotion_piece] - PIECE_VALUES["P"]
        if end_square + SOUTH == en_passant:
            score += PIECE_SQUARE_TABLES["P"][119 - (end_square + SOUTH)]
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
            if not find_check(new_position[0], new_position[4]): # if the move doesn't result in our king being in check (legal move)
                delta: int = 200
                if stand_pat + PIECE_VALUES[move[2].upper()] + PIECE_VALUES[move[3]] + delta > alpha:  # delta pruning
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
        best_move: tuple[int, int, str, str] = move_list[0]
        for move in move_list:
            new_position: tuple[str, list[bool], list[bool], int, int] = make_move(move, position, castling[:], opponent_castling[:], en_passant, king_passant)
            new_position = rotate_position(*new_position)
            if not find_check(new_position[0], new_position[4]):  # if the move doesn't result in our king being in check (legal move)
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
            if find_check(new_position[0], 0):
                return -CHECKMATE_LOWER - depth

            else:
                return 0

        else:
            if depth == root_call_depth:  # only sort moves at the root
                moves.sort(key=lambda pair: pair[0], reverse=True)
                root_call_move_list = [pair[1] for pair in moves]
            if depth > 1:  # if depth is higher, this could be increased for a more accurate transposition table
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
            root_call_alpha = root_call_score - (PIECE_VALUES["P"] // 2)  # set new bounds for search
            root_call_beta = root_call_score + (PIECE_VALUES["P"] // 2)
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
            # Even with iterative deepening and the likes, the engine is still too slow to search more than 3 ply (likely because of quiescence search).
            # Without quiescence search, the engine is able to search 4 ply in a reasonable amount of time but move quality is sacrificed.
            best_move: tuple[int, int, str, str] = search_position(3, position, castling, opponent_castling, en_passant, king_passant)
            start_square: int = best_move[0]
            end_square: int = best_move[1]
            promotion_piece: str = best_move[3]
            if color == "b":
                start_square = 119 - start_square
                end_square = 119 - end_square
            if best_move == (0, 0, "", ""):
                move_string: str = "(none)"
            else:
                move_string: str = render_coordinates(start_square) + render_coordinates(end_square) + promotion_piece.lower()
            send_response(f"bestmove {move_string}")


if __name__ == "__main__":
    main()
