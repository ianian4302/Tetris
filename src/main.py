import pygame
import sys

# Importing the locals from the pygame module
from pygame.locals import *
from game import *
from const import *


pygame.init()

DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE))
game = Game(DISPLAYSURF)
rect = pygame.Rect(game.getRelPos(), (GAME_COL*BLOCK_SIZE_WIDTH, GAME_ROW*BLOCK_SIZE_HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    game.update()
    DISPLAYSURF.fill((147, 147, 147))
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), rect)
    game.draw()
    pygame.display.update()