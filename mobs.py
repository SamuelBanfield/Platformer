import pygame
pygame.init()

def inside(point, rect):
    return rect[0] < point[0] < rect[0]+rect[2] and rect[1] < point[1] < rect[1]+rect[3]


class Mob():
    '''Player has status x, y, xdot, ydot given position within the scene and speed'''
    def __init__(self, scale, FPS):
        self.scale = scale
        self.terminalVelocity = int(25*scale/40)
        self.gravity = 2*scale/FPS
        self.landed = False
        self.facingDirection = 1
        self.jumpStrength = int(10*scale/40)
        self.collisions = []

    def __str__(self):
        return 'Mob'

    def jump(self, strength = None):
        '''provides an upwards impulse: the magnitude is jumpstrength by default'''
        if not strength:
            strength = self.jumpStrength
        self.ydot = -strength

    def checkCollision(self, block, oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight):
        '''checks what side/if a mob collided with a Block'''
        collisions = [False, False, False, False]
        if block.collisionSides[0]:
            #Checking top side of blocks
            if oldBottom <= block.top < newBottom and (block.left <= newLeft <= block.right or block.left <= newRight <= block.right):
                collisions[0] = True
        if block.collisionSides[1]:
            #Checking bottom side of blocks		
            if oldTop >= block.bottom > newTop and (block.left <= newLeft <= block.right or block.left <= newRight <= block.right):
                collisions[1] = True
        if block.collisionSides[2]:
            #Checking left side of blocks
            if oldRight <= block.left <= newRight and ((block.top <= newTop <= block.bottom or block.top <= newBottom <= block.bottom) or (newTop <= block.top <= newBottom or newTop <= block.bottom <= newBottom)):
                collisions[2] = True
        if block.collisionSides[3]:
            #Checking right side of blocks
            if oldLeft >= block.right > newLeft and ((block.top <= newTop <= block.bottom or block.top <= newBottom <= block.bottom) or (newTop <= block.top <= newBottom or newTop <= block.bottom <= newBottom)):
                collisions[3] = True
        return collisions

    def generateCollisions(self, oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level):
        '''Generates a list of collisions, and handles them'''
        mapx , mapy = int(self.x//level.scale), int(self.y//level.scale)
        for x in range(max(0,mapx-2), min(level.mapWidth, mapx+3)):
            for y in range(max(0,mapy-2), min(level.mapHeight, mapy+3)):
                if level.objectMap[x][y]:
                    block = level.objectMap[x][y]
                    collisions = self.checkCollision(block, oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight)
                    if collisions[0]:
                        self.landed = True
                        self.ydot = 0
                        self.y = block.top-self.height
                        self.collisions.append([block, 0])
                    if collisions[1]:
                        self.ydot = 0
                        self.y = block.bottom
                        self.collisions.append([block, 1])
                    if collisions[2]:
                        self.xdot = 0
                        self.x = block.left-self.width
                        self.collisions.append([block, 2])
                    if collisions[3]:
                        self.xdot = 0
                        self.x = block.right+1
                        self.collisions.append([block, 3])

    def updateImage(self):
        '''updates the image based on the direction the player is facing and whether they are landed'''
        if self.landed:
            self.image = self.landedImage
        else:
            self.image = self.jumpingImage
        if self.facingDirection == -1:
            self.image = pygame.transform.flip(self.image, True, False)