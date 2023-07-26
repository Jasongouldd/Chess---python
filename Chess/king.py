import pygame
import os
from pawn import Piece


WIDTH, HEIGHT = 640, 640
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8

class King(Piece):
    def __init__(self, x, y, color, board,attack_squares=[],color_attack_squares=[]):
        super().__init__(x, y, color, board,attack_squares)
        self.color_attack_squares = color_attack_squares
        IMG = "{}_king.png".format(self.color)
        self.img = pygame.image.load(os.path.join("imgs", IMG))
        self.img = pygame.transform.scale(self.img, (SQUARE_WIDTH, SQUARE_HEIGHT))

    def __str__(self):
        return "The {} King is at the position {}, {}".format(self.color, self.x, self.y)

    def draw(self):
        # drawing the chess image
        return self.img

    def potential_moves(self):
        # cycling through all possible moves
        potential_moves = []

        for row in [-1,0,1]:
            row_loc = self.x + row
            if 0 <= row_loc < 7:
                for col in [-1,0,1]:
                    col_loc = self.y + col
                    if 0 <= col_loc <= 7:
                        if ((row_loc*SQUARE_WIDTH),(col_loc*SQUARE_WIDTH)) in self.color_attack_squares:
                                continue
                        else:
                            if self.board[row_loc][col_loc]=='':
                                potential_moves.append(((row_loc) * SQUARE_WIDTH, (col_loc) * SQUARE_HEIGHT))
                            elif self.board[row_loc][col_loc].color!=self.color:
                                potential_moves.append(((row_loc) * SQUARE_WIDTH, (col_loc) * SQUARE_HEIGHT))
                            else:
                                continue
                    else:
                        continue
            else:
                continue 

        return potential_moves
    
    def move(self, row, col):
        # Update the board with the new position of the piece
        self.board[self.x][self.y] = ""
        self.x = row
        self.y = col
        self.board[row][col] = self