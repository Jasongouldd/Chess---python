# Importing chess classes and pygame
import pygame
import os
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from king import King
from queen import Queen

pygame.init()

#Setting display window
WIDTH, HEIGHT = 640, 640
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess!!!")

game_outcome_font = pygame.font.SysFont("comicsans", 70)

# game variables
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8
board_start = 0
board_length = 8

FPS = 10
WHITE = (255,255,255)
BLUE = (0,0,255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Setting piece arrangement on the board
board = [['BR','BN','BB','BQ','BK','BB','BN','BR'],
         ['BP','BP','BP','BP','BP','BP','BP','BP'],
         ['','','','','','','',''],
         ['','','','','','','',''],
         ['','','','','','','',''],
         ['','','','','','','',''],
         ['WP','WP','WP','WP','WP','WP','WP','WP'],
         ['WR','WN','WB','WQ','WK','WB','WN','WR']]

# Putting the tiles on the board
board_setup = []
for row in range(board_length):
    for column in range(board_length):
        if row % 2 == 0 and column %2 !=0:
            board_setup.append((row*SQUARE_HEIGHT,column*SQUARE_WIDTH,BLUE))
        elif row % 2 == 0 and column %2 ==0:
            board_setup.append((row*SQUARE_HEIGHT,column*SQUARE_WIDTH,GREEN))
        elif row % 2 != 0 and column %2 !=0:
            board_setup.append((row*SQUARE_HEIGHT,column*SQUARE_WIDTH,GREEN))
        elif row % 2 != 0 and column %2 ==0:
            board_setup.append((row*SQUARE_HEIGHT,column*SQUARE_WIDTH,BLUE))        

# initializing classes for each piece
for row in range(board_length):
    for column in range(board_length):
        if board[row][column]=='BP' or board[row][column]=='WP':
            BR = Pawn(row, column, board[row][column][0],board)
            board[row][column] = BR  

        elif board[row][column]=='BR' or board[row][column]=='WR':
            BR = Rook(row, column, board[row][column][0],board)
            board[row][column] = BR  

        elif board[row][column]=='BN' or board[row][column]=='WN':
            BR = Knight(row, column, board[row][column][0],board)
            board[row][column] = BR  

        elif board[row][column]=='BB' or board[row][column]=='WB':
            BR = Bishop(row, column, board[row][column][0],board)
            board[row][column] = BR  

        elif board[row][column]=='BQ' or board[row][column]=='WQ':
            BR = Queen(row, column, board[row][column][0],board)
            board[row][column] = BR  

        elif board[row][column]=='BK' or board[row][column]=='WK':
            BR = King(row, column, board[row][column][0],board)
            board[row][column] = BR  

        else:
            continue


def display_window(highlight_moves):
# displaying window
    WIN.fill(WHITE)
    
    for x in board_setup:
        pygame.draw.rect(WIN,x[2],[x[0],x[1],SQUARE_WIDTH,SQUARE_HEIGHT])
    
    for x in highlight_moves:
        pygame.draw.rect(WIN,ORANGE,[x[1],x[0],SQUARE_WIDTH,SQUARE_HEIGHT])
    
    for row in range(board_length):
        for column in range(board_length):
            if board[row][column] =="":
                continue
            else:
                piece = board[row][column]
                draw = piece.draw()
                WIN.blit(draw,(column*SQUARE_HEIGHT,row*SQUARE_WIDTH))

    pygame.display.update()

def highlight(board, row, column,Turn,white_attack_squares, black_attack_squares):
# Checking for potential moves   
    selected_piece = board[row][column]
    if selected_piece.color == Turn:
        try:
            if isinstance(selected_piece, King):
                squares_add = white_attack_squares if Turn == 'B' else black_attack_squares
                selected_piece.color_attack_squares = squares_add
                highlight_moves = selected_piece.potential_moves()
                return highlight_moves
            else:
                highlight_moves = selected_piece.potential_moves()
                return highlight_moves
        except:
            highlight_moves = []
            return highlight_moves
    else:
        return []

def checkmate(selected_piece,row, column, Turn, white_attack_squares, black_attack_squares,last_piece_grid,position,last_piece):
# Checking for moves that stop check    
    if isinstance(selected_piece, King):
        highlight_moves = highlight(board, row, column,Turn,white_attack_squares, black_attack_squares)
        return highlight_moves
    else:
        highlight_moves = highlight(board, row, column,Turn,white_attack_squares, black_attack_squares)
        for x in highlight_moves[:]:
            if x!= last_piece_grid:
                selected_piece.move(int(x[0]/SQUARE_WIDTH),int(x[1]/SQUARE_HEIGHT)) 
                            
                if position in last_piece.potential_moves():
                    selected_piece.move(row, column)
                    highlight_moves.remove(x)
                else:
                    selected_piece.move(row, column)
                    continue
            else:
                continue
        return highlight_moves

def final_check(selected_piece, position, highlight_moves, Turn,board,row,column):
#Check to make sure moves don't move own king into check   
    for rows in range(board_start,board_length):
        for cols in range(board_start,board_length):
            check_piece = board[rows][cols]
            if check_piece == "":
                continue
            elif check_piece.color == Turn:
                continue
            else:
                for x in highlight_moves[:]:
                    st1 = int(x[0]/SQUARE_WIDTH)
                    st2 = int(x[1]/SQUARE_HEIGHT)
                    store = board[st1][st2]
                    selected_piece.move(st1,st2)
                    attack = check_piece.potential_moves()
                    if position in attack:
                        highlight_moves.remove(x)
                        selected_piece.move(row,column)
                        board[st1][st2]=store
                    else:
                        selected_piece.move(row,column)
                        board[st1][st2]=store
    
    return highlight_moves

def result(Turn):
#Printing result if there is a checkmate   
    final = "White Wins!!!" if Turn=='B' else 'Black Wins!!!!'
    draw_text_line1 = game_outcome_font.render(final, 1, WHITE)

    line1_x = WIDTH / 2 - draw_text_line1.get_width() / 2
    line1_y = HEIGHT / 2 - draw_text_line1.get_height() / 2
    
    WIN.blit(draw_text_line1, (line1_x, line1_y))
    pygame.display.update()

def main():
#Running the game
    run = True
    clock = pygame.time.Clock()
    highlight_moves = []
    Flag = True
    selected_piece = None
    Turn = 'W'
    black_attack_squares = []
    white_attack_squares = []
    check = False
    W_king_position = (7*SQUARE_HEIGHT,4*SQUARE_WIDTH)
    B_king_position = (0*SQUARE_HEIGHT,4*SQUARE_WIDTH)
    last_piece = None


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            Flag = True
            pos = pygame.mouse.get_pos()
            column = int(pos[0] // (SQUARE_WIDTH))
            row = int(pos[1] // (SQUARE_WIDTH))

            # Moving piece if move is in highlighted_moves
            if selected_piece and (row*SQUARE_WIDTH, column*SQUARE_HEIGHT) in highlight_moves:
            
                if board[row][column]!="":
                    # updating squares underthreat (for king)
                    if Turn == 'B':
                        for x in board[row][column].attack_squares:
                            white_attack_squares.remove(x)
                        selected_piece.move(row, column)
                    else:
                        for x in board[row][column].attack_squares:
                            black_attack_squares.remove(x)
                        selected_piece.move(row, column)
                
                else:
                    if isinstance(selected_piece, King):
                        selected_piece.move(row, column)
                        if Turn == 'B':
                            B_king_position = (row*SQUARE_WIDTH,column*SQUARE_HEIGHT)
                        else:
                            W_king_position = (row*SQUARE_WIDTH, column*SQUARE_HEIGHT)
                    else:
                        selected_piece.move(row, column)

                if Turn == 'B':
                    for x in board[row][column].attack_squares:
                        black_attack_squares.remove(x)

                    attack_moves = selected_piece.potential_moves()
                    black_attack_squares += attack_moves
                    board[row][column].attack_squares = attack_moves
                
                else:
                    for x in board[row][column].attack_squares:
                        white_attack_squares.remove(x)

                    attack_moves = selected_piece.potential_moves()
                    white_attack_squares += attack_moves
                    board[row][column].attack_squares = attack_moves

                Turn = 'B' if selected_piece.color =='W' else 'W'
                last_piece = board[row][column]
                selected_piece = None
                highlight_moves = []
                display_window(highlight_moves)

                #checking to see if it is checkmate
                if B_king_position in attack_moves:
                    check = True
                    moves = 0
                    last_piece_grid = (last_piece.x*SQUARE_WIDTH, last_piece.y*SQUARE_HEIGHT)
                    position = W_king_position if Turn=='W' else B_king_position
                    for row in range(0,8):
                        for column in range(0,8):
                            selected_piece = board[row][column]
                            if selected_piece == "":
                                continue
                            elif selected_piece.color != Turn:
                                continue
                            else:
                                selected_piece = board[row][column]
                                highlight_moves = checkmate(selected_piece,row, column, Turn, white_attack_squares, 
                                            black_attack_squares,last_piece_grid,position,last_piece)
                                highlight_moves = final_check(selected_piece, position, highlight_moves, Turn,board,row,column)
                                moves += len(highlight_moves)

                    if moves==0:
                        result(Turn)
                        pygame.time.delay(4000)
                        pygame.quit()
                    else:
                        None

                elif W_king_position in attack_moves:
                    check = True
                    moves = 0
                    last_piece_grid = (last_piece.x*SQUARE_WIDTH, last_piece.y*SQUARE_HEIGHT)
                    position = W_king_position if Turn=='W' else B_king_position
                    for row in range(0,8):
                        for column in range(0,8):
                            selected_piece = board[row][column]
                            if selected_piece == "":
                                continue
                            elif selected_piece.color != Turn:
                                continue
                            else:
                                selected_piece = board[row][column]
                                highlight_moves = checkmate(selected_piece,row, column, Turn, white_attack_squares, 
                                            black_attack_squares,last_piece_grid,position,last_piece)
                                highlight_moves = final_check(selected_piece, position, highlight_moves, Turn,board,row,column)
                                moves += len(highlight_moves)

                    if moves==0:
                        result(Turn)
                        pygame.time.delay(4000)
                        pygame.quit()
                    else:
                        None
                        
                else:
                    check = False

            #seeing the potential moves of selected piece if in check
            elif check:
                last_piece_grid = (last_piece.x*SQUARE_WIDTH, last_piece.y*SQUARE_HEIGHT)
                selected_piece = board[row][column]
                position = W_king_position if Turn=='W' else B_king_position
                highlight_moves = checkmate(selected_piece,row, column, Turn, white_attack_squares, 
                                            black_attack_squares,last_piece_grid,position,last_piece)
            
                highlight_moves = final_check(selected_piece, position,highlight_moves,Turn, board,row,column)

            #seeing the potential moves of selected piece  
            else:
                selected_piece = board[row][column]
                highlight_moves = highlight(board, row, column,Turn,white_attack_squares, black_attack_squares)
                position = W_king_position if Turn=='W' else B_king_position
                highlight_moves = final_check(selected_piece, position,highlight_moves,Turn, board,row,column)

        if Flag:
            display_window(highlight_moves)
            Flag = False
    
    pygame.quit()

if __name__ == "__main__":
    main()