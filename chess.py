import pygame
from const import *

class chess_piece:
    def __init__(self, start, end, board):
        self.prev_x = start[0]
        self.prev_y = start[1]
        self.x = end[0]
        self.y = end[1]

        self.piece_moved = board[self.prev_x][self.prev_y]
        self.piece_captured = board[self.x][self.y]

class Chess:
    def __init__(self):
        #initialize the chess board
    
        # Board pieces representation:

        # black pieces:
        # bR as black rook
        # bN as black knight
        # bB as black bishop
        # bQ as black queen
        # bK as black king
        # bp as black pawn

        #white pieces:
        # wR as white rook
        # wN as white knight
        # wB as white bishop
        # wQ as white queen
        # wK as white king
        # wp as white pawn
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

            
        self.images = {}
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CHESS")

        #add the unique chess pieces to chess_pieces variable
        self.chess_pieces = list(set(self.board[0])) + list(set(self.board[1])) + list(set(self.board[6])) + list(set(self.board[7]))

        self.prev_x = 0
        self.prev_y = 0
        self.x = 0
        self.y = 0
        self.whiteKing_pos = [7,4]
        self.blackKing_pos = [0,4]
        
        # self.function_dic = {'p': self.move_Pawn()}
        self.move_Log = []
        self.white_Turn = True
            
        

    #maps the pieces to their respective loaded image
    def load_imgs(self):
        for piece in self.chess_pieces:
            self.images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sq_size, sq_size))

    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("grey")]
        for r in range(8):
            for c in range(8):
                #choose color based on the cordinate pair 
                color = colors[((r+c) % 2)]
                pygame.draw.rect(self.window, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "--":
                    self.window.blit(self.images[self.board[r][c]], pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

    def chess_graphics(self):
        self.draw_board()
        self.draw_pieces()

    def get_Possible_Moves(self, prev_x, prev_y):

        piece = self.board[prev_x][prev_y]
        moves = []

        #Pawn movement
        if piece[1] == 'p':
            self.move_Pawn(prev_x, prev_y, moves)

        #Bishop movement
        elif piece[1] == 'B':
            self.move_Bishop(prev_x, prev_y, moves)

        #Rook movement
        elif piece[1] == 'R':
            self.move_Rook(prev_x, prev_y, moves)
        
        #queen movement is a combination of rook and bishop movement
        elif piece[1] == 'Q':
            self.move_Bishop(prev_x, prev_y, moves)
            self.move_Rook(prev_x, prev_y, moves)

        #king movement
        elif piece[1] == 'K':
            self.move_King(prev_x, prev_y, moves)

        #knight movement
        elif piece[1] == "N":
            self.move_Knight(prev_x, prev_y, moves)

        return moves


    def move_Pawn(self, prev_x, prev_y, possible_moves):

        enemy_color = {}
        enemy_color["w"] = "b"
        enemy_color["b"] = "w"

        piece = self.board[prev_x][prev_y]
        parity = 1
        
        #if a pawn is black
        if piece[0] == 'b':
            parity = -1
            if prev_x == 1:
                valid_moves = [1,2]
            else:
                valid_moves = [1]
            
        elif piece[0] == 'w':
            if prev_x == 6:
                valid_moves = [1,2]
            else:
                valid_moves = [1]

        #UP MOVEMENT
        for i in range(len(valid_moves)):
            if MIN_INDEX <= (prev_x - (parity * valid_moves[i])) <= MAX_INDEX and MIN_INDEX <= prev_y <= MAX_INDEX and self.board[prev_x - (parity * valid_moves[i])][prev_y] == "--":
                possible_moves.append([prev_x - (parity * valid_moves[i]), prev_y])

        #RIGHT CAPTURE

        if MIN_INDEX <= (prev_x - parity) <= MAX_INDEX and MIN_INDEX <= (prev_y + parity) <= MAX_INDEX and self.board[prev_x - parity][prev_y + parity][0] == enemy_color[self.board[prev_x][prev_y][0]]:
            possible_moves.append([prev_x - parity, prev_y + parity])
            
        #LEFT CAPTURE

        if  MIN_INDEX <= (prev_x - parity) <= MAX_INDEX and MIN_INDEX <= (prev_y - parity) <= MAX_INDEX and  self.board[prev_x - parity][prev_y - parity][0] == enemy_color[self.board[prev_x][prev_y][0]]:
            possible_moves.append([prev_x - parity, prev_y - parity])
        
        #en passant

        #promotion

    def move_Rook(self, prev_x, prev_y, possible_moves):
        
        enemy_color = {}
        enemy_color["w"] = "b"
        enemy_color["b"] = "w"
        
        #horizontal movement
        for i in range(prev_y + 1, 8):
            
            if self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([prev_x, i])
                break
            elif self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([prev_x, i])


    
        for i in range(prev_y - 1, -1, -1):
            
            if self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([prev_x, i])
                break
            elif self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([prev_x, i])
                
        #vertical movement
        for i in range(prev_x + 1, 8):

            if self.board[prev_x][i][0] != '-' and self.board[i][prev_y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([i, prev_y])
                break
            elif self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([i, prev_y])
            
    
        for i in range(prev_x - 1, -1, -1):

            if self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([i, prev_y])
                break
            elif self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == self.board[prev_x][prev_y][0]:
                break

            possible_moves.append([i, prev_y])

    def move_Bishop(self, prev_x, prev_y, possible_moves):
        enemy_color = {}
        enemy_color["w"] = "b"
        enemy_color["b"] = "w"
      
        #Down right
        x, y = prev_x + 1, prev_y + 1

        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([x, y])
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([x, y])
            x+=1
            y+=1

        
        #Down left
        x, y = prev_x + 1, prev_y - 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([x, y])
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([x, y])
            x+=1
            y-=1

        #Up right
        x, y = prev_x - 1, prev_y + 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([x, y])
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([x, y])

            x-=1
            y+=1
        

        #Up left
        x, y = prev_x - 1, prev_y - 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append([x, y])
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append([x, y])
            x-=1
            y-=1

    def move_Knight(self, prev_x, prev_y, possible_moves):

        all_knight_pos = [[prev_x - 2, prev_y + 1], [prev_x - 1, prev_y + 2], [prev_x - 2, prev_y - 1], [prev_x - 1, prev_y - 2], [prev_x + 2, prev_y - 1], [prev_x + 1, prev_y - 2], [prev_x + 2, prev_y + 1], [prev_x + 1, prev_y + 2]]

        for x,y in all_knight_pos:
            if 0 <= x < 8 and 0 <= y < 8:
                
                if self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                    continue

                possible_moves.append([x,y])

    def move_King(self, prev_x, prev_y, possible_moves):

        all_king_pos = [[prev_x - 1, prev_y], [prev_x - 1, prev_y - 1], [prev_x - 1, prev_y + 1], [prev_x, prev_y - 1], [prev_x, prev_y + 1], [prev_x + 1, prev_y - 1], [prev_x + 1, prev_y], [prev_x + 1, prev_y + 1]]
        
        for x,y in all_king_pos:
            if 0 <= x < 8 and 0 <= y < 8:
                
                if self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                    continue

                possible_moves.append([x,y])

    def undo_move(self):
        if len(self.move_Log) != 0:

            self.white_Turn = not self.white_Turn
            move = self.move_Log.pop()

            prev_x = move[0][0]
            prev_y = move[0][1]
            
            x = move[1][0]
            y = move[1][1]

            piece_captured = move[2]
            
            self.board[prev_x][prev_y] = self.board[x][y]
            self.board[x][y] = piece_captured

            if self.board[prev_x][prev_y] == "wK":
                self.whiteKing_pos = [[prev_x, prev_y]]

            elif self.board[prev_x][prev_y] == "bK":
                self.blackKing_pos = [[prev_x, prev_y]]

    def generate_all_possible_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                turn = self.board[i][j][0]
                if (self.white_Turn == True and turn == "w") or (not self.white_Turn and turn == "b"):
                    moves += self.get_Possible_Moves(i,j)

        return moves

    def get_valid_moves(self):
        moves = self.generate_all_possible_moves()

        for i in range(len(moves)-1, -1, -1):
            self.place_piece()
    
    def place_piece(self, prev_x, prev_y, x, y):
        piece_captured = self.board[x][y]
        self.board[x][y] = self.board[prev_x][prev_y]
        self.board[prev_x][prev_y] = "--"

        #track moves so we can undo later
        self.move_Log.append([[prev_x, prev_y], [x, y], piece_captured])

        if self.board[x][y] == "wK":
            self.whiteKing_pos = [[x, y]]

        elif self.board[x][y] == "bK":
            self.blackKing_pos = [[x, y]]
        
    
    def Multi_player(self):

        run = True
        clock = pygame.time.Clock()
        self.load_imgs()
        
        selected_piece = False

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                #handle events when a chess piece is selected
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.y,self.x = pygame.mouse.get_pos()
                    self.x = int(self.x / sq_size)
                    self.y = int(self.y / sq_size)

                    self.prev_x = self.x
                    self.prev_y = self.y

                    #if a piece is selected mark the piece selected boolean as true
                    if self.board[self.x][self.y] != "--":

                        if self.white_Turn == True and self.board[self.x][self.y][0] == 'b' or self.white_Turn == False and self.board[self.x][self.y][0] == 'w':
                            print("Wait your turn please!")
                            continue

                        selected_piece = True
                        print(self.board[self.x][self.y], "selected at pos:", self.x, self.y)
                        

                #when a selected piece is dropped on a location
                elif event.type == pygame.MOUSEBUTTONUP and selected_piece == True:
        
                    self.y,self.x = pygame.mouse.get_pos()
                    self.x = int(self.x / sq_size)
                    self.y = int(self.y / sq_size)
                    
                    #if a chess piece was dropped successfully set the boolean to false
                    selected_piece = False

                    print("left at", self.x, self.y)
                    
                    #get the possible moves for 
                    moves = self.get_Possible_Moves(self.prev_x, self.prev_y)

                    x = self.x
                    y = self.y

                    if [x,y] in moves:
                        
                        self.place_piece(self.prev_x, self.prev_y, self.x, self.y)
                        
                        print("black king pos:", self.blackKing_pos, "white king pos:", self.whiteKing_pos)
                        print("Possible moves:", moves)
                        self.generate_all_possible_moves()


                        #change turn for every move made
                        self.white_Turn = not self.white_Turn

                    else:
                        continue
                
                #undo when 'z' is clicked
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    
                    self.undo_move()
                
                    
            #draw chess board and pieces
            self.chess_graphics()
            pygame.display.update()
            clock.tick(FPS)
        
        pygame.quit()

def main():
    s = Chess()
    s.Multi_player()


if __name__ == "__main__":
    main()
    