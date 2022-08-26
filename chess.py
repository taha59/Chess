from re import S
import pygame

width = height = 512
dimension = 8
sq_size = height // dimension
images = {}
FPS = 60

#maps the pieces to their respective loaded image
def load_imgs(chess_pieces, images):
    for piece in chess_pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sq_size, sq_size))

def draw_board(window):
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for r in range(8):
        for c in range(8):
            #choose color based on the cordinate pair 
            color = colors[((r+c) % 2)]
            pygame.draw.rect(window, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def draw_pieces(window, board):
    for r in range(8):
        for c in range(8):
            if board[r][c] != "":
                window.blit(images[board[r][c]], pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def chess_graphics(window, board):
    draw_board(window)
    draw_pieces(window, board)

def main():

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

    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CHESS")

    #add the unique chess pieces to chess_pieces variable
    chess_pieces = list(set(board[0])) + list(set(board[1])) + list(set(board[6])) + list(set(board[7]))

    run = True
    clock = pygame.time.Clock()
    load_imgs(chess_pieces, images)
    
 
    clicked_piece = None
    selected_piece = False

    Turns = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                y,x = pygame.mouse.get_pos()
                x = int(x / sq_size)
                y = int(y / sq_size)

                prev_x = x
                prev_y = y

                if board[x][y] != "":
                    
                    # if board[x][y][0] == 'w' and Turns % 2 == 0:
                    #     print("White turn")
                    #     Turns+=1
                        
                    # elif board[x][y][0] == 'b' and Turns % 2 == 1:
                    #     print("Black turn")
                    #     Turns += 1
                    # else:
                    #     print("Please wait for your turn")
                    #     continue


                    clicked_piece = images[board[x][y]]
                    selected_piece = True
                    print(board[x][y], "selected at pos", x, y)

            
            elif clicked_piece != None and event.type == pygame.MOUSEBUTTONUP and selected_piece == True:
                y,x = pygame.mouse.get_pos()
                x = int(x / sq_size)
                y = int(y / sq_size)
                
                print("left at", x, y)
                
                #if the move is valid, move the selected piece to where the user wants to place it on the board then clear the prev piece
                if valid_move_check(board, prev_x, prev_y, x, y) == True:
                    board[x][y] = board[prev_x][prev_y]
                    board[prev_x][prev_y] = ""

                selected_piece = False



                
        #draw chess board and pieces
        chess_graphics(window, board)
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

def valid_move_check(board, prev_x, prev_y, x, y):

    #if collision detected its not a valid move
    if collision(board[x][y], board[prev_x][prev_y]) == True:
        return False
    
    piece = board[prev_x][prev_y]
    parity = 1

    #Pawn movement
    if piece[1] == 'p':

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

        print(valid_moves)

        for i in range(len(valid_moves)):
            #white pawn up movement
            if (prev_x - (parity * valid_moves[i]) ) == x and y == prev_y and board[x][y] == "":
                return True

            #white pawn up - right movement
            pawn_x = prev_x - (parity * 1)
            pawn_y = prev_y + (parity * 1)

            if pawn_x < 8 and pawn_y < 8:
                if pawn_x == x and pawn_y == y and board[pawn_x][pawn_y] != "":
                    return True
            
            #white pawn up - left movement
            pawn_x = prev_x - (parity * 1)
            pawn_y = prev_y - (parity * 1)

            if pawn_x < 8 and pawn_y < 8:
                if pawn_x == x and pawn_y == y and board[pawn_x][pawn_y] != "":
                    return True

    #Bishop movement
    if piece[1] == 'B':
        return  move_Bishop(board, x, y, prev_x, prev_y)

    #Rook movement
    if piece[1] == 'R':
        return move_Rook(board, x, y, prev_x, prev_y)
    
    if piece[1] == 'Q':
        if move_Bishop(board, x, y, prev_x, prev_y) or move_Rook(board, x, y, prev_x, prev_y):
            return True

    return False

def path_block_check(board, x, y, prev_x, prev_y, type_movement):
    s

def collision(piece, prev_piece):
    
    if piece != "":
        if piece[0] == prev_piece[0]:
            print("collison")
            return True
    return False

def move_Rook(board, x, y, prev_x, prev_y):
        
    #horizontal movement
    if (x == prev_x and (y >= 0 and y <= 8) ):

        if y - prev_y > 0:
            print("going right")
            for i in range(prev_y + 1, y):
                if board[x][i] != "":
                    return False
        else:
            print("going left")
            for i in range(y + 1, prev_y):
                if board[x][i] != "":
                    return False

        return True
            
    #vertical movement
    elif (y == prev_y and (x >= 0 and x <= 8) ):

        if x - prev_x > 0:
            print("going down")
            for i in range(prev_x + 1, x):
                if board[i][y] != "":
                    return False
        else:
            print("going up")
            for i in range(x + 1, prev_x):
                if board[i][y] != "":
                    return False

        return True

def move_Bishop(board, x, y, prev_x, prev_y):

    #Down right
    if ((x - prev_x == y - prev_y) and (x - prev_x > 0)):
        
        print("b down right move")
    
        value = x - prev_x

        for i in range(1, y - prev_y):
            print(prev_x + i, prev_y + i)
            if board[prev_x + i][prev_y + i] != "":
                return False
                
        if (value) >= 1 and (value) <= 8:
            return True
                

    #Down left
    elif ((x - prev_x == prev_y - y) and (x - prev_x > 0)):
        print("b down left move")

        for i in range(1, prev_y - y):
            print(prev_x - i, prev_y + i)
            if board[prev_x + i][prev_y - i] != "":
                return False

        value = x - prev_x
        if (value) >= 1 and (value) <= 8:
            return True

    #Up right
    elif (prev_x - x == y - prev_y):
        print("b up right move")

        for i in range(1, y - prev_y):
            print(prev_x - i, prev_y + i)
            if board[prev_x - i][prev_y + i] != "":
                return False

        value = prev_x - x
        if (value) >= 1 and (value) <= 8:
            return True

    #Up left
    elif (prev_x - x == prev_y - y):
        print("b up left move")
        
        for i in range(1, prev_y - y):
            print(prev_x - i, prev_y + i)
            if board[prev_x - i][prev_y - i] != "":
                return False

        value = prev_x - x
        if (value) >= 1 and (value) <= 8:
            return True

def move_Knight(board, x, y, prev_x, prev_y):
    s

def move_King(board, x, y, prev_x, prev_y):
    s
    
if __name__ == "__main__":
    main()
    