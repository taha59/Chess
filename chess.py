import pygame
from const import *

class Move:
    def __init__(self, start, end, board, isEnpassantMove = False):
        self.prev_x = start[0]
        self.prev_y = start[1]
        self.x = end[0]
        self.y = end[1]

        self.piece_moved = board[self.prev_x][self.prev_y]
        self.piece_captured = board[self.x][self.y]
        self.pawn_promotion = False

        #set pawn promotion to true if a pawn reaches to the end of the board
        if self.piece_moved == "wp" and self.x == 0 or self.piece_moved == "bp" and self.x == 7:
            self.pawn_promotion = True

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.prev_x == other.prev_x and self.prev_y == other.prev_y and self.x == other.x and self.y == other.y
        
        return False


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

        self.ranks = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["a1", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
            
        self.images = {}
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CHESS")

        #add the unique chess pieces to moves variable
        self.chess_pieces = list(set(self.board[0])) + list(set(self.board[1])) + list(set(self.board[6])) + list(set(self.board[7]))

        self.prev_x = 0
        self.prev_y = 0
        self.x = 0
        self.y = 0
        self.whiteKing_pos = [7,4]
        self.blackKing_pos = [0,4]
        
        self.function_dic = {'p': lambda prev_x, prev_y, possible_moves : self.move_Pawn(prev_x, prev_y, possible_moves)}

        self.move_Log = []
        self.white_Turn = True
        self.enpassant_Possible = [] #loc where enpassant is possible
        

    #maps the pieces to their respective loaded image
    def load_imgs(self):
        for piece in self.chess_pieces:
            if piece != "--":
                self.images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sq_size, sq_size))

    #draws an empty board
    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("grey")]
        for r in range(8):
            for c in range(8):
                #choose color based on the cordinate pair 
                color = colors[((r+c) % 2)]
                pygame.draw.rect(self.window, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

    #loads the images of pieces onto the board
    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "--":
                    self.window.blit(self.images[self.board[r][c]], pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

    def chess_graphics(self):
        self.draw_board()
        self.draw_pieces()

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
                possible_moves.append(Move([prev_x, prev_y], [prev_x - (parity * valid_moves[i]), prev_y], self.board))

        #RIGHT CAPTURE
        if MIN_INDEX <= (prev_x - parity) <= MAX_INDEX and MIN_INDEX <= (prev_y + parity) <= MAX_INDEX and self.board[prev_x - parity][prev_y + parity][0] == enemy_color[self.board[prev_x][prev_y][0]]:
            possible_moves.append(Move([prev_x, prev_y], [prev_x - parity, prev_y + parity], self.board))

        elif [prev_x - parity,prev_y + parity] == self.enpassant_Possible:
            possible_moves.append(Move([prev_x, prev_y], [prev_x - parity, prev_y + parity], self.board, isEnpassantMove=True))

        #LEFT CAPTURE
        if  MIN_INDEX <= (prev_x - parity) <= MAX_INDEX and MIN_INDEX <= (prev_y - parity) <= MAX_INDEX and  self.board[prev_x - parity][prev_y - parity][0] == enemy_color[self.board[prev_x][prev_y][0]]:
            possible_moves.append( Move([prev_x, prev_y], [prev_x - parity, prev_y - parity], self.board))
        
        elif [prev_x - parity, prev_y - parity] == self.enpassant_Possible:
            possible_moves.append(Move([prev_x, prev_y], [prev_x - parity, prev_y - parity], self.board, isEnpassantMove=True))
    

    def move_Rook(self, prev_x, prev_y, possible_moves):
        
        enemy_color = {}
        enemy_color["w"] = "b"
        enemy_color["b"] = "w"
        
        #horizontal movement
        for i in range(prev_y + 1, 8):
            
            if self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[prev_x, i], self.board))
                break
            elif self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[prev_x, i], self.board))


    
        for i in range(prev_y - 1, -1, -1):
            
            if self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[prev_x, i], self.board))
                break
            elif self.board[prev_x][i][0] != '-' and self.board[prev_x][i][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[prev_x, i], self.board))
                
        #vertical movement
        for i in range(prev_x + 1, 8):

            if self.board[prev_x][i][0] != '-' and self.board[i][prev_y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[i, prev_y], self.board))
                break
            elif self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[i, prev_y], self.board))
            
    
        for i in range(prev_x - 1, -1, -1):

            if self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[i, prev_y], self.board))
                break
            elif self.board[i][prev_y][0] != '-' and self.board[i][prev_y][0] == self.board[prev_x][prev_y][0]:
                break

            possible_moves.append( Move([prev_x, prev_y],[i, prev_y], self.board))

    def move_Bishop(self, prev_x, prev_y, possible_moves):
        enemy_color = {}
        enemy_color["w"] = "b"
        enemy_color["b"] = "w"
      
        #Down right
        x, y = prev_x + 1, prev_y + 1

        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
            x+=1
            y+=1

        
        #Down left
        x, y = prev_x + 1, prev_y - 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
            x+=1
            y-=1

        #Up right
        x, y = prev_x - 1, prev_y + 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))

            x-=1
            y+=1
        

        #Up left
        x, y = prev_x - 1, prev_y - 1
        while(0 <= x < 8 and 0 <= y < 8):
            if self.board[x][y][0] != '-' and self.board[x][y][0] == enemy_color[self.board[prev_x][prev_y][0]]:
                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
                break
            elif self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                break
            possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))
            x-=1
            y-=1

    def move_Knight(self, prev_x, prev_y, possible_moves):

        all_knight_pos = [[prev_x - 2, prev_y + 1], [prev_x - 1, prev_y + 2], [prev_x - 2, prev_y - 1], [prev_x - 1, prev_y - 2], [prev_x + 2, prev_y - 1], [prev_x + 1, prev_y - 2], [prev_x + 2, prev_y + 1], [prev_x + 1, prev_y + 2]]

        for x,y in all_knight_pos:
            if 0 <= x < 8 and 0 <= y < 8:
                
                if self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                    continue

                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))

    def move_King(self, prev_x, prev_y, possible_moves):

        all_king_pos = [[prev_x - 1, prev_y], [prev_x - 1, prev_y - 1], [prev_x - 1, prev_y + 1], [prev_x, prev_y - 1], [prev_x, prev_y + 1], [prev_x + 1, prev_y - 1], [prev_x + 1, prev_y], [prev_x + 1, prev_y + 1]]
        
        for x,y in all_king_pos:
            if 0 <= x < 8 and 0 <= y < 8:
                
                if self.board[x][y][0] != '-' and self.board[x][y][0] == self.board[prev_x][prev_y][0]:
                    continue

                possible_moves.append( Move([prev_x, prev_y],[x, y], self.board))

    def undo_move(self):
        if len(self.move_Log) != 0:
            move = self.move_Log.pop()
            
            #reverse pawn promotion
            if move.pawn_promotion and move.x == 0:
                move.piece_moved = "wp"

            elif move.pawn_promotion and move.x == 7:
                move.piece_moved = "bp"

            self.board[move.prev_x][move.prev_y] = move.piece_moved
            self.board[move.x][move.y] = move.piece_captured

            self.white_Turn = not self.white_Turn

            if move.piece_moved == "wK":
                self.whiteKing_pos = [move.prev_x, move.prev_y]

            elif move.piece_moved == "bK":
                self.blackKing_pos = [move.prev_x, move.prev_y]
            
            if move.isEnpassantMove:
                self.board[move.x][move.y] = "--"
                self.board[move.prev_x][move.y] = move.piece_captured
                self.enpassant_Possible = [move.x, move.y]

            if move.piece_moved[1] == "p" and abs(move.prev_x - move.x) == 2:
                self.enpassant_Possible = []

    def generate_all_possible_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                turn = self.board[i][j][0]
                if (self.white_Turn == True and turn == "w") or (not self.white_Turn and turn == "b"):
                    piece = self.board[i][j]
                    #Pawn movement
                    if piece[1] == 'p':
                        self.move_Pawn(i, j, moves)

                    #Bishop movement
                    elif piece[1] == 'B':
                        self.move_Bishop(i, j, moves)

                    #Rook movement
                    elif piece[1] == 'R':
                        self.move_Rook(i, j, moves)
                    
                    #queen movement is a combination of rook and bishop movement
                    elif piece[1] == 'Q':
                        self.move_Bishop(i, j, moves)
                        self.move_Rook(i, j, moves)

                    #king movement
                    elif piece[1] == 'K':
                        self.move_King(i, j, moves)

                    #knight movement
                    elif piece[1] == 'N':
                        self.move_Knight(i, j, moves)

        return moves

    def in_check(self):
        #set kings position to either white or black depending on whos turn it is
        kingpos = self.whiteKing_pos if self.white_Turn else self.blackKing_pos

        #switch to enemy color to find all possible moves for the enemy
        self.white_Turn = not self.white_Turn
        opp_moves = self.generate_all_possible_moves()
        self.white_Turn = not self.white_Turn

        #if an enemy move targets the current player's king that means the king is in check so return true otherwise return false
        for move in opp_moves:
            if move.x == kingpos[0] and move.y == kingpos[1]:
                return True
        return False

    def get_valid_moves(self):

        temp = self.enpassant_Possible
        #generate all possible moves for current player
        moves = self.generate_all_possible_moves()

        #backwards traversal to make it easier to delete moves
        for i in range(len(moves) - 1, -1, -1):
            
            #place a chess piece for each possible move
            self.place_piece(moves[i])

            #need to switch turns back to current player since place_piece() function automatically switches the turns
            self.white_Turn = not self.white_Turn

            #remove the current player's possible moves that puts the king in check
            if self.in_check():
                moves.remove(moves[i])
            
            #switch turns back to opponents POV
            self.white_Turn = not self.white_Turn
            
            #undo the move where the chess piece was placed
            self.undo_move()

        self.enpassant_Possible = temp
        return moves
    
    def place_piece(self, move, promote_choice = "Q"):

        self.board[move.prev_x][move.prev_y] = "--"
        self.board[move.x][move.y] = move.piece_moved

        #track moves so we can undo later
        self.move_Log.append(move)

        #change turn for every move made
        self.white_Turn = not self.white_Turn

        if move.piece_moved == "wK":
            self.whiteKing_pos = [move.x, move.y]

        elif move.piece_moved == "bK":
            self.blackKing_pos = [move.x, move.y]


        if move.pawn_promotion:
            self.board[move.x][move.y] = move.piece_moved[0] + promote_choice

        if move.isEnpassantMove:
            self.board[move.prev_x][move.y] = "--"
        
        if move.piece_moved[1] == "p" and abs(move.prev_x - move.x) == 2:
            self.enpassant_Possible = [(move.prev_x + move.x)//2, move.prev_y]
        else:
            self.enpassant_Possible = []
        
    
    def Multi_player(self):
        Game_Over = False
        moves = []
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

                    print("left at", self.x, self.y)
        
                    #store all the valid moves for either black or white depending on whos turn it is
                    if not (self.prev_x is self.x and self.prev_y is self.y):
                        moves = self.get_valid_moves()

                    x = self.x
                    y = self.y

                    user_move = Move([self.prev_x, self.prev_y], [x, y], self.board)
                    
                    #if the user move is a valid move place the piece on the board
                    for i in range(len(moves)):

                        if user_move == moves[i]:

                            #if there is a pawn promotion move ask the user what they want their pawn to promote to
                            if user_move.pawn_promotion:
                                print ("PROMOTE OPTIONS: queen - Q, rook - R, knight - N, bishop - B")
                                promotion_Choice = input()
                                self.place_piece(moves[i], promotion_Choice)
                            else:
                                self.place_piece(moves[i])
                            
                            #after the current player's turn end the game if the enemy is in checkmate or stalemate
                            opp_moves = self.get_valid_moves()

                            #condition for checkmate: if there are no legal moves for the current player and the king is in check
                            #condition for stalemate: if there are no legal moves for the current player and the king is NOT in check
                            if len(opp_moves) == 0:

                                #stop running the game if the game status is either checkmate or stalemate
                                run = False
                                if self.in_check():
                                    color = {False: "Black", True: "White"}
                                    print ("Checkmate!", color[not self.white_Turn], "wins!!")
                                    
                                else:
                                    print ("Stalemate")

                                Game_Over = True

                            #if a chess piece was dropped successfully set the boolean to false
                            selected_piece = False

                        
                
                #undo when 'z' is clicked
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.undo_move()
                
                    
            #draw chess board and pieces
            self.chess_graphics()
            pygame.display.update()
            clock.tick(FPS)

            if Game_Over:
                import sys
                print ("Press any key to quit")
                sys.stdin.read(1)
        
        pygame.quit()

def main():
    s = Chess()
    s.Multi_player()


if __name__ == "__main__":
    main()
    