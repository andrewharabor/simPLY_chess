# simPLY_chess

## Introduction

A simple chess engine written in Python. This project was heavily inspired by [Sunfish](https://github.com/thomasahle/sunfish/tree/master), including some of its ports to faster languages as well as other engines based around Sunfish. The [Chess Programming Wiki](https://www.chessprogramming.org/Main_Page) was of great help since it explains nearly every chess programming concept in detail.

## How to play against simPLY_chess

 I initially planned to use the official [API](https://github.com/lichess-bot-devs/lichess-bot) to put the engine on [Lichess](https://lichess.org/) but until then, just import the engine in a [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) [GUI](https://www.chessprogramming.org/GUI) if you want to play against it.

[simPLY_chess v0.2.0 2023 V.S. Stockfish 14+ NNUE.webm](https://github.com/andrewharabor/simPLY_chess/assets/120438036/44203cec-63ab-4ae2-9c22-98c4768d2763)

## Features

- [Piece material values](https://www.chessprogramming.org/Point_Value) for the core of the [evaluation](https://www.chessprogramming.org/Evaluation) function

- [Piece square tables](https://www.chessprogramming.org/Piece-Square_Tables) to give the engine positional "knowledge"

- Basic [transposition table](https://www.chessprogramming.org/Transposition_Table) (without hashing) to improve search times and limit redundant computation by storing the results of previous searches

- [NegaMax search](https://www.chessprogramming.org/Negamax) algorithm with [alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta) to greatly reduce the number of nodes searched by pruning branches that are either too good or too bad

- [Quiescence search](https://www.chessprogramming.org/Quiescence_Search) to avoid the [horizon effect](https://www.chessprogramming.org/Horizon_Effect) along with [delta pruning](https://www.chessprogramming.org/Delta_Pruning) to further reduce the number of nodes searched

- [Iterative deepening](https://www.chessprogramming.org/Iterative_Deepening) to improve the efficiency of the search by utilizing the [transposition table](https://www.chessprogramming.org/Transposition_Table) and the [principal variation](https://www.chessprogramming.org/Principal_Variation) from previous searches

- [Tapered evaluation](https://www.chessprogramming.org/Tapered_Eval) to interpolate between the evaluation of the position using middlegame and endgame criteria

- Variable depth to accomodate time control and user accessibility over search time

- Communicates through standard [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) protocol to allow for easy integration into any [GUI](https://www.chessprogramming.org/GUI)
  - Standard commands:
    - `uci` - Initiate UCI protocol
    - `isready` - Synchronize and initialize engine
    - `quit` - Terminate the engine
    - `ucinewgame` - Notifiy engine that next search will be from a different game (and reset the transposition table)
    - `position` - Set up the internal board position accordingly (at least one of the following parameters is required)
      - `startpos | fen <fen>` - Set up the starting position or the position specified by the FEN string
      - `moves <move1> <move2> ... <movei>` - Make the moves specified by the list of moves
    - `go` - Calculate the best move for the current position (the following parameters are optional, `go depth 5 movetime 10000` is the default)
      - `depth <depth>` - Limit the search to a certain depth
      - `movetime <movetime>` - Limit the search to a certain time (in milliseconds)
      - `wtime <wtime> btime <btime> winc <winc> binc <binc>` - Limit the search through time control (in milliseconds)
      - `infinite` - Search without a time or depth limit, note that the engine is unable to respond to `stop` commands in this mode (even though it should be able to) and will NEVER stop searching
  - Custom commands (inspired by Stockfish):
    - `eval` - Return the static evaluation of the current position
    - `board` - Print the current board position in ASCII art and with the FEN string
    - `flip` - Flip the side to move

## Limitations

- Relies on a [GUI](https://www.chessprogramming.org/GUI) for features like time control and stalemate/checkmate detection

- Written in Python meaning that it can't search past a depth of 4-ply in a reasonable amount of time for most positions, especially in the middlegame

- Does not take 3-fold repetition or the fifty-move-rule into account meaning that those rules can be exploited when the engine has a winning position

- Does not have an [opening book](https://www.chessprogramming.org/Opening_Book) meaning that it has no variation in the opening stage of the game and may not always play according to modern theory

- Lacks various other [search](https://www.chessprogramming.org/Search) techniques that could improve its speed and strength

## My Thoughts

I decided to program this engine because I enjoy playing chess and I figured it would be a challenging project. Despite all of its limitations, the engine actually plays well enough to draw with and even beat me occasionally. There are many ways I could improve the playing strength and speed and while I will likely come back and implement some of them, my original goal with this project has been fulfilled. Overall, I'm happy with the result and I really enjoyed the process.
