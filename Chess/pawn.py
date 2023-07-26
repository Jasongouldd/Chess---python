import pygame
import os

WIDTH, HEIGHT = 640, 640
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8

class Piece:
    def __init__(self, x, y, color, board,attack_squares):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.attack_squares = attack_squares

class Pawn(Piece):
    def __init__(self, x, y, color, board,attack_squares=[]):
        super().__init__(x, y, color, board,attack_squares)
        IMG = "{}_pawn.png".format(self.color)
        self.img = pygame.image.load(os.path.join("imgs", IMG))
        self.img = pygame.transform.scale(self.img, (SQUARE_WIDTH, SQUARE_HEIGHT))

    def __str__(self):
        return "One of the {} Pawn is at the position {}, {}".format(self.color, self.x, self.y)

    def draw(self):
        # drawing the chess image
        return self.img

    def potential_moves(self):
        # cycling through all possible moves
        potential_moves = []
        direction = 1 if self.color == 'B' else -1

        # Check one square forward
        if 0 <= self.x + direction <= len(self.board) and self.board[self.x + direction][self.y] == '':
            potential_moves.append(((self.x + direction) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))

            # Check two squares forward if the pawn is at its starting position
            if self.x == (1 if self.color=='B' else 6) and self.board[self.x + 2 * direction][self.y] == '':
                potential_moves.append(((self.x + 2 * direction) * SQUARE_WIDTH, self.y * SQUARE_HEIGHT))

        # Check diagonal squares for capturing pieces
        for col_offset in [-1, 1]:
            new_x = self.x + direction
            new_y = self.y + col_offset

            if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]):
                piece_at_new_pos = self.board[new_x][new_y]
                if piece_at_new_pos and piece_at_new_pos.color != self.color:
                    potential_moves.append((new_x * SQUARE_WIDTH, new_y * SQUARE_HEIGHT))
        
        return potential_moves
    
    def move(self, row, col):
        # Update the board with the new position of the piece
        self.board[self.x][self.y] = ""
        self.x = row
        self.y = col
        self.board[row][col] = self