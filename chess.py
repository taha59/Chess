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

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                x = int(x / sq_size)
                y = int(y / sq_size)

                prev_x = x
                prev_y = y

                if board[y][x] != "":
                    clicked_piece = images[board[y][x]]
                    print(board[y][x], "selected at pos", x, y)

            
            elif clicked_piece != None and event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                x = int(x / sq_size)
                y = int(y / sq_size)
                
                #move the selected piece to where the user wants to place it on the board then clear the prev piece
                board[y][x] = board[prev_y][prev_x]
                board[prev_y][prev_x] = ""

                print("let goo",x, y)
                
        #draw chess board and pieces
        chess_graphics(window, board)
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
    