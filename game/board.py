import pygame
from .constants import BROWN,ROWS,COLS,BAMBOO,SQUARE_SIZE ,WHITE,BLACK

class Board:
    def __init__(self, pos):
        pass
    
    def draw_squares(self, win):
        win.fill(BAMBOO)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BROWN, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        pygame.display.update()