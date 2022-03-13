import pygame

class TextButton:
	'''not used, the button class in main is used instead'''
	def __init__(self, size, text, colour, hoverColour = None):
		self.font = getFont(size)
		self.text = text
		self.image = self.font.render(text, True, colour)
		if hoverColour == None:
			hoverColour = colour
		self.hoverImage = self.font.render(text, True, hoverColour)
		self.rect = self.image.get_rect()
		self.currentImage = self.image

class ImageButton:
	def __init__(self, image, name):
		self.image = image
		self.rect = image.get_rect()
		self.name = name

class Interface:
	def __init__(self, width, height, buttonList, offset, displayMode='horizontal'):
		self.displaying = False
		self.width = width
		self.height = height
		self.buttonList = buttonList
		self.image = pygame.Surface((width, height))
		self.offset = offset
		if displayMode == 'horizontal':
			for i in range(len(buttonList)):
				button = buttonList[i]
				button.rect.topleft = 10+40*i, 10
		else:
			print('that displayMode is not implemented')
		self.updateImage()

	def updateImage(self):
		self.image.fill((255,255,255))
		
		for button in self.buttonList:
			self.image.blit(button.image, button.rect)

	def __str__(self):
		print('interface')


def inside(point, pygameRect):
	return pygameRect.left < point[0] < pygameRect.right and pygameRect.top < point[1] < pygameRect.bottom