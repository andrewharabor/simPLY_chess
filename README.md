# simPLY_chess

## Introduction

A simple chess engine written in Python. This project was heavily inspired by [Sunfish](https://github.com/thomasahle/sunfish/tree/master), including some of its ports to faster languages as well as other engines based around Sunfish. The [Chess Programming Wiki](https://www.chessprogramming.org/Main_Page) was of great help since it explains nearly every chess programming concept in detail.

## How to play against simPLY_chess

 I initially planned to use the official [API](https://github.com/lichess-bot-devs/lichess-bot) to put the engine on [Lichess](https://lichess.org/) but until then, just import the engine in a [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) [GUI](https://www.chessprogramming.org/GUI) if you want to play against it.

 ![1. d4 d5 2. Nf3 Nf6 3. Be3 Nc6 4. Nc3 Bf5 5. Ne5 e6 6. Nxc6 bxc6 7. h3 Rb8 8. Rb1 Bd6 9. f3 O-O 10. Kf2 Re8 11. g4 Bg6 12. g5 Nh5 13. Rg1 e5 14. dxe5 Bxe5 15. Bc5 d4 16. Na4 Bf4 17. Rg4 Be3+ 18. Ke1 f5 19. Rxd4 Bxd4 20. Qxd4 Qxd4 21. Bxd4 Rb4 22. Bxg7 Kxg7 23. Nc5 Ng3 24. Na6 Ra4 25. Nxc7 Re7 26. Na8 Rxa2 27. Kf2 Nxf1 28. Kxf1 f4 29. e4 fxe3 30. b4 Bxc2 31. Rc1 Bd3+ 32. Kg1 e2 33. Re1 Rb2 34. Kf2 Rb1 35. Rxb1 Bxb1 36. Ke1 Bd3 37. Nb6 axb6 38. h4 Kg6 39. h5+ Kxh5 40. g6 hxg6 41. Kd2 e1=Q+ 42. Kxd3 Qe2+ 43. Kd4 Qe3+ 44. Kc4 b5# 0-1](game.gif)

 _A game that I (with the black pieces) played against simPLY_chess and won._

## Features

- [Piece material values](https://www.chessprogramming.org/Point_Value) for the core of the [evaluation](https://www.chessprogramming.org/Evaluation) function

- [Piece square tables](https://www.chessprogramming.org/Piece-Square_Tables) to give the engine positional "knowledge"

- Basic [transposition table](https://www.chessprogramming.org/Transposition_Table) (without hashing) to improve search times and limit redundant computation by storing the results of previous searches

- [NegaMax search](https://www.chessprogramming.org/Negamax) algorithm with [alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta) to greatly reduce the number of nodes searched by pruning branches that are either too good or too bad

- [Quiescence search](https://www.chessprogramming.org/Quiescence_Search) to avoid the [horizon effect](https://www.chessprogramming.org/Horizon_Effect) along with [delta pruning](https://www.chessprogramming.org/Delta_Pruning) to further reduce the number of nodes searched

- [Iterative deepening](https://www.chessprogramming.org/Iterative_Deepening) to improve the efficiency of the search by utilizing the [transposition table](https://www.chessprogramming.org/Transposition_Table) and the [principal variation](https://www.chessprogramming.org/Principal_Variation) from previous searches

- [Tapered evaluation](https://www.chessprogramming.org/Tapered_Eval) to interpolate between the evaluation of the position using middlegame and endgame criteria

- Variable depth to accomodate time control and user accessibility over search speed

- Communicates through standard [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) protocol to allow for easy integration into any [GUI](https://www.chessprogramming.org/GUI)
  - Standard commands:
    - `uci` - Initiates UCI protocol
    - `isready` - Synchronizes and initializes engine
    - `quit` - Terminates the engine
    - `ucinewgame` - Notifiy engine that next search will be from a different game (and reset the transposition table)
    - `position` - Set up the internal board position accordingly (at least one of the following parameters is required)
      - `startpos | fen <fen>` - Set up the starting position or the position specified by the FEN string
      - `moves <move1> <move2> ... <movei>` - Make the moves specified by the list of moves
    - `go` - Calculate the best move for the current position (the following parameter is required, `go depth 5 wtime 600000 btime 600000 winc 0 binc 0` is the default which limits both depth and time)
      - `depth <depth> | wtime <wtime> btime <btime> winc <winc> binc <binc>` - Limit the search to a certain depth with unlimited time or limit the search through time control with unlimited depth
  - Custom commands:
    - `eval` - Return the static evaluation of the current position
    - `board` - Print the current board position in ASCII art and with the FEN string
    - `flip` - Flip the side to move

## Limitations

- Relies on a [GUI](https://www.chessprogramming.org/GUI) for features like time control and stalemate/checkmate detection

- Written in Python meaning that it isn't too strong since it can't search past a depth of 4-ply in a reasonable amount of time (for most positions)

- Does not take 3-fold repetition or the fifty-move-rule into account meaning that those rules can be exploited when the engine has a winning position

- Does not have an [opening book](https://www.chessprogramming.org/Opening_Book) meaning that it has almost no variation in the opening stage of the game

- Lacks various other [search](https://www.chessprogramming.org/Search) techniques that could improve its speed and strength

## My Thoughts

I decided to program this engine because I enjoy playing chess and I figured it would be a challenging project. Despite all of its limitations, the engine actually plays well enough to draw with and even beat me occasionally. There are many ways I could improve the playing strength and speed and while I will likely come back and implement some of them, my original goal with this project has been fulfilled. Overall, I'm happy with the result and I really enjoyed the process.
