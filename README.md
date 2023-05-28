# simPLY_chess

## Introduction

A simple and minimalist chess engine written in Python. This project was heavily inspired by [Sunfish](https://github.com/thomasahle/sunfish/tree/master), including some of its ports to faster languages as well as other engines based around Sunfish. The [Chess Programming Wiki](https://www.chessprogramming.org/Main_Page) was of great help since it explains nearly every chess programming concept in detail.

## How to play against simPLY_chess

 I initially planned to use the official [API](https://github.com/lichess-bot-devs/lichess-bot) to put the engine on [Lichess](https://lichess.org/) but until then, just import the engine in a [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) [GUI](https://www.chessprogramming.org/GUI) if you want to play against it.

## Features

- [Piece material values](https://www.chessprogramming.org/Point_Value) for the core of the [evaluation](https://www.chessprogramming.org/Evaluation) function

- [Piece square tables](https://www.chessprogramming.org/Piece-Square_Tables) to give the engine positional "knowledge"

- Basic [transposition table](https://www.chessprogramming.org/Transposition_Table) (without hashing) to improve search times and limit redundant computation

- 3-ply [negamax search](https://www.chessprogramming.org/Negamax) algorithm with [alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta) to greatly reduce the number of nodes searched

- [Quiescence search](https://www.chessprogramming.org/Quiescence_Search) to avoid the [horizon](https://www.chessprogramming.org/Horizon_Effect) effect along with [delta pruning](https://www.chessprogramming.org/Delta_Pruning)

- [Iterative deepening](https://www.chessprogramming.org/Iterative_Deepening) framework to counter-intuitively speed up search times through [move ordering](https://www.chessprogramming.org/Move_Ordering) from the last fully-completed search

- Utilizes [aspiration windows](https://www.chessprogramming.org/Aspiration_Windows) in order to improve the effectiveness of alpha-beta pruning

- Communicates through standard [UCI](https://gist.github.com/DOBRO/2592c6dad754ba67e6dcaec8c90165bf) protocol

## Limitations

- Relies on a [GUI](https://www.chessprogramming.org/GUI) for features like time control and stalemate/checkmate

- Written in Python meaning that it isn't too strong since it can't search past a depth of 4 ply in a reasonable amount of time (even 4 is on the slow side so 3 is recommended)

- Does not take [3-fold repetition](https://www.chessprogramming.org/Repetitions#Fide_Rule) or the [fifty-move-rule](https://www.chessprogramming.org/Fifty-move_Rule#Fide_Rule) into account meaning that those rules can be exploited when the engine has a winning position

- Does not have any [endgame](https://www.chessprogramming.org/Endgame) knowledge nor [endgame-specific evaluation](https://www.chessprogramming.org/Endgame#Evaluation) meaning that it completely misjudges this phase of the game

- Does not have an [opening book](https://www.chessprogramming.org/Opening_Book) meaning that it has almost no variation in the [opening](https://www.chessprogramming.org/Opening) stage of the game

## My Thoughts

I decided to program this engine because I enjoy playing chess and I figured it would be a challenging project. While I had initially hoped for it to be able to beat me, it still plays chess fairly well. There are many ways I could improve the playing strength of the engine (both through new features and optimizations), but for now, I'll just leave it as is. Overall, I learned a lot about search algorithms and I really enjoyed working through this project.
