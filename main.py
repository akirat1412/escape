import tkinter as tk
from piece import Piece
from tkinter import font as tkfont
from PIL import ImageTk, Image


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Escape Game')
        self.root.geometry('500x650+200+100')

        board_image = tk.PhotoImage(file='images/Board.png')

        self.canvas = tk.Canvas(self.root, width=450, height=550)
        self.canvas.place(x=25, y=75)
        self.canvas.bind('<Button-1>', self.interact)
        self.canvas.bind('<KeyPress>', self.move)
        self.canvas.focus_set()
        self.canvas.create_image(0, 0, image=board_image, anchor='nw')

        self.piece_images = []
        self.selection_images = []
        self.load_piece_images()

        self.pieces = []
        self.board = []
        self.selection = None
        self.new_game()

        self.reset_button = tk.Button(self.root, text='Reset', bd=1, command=self.new_game, font=tkfont.Font(size=18))
        self.reset_button.place(x=50, y=20)
        self.status_text = tk.StringVar()
        self.status_text.set('')
        status_label = tk.Label(self.root, textvariable=self.status_text, font=tkfont.Font(size=18))
        status_label.place(x=300, y=25)

        self.root.mainloop()

    def load_piece_images(self):
        piece_image = Image.open('images/Piece.png')
        main_piece_image = Image.open('images/Main Piece.png')
        selection_image = Image.open('images/Red.png')

        self.piece_images.append(ImageTk.PhotoImage(piece_image.resize((90, 90), Image.ANTIALIAS)))
        self.piece_images.append(ImageTk.PhotoImage(piece_image.resize((190, 90), Image.ANTIALIAS)))
        self.piece_images.append(ImageTk.PhotoImage(piece_image.resize((90, 190), Image.ANTIALIAS)))
        self.piece_images.append(ImageTk.PhotoImage(main_piece_image.resize((190, 190), Image.ANTIALIAS)))
        self.selection_images.append(ImageTk.PhotoImage(selection_image.resize((110, 110), Image.ANTIALIAS)))
        self.selection_images.append(ImageTk.PhotoImage(selection_image.resize((210, 110), Image.ANTIALIAS)))
        self.selection_images.append(ImageTk.PhotoImage(selection_image.resize((110, 210), Image.ANTIALIAS)))
        self.selection_images.append(ImageTk.PhotoImage(selection_image.resize((210, 210), Image.ANTIALIAS)))

    def new_game(self):
        self.canvas.delete('reset')

        self.pieces = []
        self.pieces.append(Piece(1, 0, 2, 2, self.piece_images[3], self.selection_images[3]))
        self.pieces.append(Piece(0, 0, 1, 2, self.piece_images[2], self.selection_images[2]))
        self.pieces.append(Piece(3, 0, 1, 2, self.piece_images[2], self.selection_images[2]))
        self.pieces.append(Piece(0, 3, 1, 2, self.piece_images[2], self.selection_images[2]))
        self.pieces.append(Piece(3, 3, 1, 2, self.piece_images[2], self.selection_images[2]))
        self.pieces.append(Piece(1, 2, 2, 1, self.piece_images[1], self.selection_images[1]))
        self.pieces.append(Piece(1, 3, 1, 1, self.piece_images[0], self.selection_images[0]))
        self.pieces.append(Piece(2, 3, 1, 1, self.piece_images[0], self.selection_images[0]))
        self.pieces.append(Piece(1, 4, 1, 1, self.piece_images[0], self.selection_images[0]))
        self.pieces.append(Piece(2, 4, 1, 1, self.piece_images[0], self.selection_images[0]))

        self.board = [[True for _ in range(5)] for _ in range(4)]
        self.board[0][2] = False
        self.board[3][2] = False

        self.selection = None
        for piece in self.pieces:
            self.render_piece(piece)

    def render_piece(self, piece):
        self.canvas.create_image(100 * piece.x + 30, 100 * piece.y + 30,
                                 image=piece.image, anchor='nw', tags=('reset', f'p{piece.x}{piece.y}'))

    def render_selection(self):
        self.canvas.delete('selection')
        self.canvas.create_image(100 * self.selection.x + 20, 100 * self.selection.y + 20,
                                 image=self.selection.selection, anchor='nw', tags=('reset', 'selection'))
        self.render_piece(self.selection)

    def interact(self, event):
        x = (event.x - 25) // 100
        y = (event.y - 25) // 100

        for piece in self.pieces:
            if piece.x <= x < piece.x + piece.width and piece.y <= y < piece.y + piece.height:
                self.selection = piece
                self.canvas.delete(f'p{piece.x}{piece.y}')
                self.render_selection()

    def move(self, event):
        direction = event.keysym
        if direction == 'Up' or direction == 'w':
            vector = (0, -1)
        elif direction == 'Left' or direction == 'a':
            vector = (-1, 0)
        elif direction == 'Right' or direction == 'd':
            vector = (1, 0)
        elif direction == 'Down' or direction == 's':
            vector = (0, 1)
        else:
            return

        if self.check_move(vector):
            self.update_board(vector)
            piece = self.selection
            self.canvas.delete(f'p{piece.x}{piece.y}')
            piece.x += vector[0]
            piece.y += vector[1]
            self.render_selection()
            if self.pieces[0].x == 1 and self.pieces[0].y == 3:
                self.status_text.set('You Win!')

    def check_move(self, direction):
        piece = self.selection
        if direction[0] == 1:
            for block in range(piece.height):
                if self.board[piece.x + piece.width][piece.y + block]:
                    return False
        elif direction[1] == 1:
            for block in range(piece.width):
                if self.board[piece.x + block][piece.y + piece.height]:
                    return False
        elif direction[0] == -1:
            for block in range(piece.height):
                if self.board[piece.x - 1][piece.y + block]:
                    return False
        elif direction[1] == -1:
            for block in range(piece.width):
                print(f'checking ({piece.x + block}, {piece.y - 1})')
                if self.board[piece.x + block][piece.y - 1]:
                    return False
        return True

    def update_board(self, direction):
        piece = self.selection
        for x in range(piece.width):
            for y in range(piece.height):
                self.board[x + piece.x][y + piece.y] = False
        for x in range(piece.width):
            for y in range(piece.height):
                self.board[x + piece.x + direction[0]][y + piece.y + direction[1]] = True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
