import pygame
import os
from pawn import Piece


WIDTH, HEIGHT = 640, 640
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8

class Knight(Piece):
    def __init__(self, x, y, color, board,attack_squares=[]):
        super().__init__(x, y, color, board,attack_squares)
        IMG = "{}_knight.png".format(self.color)
        self.img = pygame.image.load(os.path.join("imgs", IMG))
        self.img = pygame.transform.scale(self.img, (SQUARE_WIDTH, SQUARE_HEIGHT))

    def __str__(self):
        return "One of the {} Knights is at the position {}, {}".format(self.color, self.x, self.y)

    def draw(self):
        # drawing the chess image
        return self.img

    def potential_moves(self):
        # cycling through all possible moves
        potential_moves = []
        
        for move in [1,-1]:
            row = self.x+move*2
            if 0<= row <=7:
                for col_move in [1,-1]:
                    col = self.y+col_move
                    
                    if 0<=col<=7:
                        if self.board[row][col]=='':
                            potential_moves.append(((row) * SQUARE_WIDTH, (col) * SQUARE_HEIGHT))
                        elif 0<=col<=7 and self.board[row][col].color != self.color:
                            potential_moves.append(((row) * SQUARE_WIDTH, (col) * SQUARE_HEIGHT))
                        else:
                            None
                    else:
                        continue
        
            else:
                continue

        for move in [1,-1]:
            col = self.y+move*2
            if 0<= col <=7:
                for row_move in [1,-1]:
                    row = self.x+row_move
                    if 0<=row<=7:
                        if self.board[row][col]=='' and 0<=row<=7:
                            potential_moves.append(((row) * SQUARE_WIDTH, (col) * SQUARE_HEIGHT))
                        elif 0<=row<=7 and self.board[row][col].color!=self.color:
                            potential_moves.append(((row) * SQUARE_WIDTH, (col) * SQUARE_HEIGHT)) 
                        else:

                            None
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