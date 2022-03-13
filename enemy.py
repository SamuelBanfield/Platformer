import pygame, mobs
pygame.init()

class Enemy(mobs.Mob):
	def __init__(self, scale, FPS, scene):
		mobs.Mob.__init__(self, scale, FPS)
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

	def generateCollisions(self, oldTop, oldBottom, oldLeft, oldRight, newTop, newBottom, newLeft, newRight, level):
		'''decides which blocks need to be checked for collisions and handles the colisions'''
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
						self.facingDirection = -1
						self.collisions.append([block, 2])
					if collisions[3]:
						self.xdot = 0
						self.x = block.right+1
						self.facingDirection = 1
						self.collisions.append([block, 3])


	def __str__(self):
		return self.type

class CannonBall(Enemy):
	def __init__(self, scale, FPS, x, y, scene):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 40
		self.speed = 5
		self.xdot = self.speed
		self.ydot = 0
		self.top, self.bottom, self.left, self.right = self.y, self.y+self.height-1, self.x, self.x+self.width-1
		self.landedImage = pygame.image.load('images/cannonBall.png')
		self.jumpingImage = pygame.image.load('images/cannonBall.png')
		self.type = 'CannonBall'
		Enemy.__init__(self, scale, FPS, scene)

	def update(self, level):
		if self.y>level.imageHeight+level.scale*5 or self.x<-self.width:
			level.mobs.remove(self)
		self.xdot = self.speed*self.facingDirection
		self.physicsUpdate(level, False)
		if len(self.collisions) != 0:
			level.mobs.remove(self)

class Goomba(Enemy):
	def __init__(self, scale, FPS, x, y, scene):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 40
		self.speed = 2
		self.xdot = 3
		self.ydot = 0
		self.top, self.bottom, self.left, self.right = self.y, self.y+self.height-1, self.x, self.x+self.width-1
		self.landedImage = pygame.image.load('images/enemy1.png')
		self.jumpingImage = pygame.image.load('images/enemy1.png')
		self.type = 'Goomba'
		Enemy.__init__(self, scale, FPS, scene)

	def update(self, level):
		if self.y>level.imageHeight+level.scale*5 or self.x<-self.width:
			level.mobs.remove(self)
		self.xdot = self.speed*self.facingDirection
		self.physicsUpdate(level, True)

class SmartGoomba(Enemy):
	def __init__(self, scale, FPS, x, y, scene):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 40
		self.speed = 2
		self.xdot = 0
		self.ydot = 0
		self.top, self.bottom, self.left, self.right = self.y, self.y+self.height-1, self.x, self.x+self.width-1
		self.landedImage = pygame.image.load('images/smartGoomba.png')
		self.jumpingImage = pygame.image.load('images/smartGoomba.png')
		self.type = 'SmartGoomba'
		Enemy.__init__(self, scale, FPS, scene)

	def update(self, level):
		'''a custom update function that also prevents smart goombas from walking of edges'''
		self.collisions = []
		self.physicsUpdate(level, True)
		if self.y>level.imageHeight+level.scale*5 or self.x<-self.width:
			level.mobs.remove(self)
		mapPosition = [int(self.x+(self.width//2))//level.scale, int(self.y+(self.height//2))//level.scale]
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
			pass