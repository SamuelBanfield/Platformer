PLATFORMER GAME by Sam Banfield
---requires pygame---

------------------------------------------------------------------------------------

Creating this game was a lockdown project, to help me get used to pygame again. The physics engine, level files and art were all made by me. This file gives an outline of the features and controls, and the overall file structure of the game.

Run main.py to launch!

------------------------------------------------------------------------------------

CONTROLS:
During normal gameplay: 
wasd or arrow keys can be used, and the space bar will jump. Jumping on top of enemies kills them and going into their side kills you. Reach the flag at the end of the level to proceed to the next one. Press 'e' if you get stuck to enable edit mode, where you can use wasd or the arrow keys to move through enemies and blocks. Press escape to return to level select/ menu.

During editing:
Wasd or arrow keys to move freely. Press e to switch between normal mode where you can test the level youve built. To build a level, click on any of the blocks in the menu at the bottom, and then click on the map to place them. The cloud block must be placed seperately as left and right halves. Select the red x from the editing menu to delete anything you dont want. If you touch the brown pole or flag during editing, youll lose your level so be careful!

------------------------------------------------------------------------------------

It is a nearly complete platforming game, including a level editor which saves the level files, which can then be selected and played from level select. The level editor is still quite incomplete, but im working on allowing enemies to be placed. The file format for the levels is fairly simple, and is very readable in any text editor:

	-The first set of lines outline what the static objects in the level will look like, with different characters corresponding to different blocks, these lines must all be the same length with .'s denoting empty blocks
	-Then there is a blank line to denote end of main level part
	-Then there are two numbers giving x,y coordinates the player spawns at
	-Finally there is a list of enemy names, and the coordinates at which they spawn. They will all spawn when the level is loaded

There are two types of normal enemies, the smart and normal 'goomba's. The smart one will avoid falling into holes, the normal one will just fall straight in. There is also a 'spawner' (cannon) that fires cannonballs at regular intervals.

The types of blocks are:
	-brick blocks, which can be broken when hit from below
	-platform blocks, which you only collide with from above
	-deadly blocks, which cause instance death if you collide with them
	-flagpole and flag blocks, which cause level completion if you touch them
	-cosmetic cloud and castle blocks

There are three modes of play:
	-New game, starts at 1-1 and continues through to harder levels each time you complete one
	-Level select, allows you to start the game later on, or play custom player-made levels
	-Level editor, allows you to make your own levels and save them, they can then be played from level select

------------------------------------------------------------------------------------

Things to add:
	-animation for player
	-animation for mobs
	-animation at level end
	-boss fight
	-more levels
	-general animation:
		-dust on landing
		-bricks braking
		-coin collection (question mark blocks do nothing atm)
	-finish level editing by:
		-allowing spawn location of player to change
		-allowing mobs to be placed
		-fixing cannons
		-allowing clouds to be placed as a single block
	-menu animation, and improve interface for during gameplay

------------------------------------------------------------------------------------

File Structure:

main.py
mobs.py
enemy.py
interfaces.py
player.py
scene.py
images
levelfiles

main.py - This file contains the main functionality of the game including:
	main() - first function called, runs the menu and calls the draw menu function. Handles all events during menuing
	drawMenu() - draws the menu
	getButtons() - reads levelFiles and creates a menu to select level
	game() - main gameloop that loops in normal and edit modes
	drawScreen() - draws and updates the screen during gameplay
	eventHandle() - handles all events during gameplay

mobs.py - This file contains the base class from which players and enemies are inherited
	Mob: class for mobs including:
		-generateCollisions() - returns a list of all collisions based on old and new position of a mob, inherited by player
		-checkCollisions() - checks collisions based on movement
		-jump() sets y velocity, only used by player
		-updateImage() - updates the players image, does very little at the moment, but its the place to implement animation when i get to it

enemy.py - Contains classes for all hostile enemies, including a generic enemy class from which the others inherit.
	Enemy: inherits from mobs.Mob, generic enemy class
		-physicsUpdate() - finds and handles collisions, also deals with gravity, if the mob obeys it
		-generateCollisions() - generates collisions and is slightly smarter than the generic mob function
	CannonBall: inherits from enemy, this is the thing fired by 'spawners' (cannons)
		-update() - very generic, contains logic that removes cannonballs on hitting a wall
	Goomba: inherits from enemy, falls of the edge of platforms
		-update() - even more generic
	SmartGoombs: inherits from enemy, doesnt fall of the edge of platforms
		-update() - contains the logic for turning around when approaching the edge of a platform, otherwise generic

player.py - The logic for player collisions and physics
	Player: the character controlled by the player, only one instance ever created
		-reset() - called on death and at the end of the level, resets the players location and speed
		-mobCollisions() - handles mob collisions, either by death or causing a jump
		-update() - main update called every gametick. produces and handles all collisions, checks for death and level completion

scene.py - The module for handling level updates. contains the level class, 'scene'
	Scene: main level class, scene.objects contains all objects as a list, scene.mapobjects contains all mapobjects
		-resetMapObjects() - resetMapObject 'loads' all the information from scene.map into scene.mapObjects, by creating objects for the corresponding character
		-reset() - respawns mobs etc, when the player dies
	Block:
		-generic block object, contains the image of the block, and which sides it can be collided into
	Spawner: actually a cannon, spawns a cannonball at regular intervals
	Camera: camera object, follows the player around up to a certain slack, also is pulled downwards
	load() - loads a level from a file into a 2d 'map' array of characters
	save() - the inverse of load(), loses information about mob placement and player spawn though :(

interface.py - Module for buttons and interfaces, not the one used during menuing though. A lot of the logic for the interfaces and buttons is contained within the main file, so it might be a good idea to transfer this into main.py to have everything in one place, although main.py is already looking a bit too big so idk.
	TextButton: not used, should probably delete this
	ImageButton: the button used to show the objects in edit mode
	Interface: their are two instances of this object, the editing menu and the interface for choosing a levelname, this class basically only contains the image and rect and whether displaying or not, most of the logic is scattered throughout main.py

images - contains all the graphics used
levelFiles - contains all prebuilt and custom made levels

------------------------------------------------------------------------------------