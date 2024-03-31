import pygame
import sys

from pygame.locals import *
from block import *
from const import *
from blockGroup import *

class Game(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.surface = surface
        self.fixedBlockGroup = BlockGroup(BlockGroupState.FIXED, BLOCK_SIZE_WIDTH, BLOCK_SIZE_HEIGHT, [], self.getRelPos())
        self.isGameOver = False
        self.dropBlockGroup = None
        self.nextBlockGroup = None
        self.scoreFont = pygame.font.Font(None, 36)
        self.score = 0
        self.gmaeOverImage = pygame.image.load(GAMEOVER)
        self.gmaeOverImage = pygame.transform.scale(self.gmaeOverImage, (320, 160))
        self.Icon = pygame.image.load(ICON)
        pygame.display.set_icon(self.Icon)
        pygame.display.set_caption(GAMENAME)
        self.generateNextBlockGroup()
        
    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0, GAME_COL/2-1)
        self.generateNextBlockGroup()
    
    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, GAME_COL+3)
        self.nextBlockGroup = BlockGroup(BlockGroupState.DROP, BLOCK_SIZE_WIDTH, BLOCK_SIZE_HEIGHT, conf, self.getRelPos())
    
    def draw(self):
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        self.nextBlockGroup.draw(self.surface)
        if self.isGameOver:
            rect = self.gmaeOverImage.get_rect()
            rect.center = (GAME_WIDTH_SIZE/2, GAME_HEIGHT_SIZE/2)
            self.surface.blit(self.gmaeOverImage, rect) 
        scoreText = self.scoreFont.render('Score: %d' % self.score, True, (0, 0, 0))
        self.surface.blit(scoreText, (50, 20))
    
    def getRelPos(self):
        return (GAME_WIDTH_SIZE/2 - GAME_COL*BLOCK_SIZE_WIDTH/2, 16)

    def willCollide(self):
        hash = {}
        allIndex = self.fixedBlockGroup.getBlockIndex()
        for index in allIndex:
            hash[index] = 1
            
        dropIndexes = self.dropBlockGroup.getNextBlockIndex()
            
        for dropIndex in dropIndexes:
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= GAME_ROW:
                return True
        return False

    def update(self):
        if self.isGameOver:
            return
        self.checkGameOver()
        self.fixedBlockGroup.update()
        if self.fixedBlockGroup.IsEliminating():
            return
        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()
        
        if self.willCollide():
            blocks = self.dropBlockGroup.getBlocks()
            for block in blocks:
                self.fixedBlockGroup.addBlock(block)
            self.dropBlockGroup.clearBlock()
            self.dropBlockGroup = None
            if self.fixedBlockGroup.processEliminate():
                self.score += 1
            
    def checkGameOver(self):
        allIndexex = self.fixedBlockGroup.getBlockIndex()
        for index in allIndexex:
            if index[0] < 2:
                self.isGameOver = True