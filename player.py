import pygame, mobs
pygame.init()

emptyBlockImage = pygame.image.load('images/emptyQuestionBlock.png') #empty block image needed for comparison

class Player(mobs.Mob):
    def __init__(self, scale, FPS, x, y):
        mobs.Mob.__init__(self, scale, FPS)
        self.x, self.y = x, y
        self.width = 30
        self.height = int(1.5*self.scale)
        self.xdot = 0
        self.ydot = 0
        self.deaths = 0
        self.speed = 2
        self.friction = 0.8 #slow down on the ground, bigger is less slow down
        self.airfriction = 0.9 #slow down in the air, bigger is less slow down
        self.startx, self.starty = x, y
        self.jumpStrength = int(27*self.scale/40)
        self.landedImage = pygame.image.load('images/newChar.png')
        self.jumpingImage = pygame.image.load('images/newCharJumping.png')
        self.image = self.landedImage

    def reset(self, level):
        '''Reset on death or hitting the flagpole'''
        self.x, self.y = self.startx, self.starty
        self.xdot, self.ydot = 0, 0
        level.reset()

    def mobCollisions(self, newTop, newBottom, newLeft, newRight, level):
        '''Checks if the new player position collides with any mobs'''
        for mob in level.mobs:
            if ((newTop <= mob.top < newBottom) or  (newTop <= mob.bottom < newBottom)) and ((mob.left <= newLeft <= mob.right) or  (mob.left <= newRight < mob.right)):
                if newBottom < mob.top+(mob.height//2) or newBottom-self.ydot < mob.top:
                    self.jump(15)
                    level.mobs.remove(mob)
                else:
                    self.deaths += 1
                    self.reset(level)

    def update(self, level):
        '''Update of the player is called every game tick'''
        self.collisions = []
        if self.landed:
            self.xdot *= self.friction
        else:
            self.xdot *= self.airfriction
        self.landed = False

        '''First moving x and checking for collsisions'''
        oldTop, oldBottom, oldLeft, oldRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.x += self.xdot
        newTop, newBottom, newLeft, newRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.generateCollisions(oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level)
        self.mobCollisions(newTop, newBottom, newLeft, newRight, level)

        '''Then moving y and checking for collsisions again'''
        oldTop, oldBottom, oldLeft, oldRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.ydot += self.gravity
        if (self.ydot**2)**0.5 > self.terminalVelocity: self.ydot = self.ydot/(self.ydot**2)**0.5*self.terminalVelocity
        self.y += self.ydot
        newTop, newBottom, newLeft, newRight = self.y, self.y+self.height-1, self.x, self.x+self.width-1
        self.generateCollisions(oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level)
        self.mobCollisions(newTop, newBottom, newLeft, newRight, level)
        
        '''Checking for deaths by falling of the bottom of the map'''
        if self.y>level.imageHeight+level.scale*5:
            self.reset(level)
            self.deaths += 1

        '''Handling all the collisions'''
        deadlyCollision = False
        for collision in self.collisions:
            '''Checking for collisions with the spike block'''
            if collision[0].type == 'deadlyBlock':
                deadlyCollision = True
                self.deaths += 1
            '''Checking for level completion'''
            if collision[0].type in ['flag', 'flagPole']:
                level.complete = True
            '''Changing the coin block image when it is hit from below, could also implement a coin score here'''
            if collision[0].type == 'questionBlock' and collision[0].image != emptyBlockImage  and collision[1] == 1:
                collision[0].image = emptyBlockImage
                level.updateImage()
            '''Breaking bricks on collision from below'''
            if collision[0].type == 'brick' and collision[1] == 1:
                level.objectMap[collision[0].mapx][collision[0].mapy] = None
                level.objects.remove(collision[0])
                level.updateImage()
        '''Resetting if collision with spikeblock detected'''
        if deadlyCollision:
            self.reset(level)

    def __str__(self):
        return 'Player'

