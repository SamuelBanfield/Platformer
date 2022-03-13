import pygame, sys, os
import player, enemy, scene, interfaces
from pygame.locals import *
pygame.init()

deleteImage = pygame.image.load('images/delete.png')

class Button():
	def __init__(self, size, text, colour, hoverColour = None):
		self.font = getFont(size)
		self.text = text
		self.image = self.font.render(text, True, colour)
		if hoverColour == None:
			hoverColour = colour
		self.hoverImage = self.font.render(text, True, hoverColour)
		self.rect = self.image.get_rect()
		self.currentImage = self.image

def inside(point, pygameRect):
	return pygameRect.left < point[0] < pygameRect.right and pygameRect.top < point[1] < pygameRect.bottom

def main():
	WIDTH = 800
	HEIGHT = 600
	FPS = 40
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Platformer')
	CLOCK = pygame.time.Clock()

	title = Button(40, 'Welcome to Platformer!', (255,255,255))
	title.rect.center = (WIDTH//2, 6*HEIGHT//15)
	info = Button(30, 'New Game', (255,255,255), (0,0,0))
	info.rect.center = (WIDTH//2, 8*HEIGHT//15)
	chooseLevelButton = Button(30, 'Level select', (255,255,255), (0,0,0))
	chooseLevelButton.rect.center = (WIDTH//2, 9*HEIGHT//15)
	levelEditButton = Button(30, 'Level editor', (255,255,255), (0,0,0))
	levelEditButton.rect.center = (WIDTH//2, 10*HEIGHT//15)

	buttons = [title, info, chooseLevelButton, levelEditButton]
	running = True
	while running:
		for button in buttons:
			if inside(pygame.mouse.get_pos(), button.rect):
				button.currentImage = button.hoverImage
			else:
				button.currentImage = button.image
		drawMenu(SCREEN, buttons)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if inside(pygame.mouse.get_pos(), info.rect):
					game(CLOCK, SCREEN, WIDTH, HEIGHT, FPS, '1-1.txt', False)
				if inside(pygame.mouse.get_pos(), chooseLevelButton.rect):
					buttons = getButtons(WIDTH, HEIGHT)
				if inside(pygame.mouse.get_pos(), levelEditButton.rect):
					game(CLOCK, SCREEN, WIDTH, HEIGHT, FPS, 'blankLevel.txt', True)
				for button in buttons:
					if inside(pygame.mouse.get_pos(), button.rect):
						if button.text+'.txt' in os.listdir('levelFiles'):
							game(CLOCK, SCREEN, WIDTH, HEIGHT, FPS, button.text+'.txt', False)

def getButtons(WIDTH, HEIGHT):
	'''Gets the buttons for level files'''
	menuButtons = []
	for buttonString in os.listdir('levelFiles'):
		if buttonString != '.DS_Store':
			menuButtons.append(Button(30, buttonString[:-4], (255,255,255), (0,0,0)))
	for x in range(len(menuButtons)):
		menuButtons[x].rect.center = (WIDTH//4+(WIDTH//4)*(x%3), HEIGHT//4+(x//3)*(HEIGHT//10))
	return menuButtons

def drawMenu(SCREEN, buttons):
	SCREEN.fill((64,189,255))
	for button in buttons:
		SCREEN.blit(button.currentImage, button.rect)
	pygame.display.flip()

def game(CLOCK, SCREEN, WIDTH, HEIGHT, FPS, startScene, editMode):
	scale = 40
	slack = [250,150]
	currentScene = scene.Scene(startScene, scale, FPS)
	gameImage = pygame.Surface((currentScene.imageWidth, currentScene.imageHeight))
	character = player.Player(scale, FPS, currentScene.playerStartPosition[0]*scale, currentScene.playerStartPosition[1]*scale)
	camera = scene.Camera(slack)
	buttonList = [interfaces.ImageButton(scene.imageDict[block], block) for block in scene.imageDict if block != 'castle']
	buttonList.append(interfaces.ImageButton(deleteImage, ' '))
	editInterface = interfaces.Interface(scale*(len(buttonList))+20, 20+scale, buttonList, [(WIDTH-scale*(len(buttonList))-20)//2,HEIGHT-20-scale], )
	editInterface.currentlySelected = ' '
	editInterface.displaying = editMode
	w, h = 600, 100
	saving = False
	savingInterface = interfaces.Interface(w, h, [], [(WIDTH-w)//2,(HEIGHT-h)//2])
	savingInterface.levelname = ''

	playing = True
	paused = False
	time = 0
	levelDelayTime = 20

	while playing:
		playing = eventHandle(pygame.event.get(), currentScene, character, editInterface, savingInterface, camera, WIDTH, HEIGHT, editMode)
		drawScreen(SCREEN, currentScene, gameImage, character, camera, scale, editInterface, savingInterface, editMode)
		if currentScene.complete:
			if not paused:
				completeTime = time
				paused = True
			if time > completeTime + levelDelayTime:
				if currentScene.name in nextLevel:
					currentScene = scene.Scene(nextLevel[currentScene.name], scale, FPS)
					character.startx, character.starty = currentScene.playerStartPosition[0]*scale, currentScene.playerStartPosition[1]*scale
				else:
					currentScene = scene.Scene(currentScene.name, scale, FPS)
				camera = scene.Camera(slack)
				gameImage = pygame.Surface((currentScene.imageWidth, currentScene.imageHeight))
				character.reset(currentScene)
				paused = False

		if not (paused or editInterface.displaying):
			character.update(currentScene)
			for mob in currentScene.mobs:
				mob.update(currentScene)
			for spawner in currentScene.spawners:
				spawner.update(character, time)

		time += 1
		CLOCK.tick(FPS)

def drawScreen(canvas, currentScene, gameImage, character, camera, scale, editInterface, savingInterface, editMode):
	'''draws everything to the main canvas'''
	camera.updateOffset(character, canvas.get_width(), canvas.get_height())
	if editInterface.displaying:
		fillColour = (40,130,200)
	else:
		fillColour = (64,189,255)
	canvas.fill(fillColour)
	sceneImage = currentScene.image
	gameImage.blit(sceneImage,(0,0))
	for mob in currentScene.mobs:
		mob.updateImage()
		mobRect = mob.image.get_rect()
		mobRect.topleft = (mob.x, mob.y)
		gameImage.blit(mob.image, mobRect)
	canvas.blit(gameImage, camera.offset)
	rect = character.image.get_rect()
	rect.topleft = (character.x+camera.offset[0], character.y+camera.offset[1])
	character.updateImage()
	canvas.blit(character.image, rect)
	if editMode == False:
		canvas.blit(font.render(currentScene.name[:-4] + '  Deaths: ' + str(character.deaths), True, (0,0,0)), font.render('Hello', True, (0,0,0)).get_rect())
	else:
		editImage = font.render('You are in edit mode, press e to toggle flight', True, (0,0,0))
		canvas.blit(editImage, editImage.get_rect())

	if editInterface.displaying:
		#handles drawing on the edit interface and text
		editImage = font.render('Press the escape key to save and name your level', True, (0,0,0))
		editRect = editImage.get_rect()
		editRect.top = editRect.height
		canvas.blit(editImage, editRect)
		canvas.blit(editInterface.image, (canvas.get_size()[0]//2 - editInterface.width//2,canvas.get_size()[1]-editInterface.height))
	if savingInterface.displaying:
		savingInterface.updateImage()

		levelnameText = font.render(savingInterface.levelname, True, (255,0,0))
		levelnameRect = levelnameText.get_rect()
		levelnameRect.center = (savingInterface.image.get_size()[0]//2, 2*savingInterface.image.get_size()[1]//3)
		savingInterface.image.blit(levelnameText, levelnameRect)

		instructionText = font.render('Type your level name then press enter to save:', True, (0,0,0))
		instructionRect = instructionText.get_rect()
		instructionRect.center = (savingInterface.image.get_size()[0]//2, 1*savingInterface.image.get_size()[1]//3)
		savingInterface.image.blit(instructionText, instructionRect)

		canvas.blit(savingInterface.image, (canvas.get_size()[0]//2 - savingInterface.width//2,canvas.get_size()[1]//2-savingInterface.height//2))
	pygame.display.flip()

def eventHandle(events, currentScene, character, editInterface, savingInterface, camera, WIDTH, HEIGHT, editMode):
	'''handles all click, typing and quit events while a game is being played'''
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE and editMode == False:
				return False
			if event.key == K_ESCAPE and editInterface.displaying:
				savingInterface.displaying = not savingInterface.displaying
			elif savingInterface.displaying:
				if 97 <= event.key <= 122:
					#adding characters to guess
					if len(savingInterface.levelname) < 20:
						savingInterface.levelname += chr(event.key)
				elif event.key == 8:
					#Dealing with the backspace key
					if len(savingInterface.levelname) > 0:
						savingInterface.levelname = savingInterface.levelname[:-1]
				elif event.key == 13:
					scene.save(savingInterface.levelname, currentScene.map)
					return False
			else:
				if event.key == K_e:
					editInterface.displaying = not editInterface.displaying
				if (event.key in [K_SPACE, K_UP, K_w]) and not editInterface.displaying:
					if character.landed:
						character.jump()
			
		if event.type == MOUSEBUTTONDOWN and editInterface.displaying:
			#calculating location of click within map:
			mousePos = pygame.mouse.get_pos()
			if (WIDTH-editInterface.width)//2 <= mousePos[0] <= (WIDTH+editInterface.width)//2 and HEIGHT-editInterface.height <= mousePos[1]:
				for button in editInterface.buttonList:
					if inside([mousePos[0]-editInterface.offset[0],mousePos[1]-editInterface.offset[1]], button.rect):
						editInterface.currentlySelected = button.name
						print(button.name, ' is the current block')
			elif savingInterface.displaying and (WIDTH-savingInterface.width)//2 <= mousePos[0] <= (WIDTH+savingInterface.width)//2 and (HEIGHT-savingInterface.height)//2 <= mousePos[1] <= (HEIGHT+savingInterface.height)//2:
				pass
			else:
				x, y = (pygame.mouse.get_pos()[0]-camera.offset[0])//currentScene.scale,(pygame.mouse.get_pos()[1]-camera.offset[1])//currentScene.scale
				sceneWidth = len(currentScene.map)
				sceneHeight = len(currentScene.map[0])
				if 0 <= x < sceneWidth and 0 <= y < sceneHeight:

					if currentScene.objectMap[x][y] != None:
						#removes the object from the map object list if there is currently one at that location
						currentScene.objects.remove(currentScene.objectMap[x][y])
					if editInterface.currentlySelected != ' ':
						#adding new object
						b = scene.Block(currentScene, x, y, currentScene.scale, editInterface.currentlySelected)
						currentScene.objectMap[x][y] = b
						currentScene.objects.append(b)
						currentScene.map[x][y] = scene.getIndex(scene.objectDict, editInterface.currentlySelected)
						currentScene.updateImage()
					else:
						#removing object in the case that delete has been selected
						currentScene.objectMap[x][y] = None
						currentScene.map[x][y] = ' '
						currentScene.updateImage()

	pressed = pygame.key.get_pressed()
	if not savingInterface.displaying:
		if editInterface.displaying:
			if pressed[K_LEFT] or pressed[K_a]:
				character.facingDirection = -1
				character.x -= character.speed*4
			if pressed[K_RIGHT] or pressed[K_d]:
				character.facingDirection = +1
				character.x += character.speed*4
			if pressed[K_UP] or pressed[K_w]:
				character.y -= character.speed*4
			if pressed[K_DOWN] or pressed[K_s]:
				character.y += character.speed*4

		else:
			if pressed[K_LEFT] or pressed[K_a]:
				character.facingDirection = -1
				if character.landed:
					character.xdot -= character.speed
				else:
					character.xdot -= character.speed/2
			if pressed[K_RIGHT] or pressed[K_d]:
				character.facingDirection = 1
				if character.landed:
					character.xdot += character.speed
				else:
					character.xdot += character.speed/2

	return True

nextLevel = {
	'1-1.txt': '1-2.txt',
	'1-2.txt': '2-1.txt',
	'2-1.txt': '3-1.txt',
	'3-1.txt': '3-2.txt'
}
def getFont(size):
	return pygame.font.Font(pygame.font.get_default_font(), size)
font = getFont(24)

if __name__ == '__main__':
	main()