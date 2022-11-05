import pygame, enemy
pygame.init()

def load(name, level):
    '''loads the level and returns the rotated matrix representation, also sets up the mobs'''
    with open('levelFiles/'+name, 'r') as levelFile:
        levelLayout = []
        line = levelFile.readline()
        while line not in ['','\n']:
            levelLayout.append(list(line))
            line = levelFile.readline()
        mobListString = levelFile.readline()
        startPositionString = levelFile.readline().split(',')
    stringList = [mob.split(',') for mob in mobListString.split()]
    level.mobData = stringList
    for mobParams in stringList:
        level.mobs.append(mobDict[mobParams[0]](level.scale, level.FPS, int(level.scale*int(mobParams[1])), int(level.scale*int(mobParams[2])), level))
    level.playerStartPosition = [int(x) for x in startPositionString]
    return flip(levelLayout)

def flip(mat):
    '''flips a 2d matrix'''
    width, height = len(mat), len(mat[0])
    newMat = []
    for x in range(height):
        newMat.append([mat[y][x] for y in range(width)])
    return newMat

def save(name, level):
    levels = []
    for lineNo in range(len(level[0])):
        s = ''
        levels.append(''.join([level[i][lineNo] for i in range(len(level))]))
    levelString = ''.join(levels)+2*'\n'+'0,0'
    with open('levelFiles/'+name+'.txt', 'w') as levelFile:
        levelFile.write(levelString)
    return

def getIndex(d,v):
    '''i = index, d = dict, v = value'''
    for i in d:
        if d[i] == v:
            return i
    print('cant find value in dict')

class Camera():
    def __init__(self, slack):
        self.slack = slack
        self.offset = [0,0]

    def __str__(self):
        return 'Camera'

    def updateOffset(self, character, screenWidth, screenHeight):
        '''ensures the character is on screen: adjusts camera position if the character is within slack of the left or right of the screen'''
        if self.offset[0] + character.x < self.slack[0]:
            self.offset[0] = int(self.slack[0]-character.x)
        if self.offset[0] + character.x + character.width > screenWidth - self.slack[0]:
            self.offset[0] = int(screenWidth-self.slack[0]-character.x-character.width)
        self.offset[1] = 0
        if self.offset[1] + character.y < self.slack[1]:
            self.offset[1] = int(self.slack[1]-character.y)
        if self.offset[1] + character.y + character.height > screenHeight - self.slack[1]:
            self.offset[1] = int(screenHeight-self.slack[1]-character.y-character.height)

class Scene():
    def __init__(self, name, scale, FPS):
        self.name = name
        self.complete = False
        self.scale = scale
        self.FPS = FPS
        self.mobData = []
        self.mobs = []
        self.spawners = []
        self.map = load(name, self)
        self.mapWidth = len(self.map)
        self.mapHeight = len(self.map[-1])
        self.objects = []
        self.resetMapObjects()
        self.updateImage()

    def __str__(self):
        return self.name

    def updateImage(self):
        '''converts the matrix representation to a pygame image'''
        self.imageWidth, self.imageHeight = self.scale*len(self.map), self.scale*len(self.map[0])
        image = pygame.Surface((self.imageWidth, self.imageHeight))
        image.fill((64,189,255))
        for block in self.objects:
            rect = block.image.get_rect()
            rect.topleft = (self.scale*block.mapx,self.scale*block.mapy)
            image.blit(block.image, rect)
        self.image = image

    def reset(self):
        '''resets the level, called when the player dies: resets coinblocks and mobs'''
        self.objects = []
        self.spawners = []
        self.resetMapObjects()
        self.updateImage()
        self.mobs = []
        for mobParams in self.mobData:
            self.mobs.append(mobDict[mobParams[0]](self.scale, self.FPS, int(self.scale*int(mobParams[1])), int(self.scale*int(mobParams[2])), self))

    def resetMapObjects(self):
        '''creates objects for collision detection'''
        self.objectMap = [[None for y in range(self.mapHeight)] for x in range(self.mapWidth)]
        for mapx in range(len(self.map)):
            for mapy in range(len(self.map[mapx])):
                if self.map[mapx][mapy] in objectDict:
                    newTile = Block(self, mapx, mapy, self.scale, objectDict[self.map[mapx][mapy]])
                    if self.map[mapx][mapy] in ['}', '{']:
                        self.spawners.append(Spawner(self.map[mapx][mapy], mapx, mapy, self.scale, self.FPS, self, newTile))
                    self.objectMap[mapx][mapy] = newTile
                    self.objects.append(newTile)

