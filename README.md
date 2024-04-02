# ChessKoban

ChessKoban is a chess variant that combines elements of Chess and Sokoban. The goal is to move the white knights to positions where they can capture the black pawns. Each white knight can only capture a single black pawn. The game is won when all black pawns are being captured at the same time by the white knights.

## Prerequisites

- Python 3.x
- Pygame
- Psutil

## Installation

```bash
pip install pygame psutil
```

## Usage

### Windows

```bash
python main.py
```

### Linux

```bash
python3 main.py
```

## How to play

- Use the arrow keys to move the pawn. If the pawn is adjacent to a white knight, the pawn can push the knight in the direction of movement
- Use the space key to get hints when you are stuck
- Use the Z key to undo the last move

## Game Modes

- **Human**: Play the game manually
- **BFS**: The computer will solve the game using Breadth First Search
- **DFS**: The computer will solve the game using Depth First Search
- **IDDFS**: The computer will solve the game using Iterative Deepening Depth First Search
- **AStar**: The computer will solve the game using A* Search
- **Uniform Cost**: The computer will solve the game using Uniform Cost Search
- **Greedy**: The computer will solve the game using Greedy Search
- **Weighted AStar**: The computer will solve the game using Weighted A* Search
- **IDAStar**: The computer will solve the game using Iterative Deepening A* Search

### Team

* Carolina Couto Viana - 202108802
* João Oliveira - 202108737
* Sérgio Peixoto - 202108681
