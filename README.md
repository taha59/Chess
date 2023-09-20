# Chess Project

This is a Python implementation of a Chess game using the Pygame library. It provides a graphical interface for playing chess against another human player. The game follows the standard rules of chess, including legal moves, capturing pieces, and special moves such as castling and pawn promotion.

## App Demonstration
[chess_App_Demonstration.webm](https://github.com/taha59/Chess/assets/90119856/01bc51e6-a6f8-44f1-8b14-34e0dcce3161)

## Prerequisites

- Python 3.10
- Pygame library

## Installation

1. Clone the repository or download the source code.
2. Install the Pygame library by running the following command:
```
pip install pygame
```

## How to Run

1. Navigate to the project directory.
2. Run the following command to start the game:
```
python3 chess.py
```
4. The game window will open, and you can start playing chess.

## Game Controls

- Click on a piece to select it and drop it to your desired square.
- Use the mouse to interact with the game interface.
- Undo a move by clicking the 'z' key. You can't undo a move once the game ends in a stalemate or a draw.

## Features

- Graphical interface using Pygame library.
- Support for standard chess rules and moves.
- Special moves: castling and pawn promotion.
- Turn-based gameplay for two human players.
- Basic error handling for invalid moves.

## Code Structure

The code is organized into the following files:

- `chess.py`: Main file to run the game.
- `const.py`: Contains constant values and configurations.
- `README.md`: Documentation file.
- `images/`: Directory containing chess piece images.

The main logic of the chess game is implemented in the `Chess` class in the `chess.py` file. It handles the game state, board representation, move validation, and graphical rendering.
