# About the Project

This is a simple chess game implemented in Python using the Pygame library. It allows you to play chess against another human player on your computer.

# Requirements

Before running the game, ensure that you have the following installed:

- Python (Version 3.10.5): You can download Python from the official website [here](https://www.python.org/downloads/).

- Install pygame 'pip install pygame'

    pip install pygame

# Features

## Game Mechanics
The code implements the basic mechanics of chess, including moving pieces, capturing, and checking for checkmate. The game follows the standard rules of chess.

## User Interface
The code uses the Pygame library to provide a graphical user interface for the chess game. The game board is displayed on a Pygame window, and the user can interact with the game by clicking on the pieces and their destination squares.

## Piece Movement
Each piece has its own movement logic implemented as separate methods in the Chess class. The following piece movement methods are implemented:

- move_Pawn: Handles movement for pawns.
- move_Rook: Handles movement for rooks.
- move_Bishop: Handles movement for bishops.
- move_Knight: Handles movement for knights.
- move_King: Handles movement for kings.
- move_Queen: Handles movement for queens.

## Check and Checkmate Detection
The code includes methods to check for check and checkmate conditions. The `is_in_check` method determines if a player's king is in check, and the `is_checkmate` method checks if a player is in checkmate.

## En Passant Capture
The code handles the special en passant capture rule for pawns. When a pawn moves two squares forward from its starting position and lands beside an opponent's pawn, the opponent can capture the pawn as if it had only moved one square forward.

## Promotion
The code includes logic to handle pawn promotion. When a pawn reaches the opposite end of the board, it can be promoted to a queen, rook, bishop, or knight.

## Code Structure
The code is organized into the following classes and methods:

### Move Class
- `__init__`: Initializes a Move object with the starting and ending positions, the current board state, and whether it is an en passant move or not.
- `__eq__`: Compares two Move objects for equality.

### Chess Class
- `__init__`: Initializes the chess game by setting up the board, loading images, and setting initial game state.
- `load_imgs`: Loads the images of chess pieces from files.
- `draw_board`: Draws the chess board on the Pygame window.
- `draw_pieces`: Draws the chess pieces on the board.
- `chess_graphics`: Draws the entire chess game graphics, including the board and pieces.
- `run`: The main game loop that handles user input and updates the game state.
- Piece movement methods: Methods for handling movement logic for different pieces, such as pawns, rooks, bishops, knights, kings, and queens.
- `in_check`: Checks if a player's king is in check.
- Other helper methods: Various helper methods for game logic, such as updating the game state, handling en passant capture, promoting pawns, etc.
