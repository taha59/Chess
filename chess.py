import pygame

width = height = 512
dimension = 8
sq_size = height // dimension

FPS = 60
def load_imgs(chess_pieces, images, sq_size):
    for piece in chess_pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sq_size, sq_size))

def draw_board(window):
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for r in range(8):
        for c in range(8):
            #choose color based on if the cord pair 
            color = colors[((r+c) % 2)]
            pygame.draw.rect(window, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


def draw_pieces(window, board):
    j = 1

def chess_graphics(window, board):
    draw_board(window)
    draw_pieces(window, board)

def main():

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

    width = height = 512
    dimension = 8
    sq_size = height // dimension
    max_fps = 15
    images = {}

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CHESS")

    #add the unique chess pieces to chess_pieces variable
    chess_pieces = list(set(board[0])) + list(set(board[1])) + list(set(board[6])) + list(set(board[7]))

    run = True
    clock = pygame.time.Clock()
    load_imgs(chess_pieces, images, sq_size)
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        chess_graphics(window,board)
        clock.tick(FPS)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
    