class Spawner():
    def __init__(self, direction, mapx, mapy, scale, FPS, level, newTile):
        self.startTime = -1
        self.tile = newTile
        self.timer = 150 #period between cannon firing
        self.mapx, self.mapy = mapx, mapy
        self.x, self.y = scale*self.mapx, scale*self.mapy
        self.scale, self.FPS = scale, FPS
        self.level = level
        if direction == '{':
            self.direction = -1
            self.tile.image = pygame.transform.flip(self.tile.image, True, False)
        else:
            self.direction = 1

    def update(self, player, time):
        mapx, mapy = player.x//self.scale, player.y//self.scale
        if (mapx-self.mapx)**2 < 15**2:
            if self.startTime == -1:
                self.startTime = time
            if (time-self.startTime) % self.timer == 0:
                newCannonBall = enemy.CannonBall(self.scale, self.FPS, self.x+self.direction*(self.scale), self.y, self.level)
                newCannonBall.facingDirection = self.direction
                self.level.mobs.append(newCannonBall)

    def __str__(self):
        return 'Spawner: ' + str(self.mapx) + ', ' + str(self.mapy)

class Block():
    def __init__(self, scene, mapx, mapy, scale, blockType):
        self.type = blockType
        self.image = imageDict[blockType]
        self.collisionSides = collisionSidesDict[blockType]
        self.mapx, self.mapy = mapx, mapy
        self.scene = scene
        self.scale = scale
        self.width = self.height = scale
        self.rect = [scale*mapx, scale*mapy, scale, scale]
        self.top, self.bottom, self.left, self.right = [self.mapy*self.scale, self.mapy*self.scale+self.scale-1, self.mapx*self.scale, self.mapx*self.scale+self.scale-1]

    def __str__(self):
        return 'Block, location: '+str(self.x)+', '+str(self.y)

mobDict = {
    'Goomba': enemy.Goomba,
    'SmartGoomba': enemy.SmartGoomba,
    'CannonBall': enemy.CannonBall,
}
objectDict = {
    '-': 'platform',
    '=': 'brick',
    'c': 'questionBlock',
    '<': 'cloudLeft',
    '>': 'cloudRight',
    'x': 'deadlyBlock',
    '|': 'flagPole',
    '?': 'flag',
    '1': 'castle',
    '{': 'cannon',
    '}': 'cannon'
}
imageDict = {
    'platform': pygame.image.load('images/platform.png'),
    'brick': pygame.image.load('images/brick.png'),
    'questionBlock': pygame.image.load('images/questionBlock.png'),
    'cloudLeft': pygame.image.load('images/cloudLeft.png'),
    'cloudRight': pygame.image.load('images/cloudRight.png'),
    'deadlyBlock': pygame.image.load('images/deadlyBlock.png'),
    'flagPole': pygame.image.load('images/flagPole.png'),
    'flag': pygame.image.load('images/flag.png'),
    'castle': pygame.image.load('images/castle.png'),
    'cannon': pygame.image.load('images/cannon.png'),
}
collisionSidesDict = {
    'platform': [1,0,0,0],
    'brick': [1,1,1,1],
    'questionBlock': [1,1,1,1],
    'cloudLeft': [0,0,0,0],
    'cloudRight': [0,0,0,0],
    'deadlyBlock': [1,1,1,1],
    'flagPole': [1,1,1,1],
    'flag': [1,1,1,1],
    'castle':[0,0,0,0],
    'cannon': [1,1,1,1],
}