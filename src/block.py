import pygame
import sys

from pygame.locals import *
from const import *
from utils import *

class Block(pygame.sprite.Sprite):
    def __init__(self, blockType, baseRowIdx, baseColIdx, blockShape, blockRotate, blockGroupIndex,  width, height, relPos):
        super().__init__()
        self.blockType = blockType
        self.blockShape = blockShape
        self.blockRotate = blockRotate
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx
        self.blockGroupIndex = blockGroupIndex
        self.height = height
        self.width = width
        self.relPos = relPos
        self.blink = False
        self.blinkCount = 0
        self.loadImage()
        self.updateimagePos()
    
    def blinkBlock(self):
        self.blink = True
        self.blinkTime = getCurrentTime()
        
    def setBaseIndex(self, baseRowIdx, baseColIdx):
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx
    
    def loadImage(self):
        self.image = pygame.image.load(BLOCK_RES[self.blockType])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        
    def updateimagePos(self):
        self.rect.x = self.colIdx * self.width + self.relPos[0]
        self.rect.y = self.rowIdx * self.height + self.relPos[1]
            
    def draw(self, surface):
        self.updateimagePos()
        if self.blink and self.blinkCount % 2 == 0:
            return 
        surface.blit(self.image, self.rect)
        
    def drop(self):
        self.baseRowIdx += 1
        
    def getIndex(self):
        return (int(self.rowIdx), int(self.colIdx))
    
    def getNextIndex(self):
        return (int(self.rowIdx)+1, int(self.colIdx))
    
    def isLeftBound(self):
        return self.colIdx == 0
    
    def isRightBound(self):
        return self.colIdx == GAME_COL - 1
        
    def getBlockConfigIndex(self):
        return BLOCK_SHAPE[self.blockShape][self.blockRotate][self.blockGroupIndex]
    
    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockConfigIndex()[0]
    
    @property
    def colIdx(self):
        return self.baseColIdx + self.getBlockConfigIndex()[1]
    
    def doLeft(self):
        self.baseColIdx -= 1
        
    def doRight(self):
        self.baseColIdx += 1
    
    def doRotate(self):
        self.blockRotate = (self.blockRotate + 1) % len(BLOCK_SHAPE[self.blockShape])
        
    def getNextRotateIndex(self):
        return (self.blockRotate + 1) % len(BLOCK_SHAPE[self.blockShape])
        
    def doDrop(self):
        self.baseRowIdx += 1
    
    def update(self):
        if(self.blink):
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime / 30)
            