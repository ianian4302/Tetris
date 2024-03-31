import pygame
import sys
import random

from pygame.locals import *
from block import *
from const import *
from utils import *

class BlockGroup(object):
    def GenerateBlockGroupConfig(rowIdx, colIdx):
        shapeType = random.randint(0, len(BLOCK_SHAPE)-1)
        blockType = random.randint(0, BlockType.BLOCKMAX-1)
        configList = []
        rotIndex = 0 #random.randint(0, len(BLOCK_SHAPE[shapeType])-1)
        for idx in range(len(BLOCK_SHAPE[shapeType][rotIndex])):
            config = {
                'blockType': blockType,
                'blockShape': shapeType,
                'blockRotate': rotIndex,
                'blockGroupIndex': idx,
                'rowIdx': rowIdx,
                'colIdx': colIdx,
            }
            configList.append(config)
        return configList
    
    def __init__(self, blockGroupType, width, height, blockConfigList, relPos):
        super().__init__()
        self.blocks = []
        self.time = 0
        self.blockGroupType = blockGroupType
        self.lastPressTime = {}
        self.dropSpeed = 300
        self.pressDiffTime = 10
        self.elminateTime = 0
        self.elminateRow = 0
        self.isElminating = False
        for config in blockConfigList:
            block = Block(config['blockType'], config['rowIdx'], config['colIdx'], config['blockShape'], config['blockRotate'], config['blockGroupIndex'], width, height, relPos)
            self.blocks.append(block)
            
    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
            
    def update(self):
        oldTime = self.time
        currenTime = getCurrentTime()
        diffTime = currenTime - oldTime
        if self.blockGroupType == BlockGroupState.DROP:
            if diffTime > self.dropSpeed:
                self.time = getCurrentTime()
                for block in self.blocks:
                    block.drop()
            self.keyDownHandler()
        for block in self.blocks:
            block.update()
        
        if self.IsEliminating():
            if getCurrentTime() - self.elminateTime > 500:
                tempBlocks = []
                for block in self.blocks:
                    if block.getIndex()[0] != self.elminateRow:
                        if block.getIndex()[0] < self.elminateRow:
                            block.drop()
                        tempBlocks.append(block)
                self.blocks = tempBlocks
                self.setEliminate(False)
                    
    def getBlockIndex(self):
        indexList = []
        for block in self.blocks:
            indexList.append(block.getIndex())
        return indexList
    
    def getNextBlockIndex(self):
        indexList = []
        for block in self.blocks:
            indexList.append(block.getNextIndex())
        return indexList
    
    def setBaseIndexes(self, BseRowIdx, BaseColIdx):
        for block in self.blocks:
            block.setBaseIndex(BseRowIdx, BaseColIdx)
    
    def getNextRotateBlockIndex(self):
        indexList = []
        for block in self.blocks:
            indexList.append(block.getNextRotateIndex())
        return indexList
    
    def getBlocks(self):
        return self.blocks
    
    def clearBlock(self):
        self.blocks = []
        
    def addBlock(self, block):
        self.blocks.append(block)
        
    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.lastPressTime.get(key, 0) > self.pressDiffTime:
            ret = True
        self.lastPressTime[key] = getCurrentTime()
        return ret
    
    def keyDownHandler(self):
        press = pygame.key.get_pressed()
        if press[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            b = True
            for block in self.blocks:
                if block.isLeftBound():
                    b = False
                    break
            if b:
                for block in self.blocks:
                    block.doLeft()
        elif press[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            b = True
            for block in self.blocks:
                if block.isRightBound():
                    b = False
                    break
            if b:
                for block in self.blocks:
                    block.doRight()
        if press[K_DOWN]:
            self.dropSpeed = 50
        else:
            self.dropSpeed = 300
        if press[K_UP] and self.checkAndSetPressTime(K_UP):
            for block in self.blocks:
                block.doRotate()
                
    def doEliminate(self, row):
        self.elminateTime = getCurrentTime()
        self.elminateRow = row
        self.setEliminate(True)
        elminateRow = {}
        for col in range(0, GAME_COL):
            index = (row, col)
            elminateRow[index] = 1
            
        for block in self.blocks:
            if elminateRow.get(block.getIndex()):
                block.blinkBlock()
                
    def processEliminate(self):
        hash = {}
        
        allIndex = self.getBlockIndex()
        for index in allIndex:
            hash[index] = 1
        
        for row in range(GAME_ROW-1 , -1, -1):
            full = True
            for col in range(0, GAME_COL):
                index = (row, col)
                if not hash.get(index):
                    full = False
                    break
            if full:
                self.doEliminate(row)
                return True
                
    def setEliminate(self, isEliminate):
        self.isElminating = isEliminate
    
    def IsEliminating(self):
        return self.isElminating