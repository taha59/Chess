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

    def is_checked(self):
        king_pos = 0
        #print if a piece was checked
        if self.board[self.x][self.y][0] == "w":
            king_pos = self.blackKing_pos
        else:
            king_pos = self.whiteKing_pos
        

        self.prev_x = self.x
        self.prev_y = self.y

        self.x = king_pos[0]
        self.y = king_pos[1]

        if (self.valid_move_check()):
            return True
        return False

    def Checkmate():
        s = 0
    def valid_move_check(self):

        #if the chess piece hits another piece with same color its not a valid move
        if self.collision() == True:
            return False
        
        piece = self.board[self.prev_x][self.prev_y]

        #Pawn movement
        if piece[1] == 'p':
            return self.move_Pawn()

        #Bishop movement
        elif piece[1] == 'B':
            return  self.move_Bishop()

        #Rook movement
        elif piece[1] == 'R':
            return self.move_Rook()
        
        #queen movement is a combination of rook and bishop movement
        elif piece[1] == 'Q':
            if self.move_Bishop() or self.move_Rook():
                return True

        elif piece[1] == 'K':
            return self.move_King()

        elif piece[1] == "N":
            return self.move_Knight()

        return False

    def Turn_checker():
        s
    def collision(self):
        piece = self.board[self.x][self.y]
        prev_piece = self.board[self.prev_x][self.prev_y]

        #if a valid piece is selected and chess pieces of the same color collide
        if piece != "":
            if piece[0] == prev_piece[0]:
                print("collison")
                return True
        return False

    def move_Pawn(self):
        piece = self.board[self.prev_x][self.prev_y]
        parity = 1
        #if a pawn is black
        if piece[0] == 'b':
            parity = -1
            if self.prev_x == 1:
                valid_moves = [1,2]
            else:
                valid_moves = [1]
            
        else:
            if self.prev_x == 6:
                valid_moves = [1,2]
            else:
                valid_moves = [1]

        print(valid_moves)

        for i in range(len(valid_moves)):
            #pawn up movement
            if (self.prev_x - (parity * valid_moves[i]) ) == self.x and self.y == self.prev_y and self.board[self.x][self.y] == "":
                return True

            #pawn up - right movement
            pawn_x = self.prev_x - (parity * 1)
            pawn_y = self.prev_y + (parity * 1)

            if pawn_x < 8 and pawn_y < 8:
                if pawn_x == self.x and pawn_y == self.y and self.board[pawn_x][pawn_y] != "":
                    return True
                
            #pawn up - left movement
            pawn_x = self.prev_x - (parity * 1)
            pawn_y = self.prev_y - (parity * 1)

            if pawn_x < 8 and pawn_y < 8:
                if pawn_x == self.x and pawn_y == self.y and self.board[pawn_x][pawn_y] != "":
                    return True

    def move_Rook(self):
            
        #horizontal movement
        if (self.x == self.prev_x and (self.y >= 0 and self.y <= 8) ):

            if self.y - self.prev_y > 0:
                print("going right")
                for i in range(self.prev_y + 1, self.y):
                    if self.board[self.x][i] != "":
                        return False
            else:
                print("going left")
                for i in range(self.y + 1, self.prev_y):
                    if self.board[self.x][i] != "":
                        return False

            return True
                
        #vertical movement
        elif (self.y == self.prev_y and (self.x >= 0 and self.x <= 8) ):
            
            #check for blocked paths
            if self.x - self.prev_x > 0:
                print("going down")
                for i in range(self.prev_x + 1, self.x):
                    if self.board[i][self.y] != "":
                        return False
            else:
                print("going up")
                for i in range(self.x + 1, self.prev_x):
                    if self.board[i][self.y] != "":
                        return False

            return True

    def move_Bishop(self):

        #Down right
        if ((self.x - self.prev_x == self.y - self.prev_y) and (self.x - self.prev_x > 0)):
            
            print("b down right move")
        
            value = self.x - self.prev_x

            for i in range(1, self.y - self.prev_y):
                print(self.prev_x + i, self.prev_y + i)
                if self.board[self.prev_x + i][self.prev_y + i] != "":
                    return False
                    
            if (value) >= 1 and (value) <= 8:
                return True
                    

        #Down left
        elif ((self.x - self.prev_x == self.prev_y - self.y) and (self.x - self.prev_x > 0)):
            print("b down left move")

            for i in range(1, self.prev_y - self.y):
                print(self.prev_x - i, self.prev_y + i)
                if self.board[self.prev_x + i][self.prev_y - i] != "":
                    return False

            value = self.x - self.prev_x
            if (value) >= 1 and (value) <= 8:
                return True

        #Up right
        elif (self.prev_x - self.x == self.y - self.prev_y):
            print("b up right move")

            for i in range(1, self.y - self.prev_y):
                print(self.prev_x - i, self.prev_y + i)
                if self.board[self.prev_x - i][self.prev_y + i] != "":
                    return False

            value = self.prev_x - self.x
            if (value) >= 1 and (value) <= 8:
                return True

        #Up left
        elif (self.prev_x - self.x == self.prev_y - self.y):
            print("b up left move")
            
            for i in range(1, self.prev_y - self.y):
                print(self.prev_x - i, self.prev_y + i)
                if self.board[self.prev_x - i][self.prev_y - i] != "":
                    return False

            value = self.prev_x - self.x
            if (value) >= 1 and (value) <= 8:
                return True

    def move_Knight(self):

        #up right - 1
        if self.x == self.prev_x - 2 and self.y == self.prev_y + 1:
            return True
        
        #up right - 2
        elif self.x == self.prev_x - 1 and self.y == self.prev_y + 2:
            return True

        #up left - 1
        elif self.x == self.prev_x - 2 and self.y == self.prev_y - 1:
            return True
        
        #up left - 2
        elif self.x == self.prev_x - 1 and self.y == self.prev_y - 2:
            return True

        #down left - 1
        elif self.x == self.prev_x + 2 and self.y == self.prev_y - 1:
            return True

        #down left - 2
        elif self.x == self.prev_x + 1 and self.y == self.prev_y - 2:
            return True

        #down right - 1
        elif self.x == self.prev_x + 2 and self.y == self.prev_y + 1:
            return True
        
        #down right - 2
        elif self.x == self.prev_x + 1 and self.y == self.prev_y + 2:
            return True

    def move_King(self):
        #up
        if self.x == self.prev_x - 1 and self.y == self.prev_y:
            return True

        #up left
        elif self.x == self.prev_x - 1 and self.y == self.prev_y - 1:
            return True
        
        #up right
        elif self.x == self.prev_x - 1 and self.y == self.prev_y + 1:
            return True
        
        #left
        elif self.x == self.prev_x and self.y == self.prev_y - 1:
            return True
        
        #right
        elif self.x == self.prev_x and self.y == self.prev_y + 1:
            return True
        
        #down left
        elif self.x == self.prev_x + 1 and self.y == self.prev_y - 1:
            return True

        #down
        elif self.x == self.prev_x + 1 and self.y == self.prev_y:
            return True

        #down right
        elif self.x == self.prev_x + 1 and self.y == self.prev_y + 1:
            return True
    
    def Multi_player(self):

        run = True
        clock = pygame.time.Clock()
        self.load_imgs()
        
    
        clicked_piece = None
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
                        
                        if self.board[self.x][self.y][0] == 'w' and Turns % 2 == 0:
                            print("White turn")
                            Turns+=1
                            
                        elif self.board[self.x][self.y][0] == 'b' and Turns % 2 == 1:
                            print("Black turn")
                            Turns += 1
                        else:
                            print("Please wait for your turn")
                            continue

                        selected_piece = True
                        print(self.board[self.x][self.y], "selected at pos", self.x, self.y)
                        

                #when a selected piece is dropped on a location
                elif event.type == pygame.MOUSEBUTTONUP and selected_piece == True:
                    self.y,self.x = pygame.mouse.get_pos()
                    self.x = int(self.x / sq_size)
                    self.y = int(self.y / sq_size)
                    
                    print("left at", self.x, self.y)
                    
                    #if the move is valid, move the selected piece to where the user wants to place it on the board then clear the prev piece
                    if self.valid_move_check():
                        self.board[self.x][self.y] = self.board[self.prev_x][self.prev_y]
                        self.board[self.prev_x][self.prev_y] = ""
                        
                        #update king pos if its moved to a new location
                        if self.board[self.x][self.y] == "wK":
                            self.whiteKing_pos = [self.x,self.y]
                        elif self.board[self.x][self.y] == "bK":
                            self.blackKing_pos = [self.x,self.y]
                        
                        #confirm if the opposing king is checked whenever any chess piece is moved
                        if self.is_checked():
                            print(self.board[self.x][self.y], "is checked")
                    else:
                        continue
                    
                    #if a chess piece was dropped successfully set the boolean to false
                    selected_piece = False
                    
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
    