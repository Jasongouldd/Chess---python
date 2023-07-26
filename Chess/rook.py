import pygame
import os
from pawn import Piece


WIDTH, HEIGHT = 640, 640
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8
board_start = 0
board_length = 8

class Rook(Piece):
    def __init__(self, x, y, color, board,attack_squares=[]):
        super().__init__(x, y, color, board,attack_squares)
        IMG = "{}_rook.png".format(self.color)
        self.img = pygame.image.load(os.path.join("imgs", IMG))
        self.img = pygame.transform.scale(self.img, (SQUARE_WIDTH, SQUARE_HEIGHT))

    def __str__(self):
        return "One of the {} rooks is at the position {}, {}".format(self.color, self.x, self.y)

    def draw(self):
        # drawing the chess image
        return self.img

    def potential_moves(self):
        # cycling through all possible moves
        potential_moves = []

        for row in range(self.x+1,board_length):
            try:
                if self.board[row][self.y].color==self.color:
                    break
                elif self.board[row][self.y].color!=self.color:
                    potential_moves.append(((row) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))
                    break
            except:
                potential_moves.append(((row) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))

        for row in reversed(range(board_start,self.x)):
            try:
                if self.board[row][self.y].color==self.color:
                    break
                elif self.board[row][self.y].color!=self.color:
                    potential_moves.append(((row) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))
                    break
            except:
                potential_moves.append(((row) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))

        for col in range(self.y+1,board_length):
            try:
                if self.board[self.x][col].color==self.color:
                    break
                elif self.board[self.x][col].color!=self.color:
                    potential_moves.append(((self.x) * SQUARE_WIDTH, col * SQUARE_HEIGHT))
                    break
            except:
                potential_moves.append(((self.x) * SQUARE_WIDTH, col * SQUARE_HEIGHT))

        for col in reversed(range(board_start,self.y)):
            try:
                if self.board[self.x][col].color==self.color:
                    break
                elif self.board[self.x][col].color!=self.color:
                    potential_moves.append(((self.x) * SQUARE_WIDTH, col * SQUARE_HEIGHT))
                    break
            except:
                potential_moves.append(((self.x) * SQUARE_WIDTH, col * SQUARE_HEIGHT))

        return potential_moves
    
    def move(self, row, col):
        # Update the board with the new position of the piece
        self.board[self.x][self.y] = ""
        self.x = row
        self.y = col
        self.board[row][col] = self