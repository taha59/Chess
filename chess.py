import pygame
from const import *

class Chess:
    def __init__(self):
        #initialize the chess board
    
        # Board pieces representation:

        # black pieces:
        # bR as black rook
        # bN as black knight -- 
        # bB as black bishop
        # bQ as black queen
        # bK as black king --
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
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
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
        self.possible_moves = []
        self.color = {}
        self.color["b"] = "BLACK"
        self.color["w"] = "WHITE"

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
                if self.board[r][c] != "":
                    self.window.blit(self.images[self.board[r][c]], pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

    def chess_graphics(self):
        self.draw_board()
        self.draw_pieces()

    def get_kings_pos(self, x, y):
        king_pos = 0
        
        if self.board[x][y][0] == "w":
            king_pos = self.blackKing_pos
        else:
            king_pos = self.whiteKing_pos

        return king_pos

    def is_checked(self, x, y, king_x, king_y):

        if self.valid_move_check(x, y, king_x, king_y):
            return True
        return False

    def Checkmate():
        s = 0
    def valid_move_check(self, prev_x, prev_y, x, y):
        
        #not a valid move if pieces dont move
        if prev_x == x and prev_y == y:
            return False
        
        #if the chess piece hits another piece with same color its not a valid move
        if self.board[x][y] != "" and self.board[prev_x][prev_y][0] == self.board[x][y][0]:
            return False

        piece = self.board[prev_x][prev_y]

        #Pawn movement
        if piece[1] == 'p':
            return self.move_Pawn(prev_x, prev_y, x, y)

        #Bishop movement
        elif piece[1] == 'B':
            return  self.move_Bishop(prev_x, prev_y, x, y)

        #Rook movement
        elif piece[1] == 'R':
            return self.move_Rook(prev_x, prev_y, x, y)
        
        #queen movement is a combination of rook and bishop movement
        elif piece[1] == 'Q':
            if self.move_Bishop(prev_x, prev_y, x, y) or self.move_Rook(prev_x, prev_y, x, y):
                return True

        #king movement
        elif piece[1] == 'K':
            return self.move_King(prev_x, prev_y, x, y)

        #knight movement
        elif piece[1] == "N":
            return self.move_Knight(prev_x, prev_y, x, y)

        return False

    def move_Pawn(self, prev_x, prev_y, x, y):
        piece = self.board[prev_x][prev_y]
        parity = 1
        #if a pawn is black
        if piece[0] == 'b':
            parity = -1
            if prev_x == 1:
                valid_moves = [1,2]
            else:
                valid_moves = [1]
            
        else:
            if prev_x == 6:
                valid_moves = [1,2]
            else:
                valid_moves = [1]

        for i in range(len(valid_moves)):
            #pawn up movement
            if (prev_x - (parity * valid_moves[i]) ) == x and y == prev_y and self.board[x][y] == "":
                return True

        #pawn up - right movement
        pawn_x = prev_x - (parity * 1)
        pawn_y = prev_y + (parity * 1)

        if pawn_x == x and pawn_y == y and self.board[x][y] != "":
            return True
            
        #pawn up - left movement
        pawn_x = prev_x - (parity * 1)
        pawn_y = prev_y - (parity * 1)

        
        if pawn_x == x and pawn_y == y and self.board[x][y] != "":
            return True

    def move_Rook(self, prev_x, prev_y, x, y):
            
        #horizontal movement
        if (x == prev_x and (y >= 0 and y <= 8) ):

            if y - prev_y > 0:
                print("going right")
                for i in range(prev_y + 1, y):
                    if self.board[x][i] != "":
                        return False
            else:
                print("going left")
                for i in range(y + 1, prev_y):
                    if self.board[x][i] != "":
                        return False

            return True
                
        #vertical movement
        elif (y == prev_y and (x >= 0 and x <= 8) ):
            
            #check for blocked paths
            if x - prev_x > 0:
                print("going down")
                for i in range(prev_x + 1, x):
                    if self.board[i][y] != "":
                        return False
            else:
                print("going up")
                for i in range(x + 1, prev_x):
                    if self.board[i][y] != "":
                        return False

            return True

    def move_Bishop(self, prev_x, prev_y, x, y):

        #Down right
        if ((x - prev_x == y - prev_y) and (x - prev_x > 0)):
            
            print("b down right move")
        
            value = x - prev_x

            for i in range(1, y - prev_y):
                if self.board[prev_x + i][prev_y + i] != "":
                    return False
                print(prev_x + i, prev_y + i)
                    
            if (value) >= 1 and (value) <= 8:
                return True
                    

        #Down left
        elif ((x - prev_x == prev_y - y) and (x - prev_x > 0)):
            print("b down left move")

            for i in range(1, prev_y - y):
                if self.board[prev_x + i][prev_y - i] != "":
                    return False
                
                print(prev_x + i, prev_y - i)

            value = x - prev_x
            if (value) >= 1 and (value) <= 8:
                return True

        #Up right
        elif (prev_x - x == y - prev_y):
            print("b up right move")

            for i in range(1, y - prev_y):
               
                if self.board[prev_x - i][prev_y + i] != "":
                    return False
                print(prev_x - i, prev_y + i)
            value = prev_x - x
            if (value) >= 1 and (value) <= 8:
                return True

        #Up left
        elif (prev_x - x == prev_y - y):
            print("b up left move")
            
            for i in range(1, prev_y - y):
                print(prev_x - i, prev_y - i)
                if self.board[prev_x - i][prev_y - i] != "":
                    return False

            value = prev_x - x
            if (value) >= 1 and (value) <= 8:
                return True

    def move_Knight(self, prev_x, prev_y, x, y):

        #up right - 1
        if x == prev_x - 2 and y == prev_y + 1:
            return True
        
        #up right - 2
        elif x == prev_x - 1 and y == prev_y + 2:
            return True

        #up left - 1
        elif x == prev_x - 2 and y == prev_y - 1:
            return True
        
        #up left - 2
        elif x == prev_x - 1 and y == prev_y - 2:
            return True

        #down left - 1
        elif x == prev_x + 2 and y == prev_y - 1:
            return True

        #down left - 2
        elif x == prev_x + 1 and y == prev_y - 2:
            return True

        #down right - 1
        elif x == prev_x + 2 and y == prev_y + 1:
            return True
        
        #down right - 2
        elif x == prev_x + 1 and y == prev_y + 2:
            return True

    def move_King(self, prev_x, prev_y, x, y):
        #up
        if x == prev_x - 1 and y == prev_y:
            return True

        #up left
        elif x == prev_x - 1 and y == prev_y - 1:
            return True
        
        #up right
        elif x == prev_x - 1 and y == prev_y + 1:
            return True
        
        #left
        elif x == prev_x and y == prev_y - 1:
            return True
        
        #right
        elif x == prev_x and y == prev_y + 1:
            return True
        
        #down left
        elif x == prev_x + 1 and y == prev_y - 1:
            return True

        #down
        elif x == prev_x + 1 and y == prev_y:
            return True

        #down right
        elif x == prev_x + 1 and y == prev_y + 1:
            return True
    
    def Multi_player(self):

        run = True
        clock = pygame.time.Clock()
        self.load_imgs()
        
        selected_piece = False

        Turns = 0
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

                    if self.board[self.x][self.y] != "":
                        
                        chess_piece_color = ["w", "b"]
                        
                        if chess_piece_color[Turns % 2] != self.board[self.x][self.y][0]:
                            print(self.color[chess_piece_color[Turns % 2]], "Turn !!!!!!!!!")
                            continue

                        selected_piece = True
                        print(self.board[self.x][self.y], "selected at pos", self.x, self.y)
                        

                #when a selected piece is dropped on a location
                elif event.type == pygame.MOUSEBUTTONUP and selected_piece == True:
                    print(self.possible_moves)
                    self.y,self.x = pygame.mouse.get_pos()
                    self.x = int(self.x / sq_size)
                    self.y = int(self.y / sq_size)
                    
                    #if a chess piece was dropped successfully set the boolean to false
                    selected_piece = False

                    print("left at", self.x, self.y)
                    
                    #if the move is valid, move the selected piece to where the user wants to place it on the board then clear the prev piece
                    if self.valid_move_check(self.prev_x, self.prev_y, self.x, self.y):
                        x = self.x
                        y = self.y
                        
                        self.board[self.x][self.y] = self.board[self.prev_x][self.prev_y]
                        self.board[self.prev_x][self.prev_y] = ""
                        
                        #update king pos if its moved to a new location
                        if self.board[self.x][self.y] == "wK":
                            self.whiteKing_pos = [self.x,self.y]
                        elif self.board[self.x][self.y] == "bK":
                            self.blackKing_pos = [self.x,self.y]
                        
                        king_pos = self.get_kings_pos(x, y)

                        #confirm if the opposing king is checked whenever any chess piece is moved
                        if self.is_checked(self.x, self.y, king_pos[0], king_pos[1]):
                            print(self.board[self.x][self.y], "checked", self.board[king_pos[0]][king_pos[1]])

                            for i in range(8):
                                for j in range(8):

                                    #insert valid king moves into a list by placing the king to each cord on the board and checking if its a valid move or not
                                    if self.valid_move_check(king_pos[0], king_pos[1], i, j):
                                        if [i,j] not in self.possible_moves:
                                            self.possible_moves.append([i,j])
                                        
                                        #if the king is being checked at i,j remove it from the king's possible moves as it cant move to a location that is in check
                                        if self.is_checked(self.x, self.y, i, j):
                                            self.possible_moves.remove([i,j])

                            #if the king is in check and there are no possible moves left for the king, end the game and display a checkmate message
                            if len(self.possible_moves) == 0:
                                print("Checkmate!", self.color[self.board[self.x][self.y][0]], "wins")
                                exit()
                                        
                        print(self.possible_moves)
                        self.possible_moves.clear()
                        Turns += 1
                    else:
                        continue
                
                    
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
    