from PIL import Image

#...

img = Image.open('chess image.jpg')
w_pawn = Image.open('images/bB.png')
a_eight = (102, 30, 210, 158)  # Left, top, right and bottom coordinates of where the piece is pasted onto the board

battle_board = img.copy()
battle_board.paste(w_pawn, a_eight)
battle_board.show()