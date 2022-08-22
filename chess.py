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
                    
                    if board[x][y][0] == 'w' and Turns % 2 == 0:
                        print("White turn")
                        Turns+=1
                        
                    elif board[x][y][0] == 'b' and Turns % 2 == 1:
                        print("Black turn")
                        Turns += 1
                    else:
                        print("Please wait for your turn")
                        continue


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
            index1 = prev_x - (parity * 1)
            index2 = prev_y + (parity * 1)

            if index1 < 8 and index2 < 8:
                if board[prev_x - (parity * 1)][prev_y + (parity * 1)] != "":
                    if board[prev_x - (parity * 1)][prev_y + (parity * 1)][0] != board[prev_x][prev_y][0]:
                        if prev_x - (parity * 1) == x and prev_y + (parity * 1) == y:
                            return True
                        
            #white pawn up - left movement
            if board[prev_x - (parity * 1)][prev_y - (parity * 1)] != "":
                if board[prev_x - (parity * 1)][prev_y - (parity * 1)][0] != board[prev_x][prev_y][0]:
                    if prev_x - (parity * 1) == x and prev_y - (parity * 1) == y:
                        return True

    #Bishop movement
    if piece[1] == 'B':

        #Down right
        if (x - prev_x == y - prev_y):
            value = x - prev_x
            if (value) >= 1 and (value) <= 8:
                return collision(board[x][y], board[prev_x][prev_y])
                

        #Down left
        if (x - prev_x == prev_y - y):

            value = x - prev_x
            if (value) >= 1 and (value) <= 8:
                return collision(board[x][y], board[prev_x][prev_y])

        #Up right
        if (prev_x - x == y - prev_y):

            value = prev_x - x
            if (value) >= 1 and (value) <= 8:
                return collision(board[x][y], board[prev_x][prev_y])

        #Up left
        if (prev_x - x == prev_y - y):

            value = prev_x - x
            if (value) >= 1 and (value) <= 8:
                return collision(board[x][y], board[prev_x][prev_y])
        

    #Rook movement
    if piece[1] == 'R':

        if x == prev_x and prev_y == y:
            return False
        else:
            #horizontal movement
            if (x == prev_x and (y >= 0 and y <= 8) ):
                return collision(board[x][y], board[prev_x][prev_y])
            
            #vertical movement
            if (y == prev_y and (x >= 0 and x <= 8) ):
                return collision(board[x][y], board[prev_x][prev_y])

    return False

def Check_collisions(piece, x, y, prev_x, prev_y, type_movement):
    s
def collision(piece, prev_piece):
    if piece != "":
        if piece[0] != prev_piece[0]:
            return True
        else:
            return False

    return True

if __name__ == "__main__":
    main()
    