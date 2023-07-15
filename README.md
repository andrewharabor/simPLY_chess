# simPLY_chess

## Introduction

A simple chess engine written in Python. This project was heavily inspired by [Sunfish](https://github.com/thomasahle/sunfish/tree/master), including some of its ports to faster languages as well as other engines based around Sunfish. The [Chess Programming Wiki](https://www.chessprogramming.org/Main_Page) was of great help since it explains nearly every chess programming concept in detail.

## How to play against simPLY_chess

 I initially planned to use the official [API](https://github.com/lichess-bot-devs/lichess-bot) to put the engine on [Lichess](https://lichess.org/) but until then, just import the engine in a [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) [GUI](https://www.chessprogramming.org/GUI) if you want to play against it.

[simPLY_chess1.0-vs-simPLY_chess3.3.webm](https://github.com/andrewharabor/simPLY_chess/assets/120438036/20100e3f-d2f4-4b2a-9b93-9a0e78756529)

## Features

- [NegaMax](https://www.chessprogramming.org/Negamax) search with [alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta) and [quiescence search](https://www.chessprogramming.org/Quiescence_Search) within an [iterative deepening](https://www.chessprogramming.org/Iterative_Deepening) loop

- [Piece square tables](https://www.chessprogramming.org/Piece-Square_Tables), [king tropism](https://www.chessprogramming.org/King_Safety#King_Tropism), [mop-up evaluation](https://www.chessprogramming.org/Mop-up_Evaluation), and [tapered evaluation](https://www.chessprogramming.org/Tapered_Eval)

- [Transposition table](https://www.chessprogramming.org/Transposition_Table) with [Zobrist hashing](https://www.chessprogramming.org/Zobrist_Hashing) along with  built-in [PolyGlot](https://www.chessprogramming.org/Polyglot) [opening book](https://www.chessprogramming.org/Opening_Book) reader

- Communicates through standard [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) protocol
  - Standard commands:
    - `uci`: Tell engine to use the uci (universal chess interface), this will be sent once as a first command after program boot to tell the engine to switch to uci mode.
    - `isready`: This is used to synchronize the engine with the GUI. When the GUI has sent a command or multiple commands that can take some time to complete, this command can be used to wait for the engine to be ready again or to ping the engine to find out if it is still alive.
    - `ucinewgame`: This is sent to the engine when the next search (started with `position` and `go`) will be from a different game. This can be a new game the engine should play or a new game it should analyze but also the next position from a testsuite with positions only.
    - `position [fen <fenstring> | startpos ]  moves <move1> .... <movei>`: Set up the position described in fenstring on the internal board and play the moves on the internal chess board. If the game was played from the start position, the string `startpos` should be sent
    - `go`: Start calculating on the current position set up with the `position` command. There are a number of commands that can follow this command, all will be sent in the same string. If just `go` is sent, `go depth 5 movetime 10000` is run by default.
      - `wtime <x>`: White has x milliseconds left on the clock.
      - `btime <x>`: Black has x milliseconds left on the clock.
      - `winc <x>`: White increment per move in milliseconds if x > 0.
      - `binc <x>`: Black increment per move in milliseconds if x > 0.
      - `depth <x>`: Search x plies only.
      - `movetime <x>`: Search exactly x milliseconds.
    - `quit`: Quit the program as soon as possible.
  - Custom commands:
    - `board`: Display the current position, with ASCII art and FEN.
    - `eval`: Display the static evaluation of the current position.
    - `flip`: Flips the side to move.

## Limitations

- Relies on a [GUI](https://www.chessprogramming.org/GUI) for features like time control and stalemate/checkmate detection

- Written in Python meaning that it can't search past a depth of 4-ply in a reasonable amount of time for most positions, especially in the middlegame

- Does not take 3-fold repetition or the fifty-move-rule into account meaning that those rules can be exploited when the engine has a winning position

- Lacks various other [search](https://www.chessprogramming.org/Search) techniques that could improve its speed and strength

## My Thoughts

I decided to program this engine because I enjoy playing chess and I figured it would be a challenging project. Despite all of its limitations, the engine plays better than I had initially thought it would. There are many ways I could improve the playing strength and speed and while I will likely come back and implement some of them, my original goal with this project has been fulfilled. Overall, I'm happy with the result and I really enjoyed the process.
