import pygame, mobs
pygame.init()

enemyImages = {
    "CannonBall": pygame.image.load('images/cannonBall.png'),
    "Goomba": pygame.image.load('images/enemy1.png'),
    "SmartGoomba": pygame.image.load('images/smartGoomba.png')
}

class Enemy(mobs.Mob):
    def __init__(self, x, y, scale, FPS, scene):
        mobs.Mob.__init__(self, scale, FPS)
        self.x, self.y = x, y
        self.width, self.height = 40, 40
        self.top, self.bottom, self.left, self.right = self.y, self.y + self.height - 1, self.x, self.x + self.width - 1
        self.landedImage = self.jumpingImage = enemyImages[self.type] # No difference between jumping and standard image for enemies
        self.collisionSides = [True, True, True, True]
        self.image = self.landedImage
        self.scene = scene
        self.facingDirection = -1

    def physicsUpdate(self, level, gravity):
        '''checks for collisions between the mob and all blocks in two stages'''
        self.landed = False
        self.collisions = []

        oldTop, oldBottom, oldLeft, oldRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.x += self.xdot
        self.xdot *= 0.5
        newTop, newBottom, newLeft, newRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.generateCollisions(oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level)
        
        oldTop, oldBottom, oldLeft, oldRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        if gravity:
            self.ydot += self.gravity
        if (self.ydot**2)**0.5 > self.terminalVelocity: self.ydot = self.ydot/(self.ydot**2)**0.5*self.terminalVelocity
        self.y += self.ydot
        newTop, newBottom, newLeft, newRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.generateCollisions(oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level)
        self.top, self.bottom, self.left, self.right = self.y, self.y+self.height, self.x, self.x+self.width

        # Turning around when hitting a wall is part of the physicsUpdate
        for collision in self.collisions:
            if collision[1] == 2:
                self.facingDirection = -1
                self.xdot = 0
            if collision[1] == 3:
                self.facingDirection = 1
                self.xdot = 0

    def __str__(self):
        return self.type

class CannonBall(Enemy):
    def __init__(self, scale, FPS, x, y, scene):
        self.speed = 5
        self.xdot, self.ydot = self.speed, 0
        self.type = 'CannonBall'
        Enemy.__init__(self, x, y, scale, FPS, scene)

    def update(self, level):
        if self.y > level.imageHeight + level.scale * 5 or self.x < -self.width:
            level.mobs.remove(self)
        self.xdot = self.speed * self.facingDirection
        self.physicsUpdate(level, False)
        if len(self.collisions) != 0:
            level.mobs.remove(self)

class Goomba(Enemy):
    def __init__(self, scale, FPS, x, y, scene):
        self.speed = 2
        self.xdot, self.ydot = 3, 0
        self.type = 'Goomba'
        Enemy.__init__(self, x, y, scale, FPS, scene)

    def update(self, level):
        if self.y>level.imageHeight+level.scale*5 or self.x<-self.width:
            level.mobs.remove(self)
        self.xdot = self.speed*self.facingDirection
        self.physicsUpdate(level, True)

class SmartGoomba(Enemy):
    def __init__(self, scale, FPS, x, y, scene):
        self.speed = 2
        self.xdot, self.ydot = 0, 0
        self.type = 'SmartGoomba'
        Enemy.__init__(self, x, y, scale, FPS, scene)

    def update(self, level):
        '''a custom update function that also prevents smart goombas from walking of edges'''
        self.collisions = []
        self.physicsUpdate(level, True)
        if self.y > level.imageHeight + level.scale * 5 or self.x < -self.width:
            level.mobs.remove(self)
        mapPosition = [
            int(self.x + (self.width // 2)) // level.scale,
            int(self.y + (self.height // 2)) // level.scale
        ]
        try:
            self.xdot = self.speed*self.facingDirection
            if (level.map[mapPosition[0]+1][mapPosition[1]+1] in ['.','x','<','>'] and level.map[mapPosition[0]-1][mapPosition[1]+1] in ['.','x','<','>']):
                self.xdot = 0
            if level.map[mapPosition[0]+1][mapPosition[1]+1] in ['.','x','<','>'] and self.facingDirection == 1:
                if self.landed and (self.right%level.scale) >= level.scale-self.speed:
                    self.facingDirection = -1
            if level.map[mapPosition[0]-1][mapPosition[1]+1] in ['.','x','<','>'] and self.facingDirection == -1:
                if self.landed and (self.left%level.scale) <= self.speed:
                    self.facingDirection = 1
        except:
            # Walking of the edge of the map gives an index error.
            pass