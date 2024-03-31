GAMENAME = 'Tetris'
class BlockType:
    RED = 0
    GREEN = 1
    BLUE = 2
    ORANGE = 3
    YELLOW = 4
    PURPLE = 5
    LIGHTGREEN = 6
    NAVY = 7
    BLOCKMAX = 8

class GameState:
    RUNNING = 0
    PAUSE = 1
    GAMEOVER = 2
    
class BlockGroupState:
    FIXED = 0
    DROP = 1

BLOCK_RES = {
    BlockType.RED: 'assests/red_block.png',
    BlockType.GREEN: 'assests/green_block.png',
    BlockType.BLUE: 'assests/blue_block.png',
    BlockType.ORANGE: 'assests/orange_block.png',
    BlockType.YELLOW: 'assests/yellow_block.png',
    BlockType.PURPLE: 'assests/purple_block.png',
    BlockType.LIGHTGREEN: 'assests/lightgreen_block.png',
    BlockType.NAVY: 'assests/navy_block.png',
}

ICON = 'assests/icon.png'
GAMEOVER = 'assests/gameover.png'

BLOCK_SIZE_WIDTH = 32
BLOCK_SIZE_HEIGHT = 32

GAME_ROW = 18
GAME_COL = 10

GAME_WIDTH_SIZE = 800
GAME_HEIGHT_SIZE = 600

BLOCK_SHAPE = [
                [((0,0), (0,1), (1,0), (1,1))], # square
                [((0,0), (0,1), (0,2), (0,3)),((0,0), (1,0), (2,0), (3,0))], # line
                [((0,0), (0,1), (0,2), (1,2)),((0,0), (1,0), (2,0), (0,1)),((0,0), (1,0), (1,1), (1,2)),((2,0), (0,1), (1,1), (2,1))], # L
                [((0,0), (0,1), (0,2), (1,0)),((0,0), (1,0), (1,1), (1,2)),((0,2), (1,0), (1,1), (1,2)),((2,0), (0,1), (1,1), (2,1))], # L reverse
                [((0,0), (0,1), (0,2), (1,1)),((0,1), (1,0), (1,1), (1,2)),((1,0), (0,1), (1,1), (2,1)),((0,0), (1,0), (1,1), (2,0))], # T
                [((0,0), (0,1), (1,1), (1,2)),((0,1), (1,0), (1,1), (2,0))] # Z
            ]

# BLOCK_SHAPE = [
#                 [((0,0), (0,1), (1,0), (1,1))], # square
#             ]