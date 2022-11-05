import os
from interfaces import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def getTitleScreenButtons(screenWidth, screenHeight):
    title = Button(40, 'Welcome to Platformer!', WHITE)
    title.rect.center = (screenWidth // 2, 6 * screenHeight // 15)
    newGameButton = Button(30, 'New Game', WHITE, BLACK)
    newGameButton.rect.center = (screenWidth // 2, 8 * screenHeight // 15)
    levelSelectButton = Button(30, 'Level select', WHITE, BLACK)
    levelSelectButton.rect.center = (screenWidth//2, 9*screenHeight//15)
    levelEditButton = Button(30, 'Level editor', WHITE, BLACK)
    levelEditButton.rect.center = (screenWidth // 2, 10 * screenHeight // 15)

    return [title, newGameButton, levelSelectButton, levelEditButton]

def getLevelSelectButtons(screenWidth, screenHeight):
    '''Gets the buttons for level files'''
    menuButtons = []
    for buttonString in os.listdir('levelFiles'):
        # This is probably a bit platform specific
        if buttonString != '.DS_Store':
            menuButtons.append(Button(30, buttonString[:-4], WHITE, BLACK))
    for x in range(len(menuButtons)):
        menuButtons[x].rect.center = (
            screenWidth // 4 + (screenWidth // 4) * (x % 3),
            screenHeight // 4 + (x // 3) * (screenHeight // 10)
            )
    return menuButtons