# Platformer Game

Creating this game was a lockdown project to help me get used to Pygame again. The physics engine, level files, and art were all made by me.

Run `main.py` to launch!

---

## Contents
1. [Controls](#controls)
	- [During Normal Gameplay](#during-normal-gameplay)
	- [During Editing](#during-editing)
2. [Game Features](#game-features)
	- [Enemy Types](#enemy-types)
	- [Block Types](#block-types)
	- [Modes of Play](#modes-of-play)
3. [Things to Add](#things-to-add)

---

## Controls

### During Normal Gameplay
- **Movement:** `WASD` or arrow keys
- **Jump:** Space bar
- **Kill Enemies:** Jump on top of them
- **Die:** Collide with enemies from the side
- **Proceed to Next Level:** Reach the flag at the end of the level
- **Edit Mode:** Press `E` if stuck to enable edit mode, use `WASD` or arrow keys to move through enemies and blocks
- **Return to Menu:** Press `Escape`

### During Editing
- **Movement:** `WASD` or arrow keys
- **Switch Modes:** Press `E` to switch between normal and edit mode
- **Build Level:** Click on blocks in the menu at the bottom, then click on the map to place them
- **Delete Blocks:** Select the red `X` from the editing menu
- **Warning:** Touching the brown pole or flag during editing will lose your level

---

## Game Features

This is a nearly complete platforming game, including a level editor that saves level files, which can then be selected and played from level select. The level editor is still quite incomplete, but I'm working on allowing enemies to be placed. The file format for the levels is fairly simple and readable in any text editor:

1. **Static Objects:** Lines outline the static objects in the level, with different characters corresponding to different blocks. Lines must all be the same length with `.` denoting empty blocks.
2. **Blank Line:** Denotes the end of the main level part.
3. **Player Spawn Coordinates:** Two numbers giving `x,y` coordinates where the player spawns.
4. **Enemy List:** List of enemy names and their spawn coordinates. They spawn when the level is loaded.

### Enemy Types
- **Normal Goomba:** Falls straight into holes.
- **Smart Goomba:** Avoids falling into holes.
- **Spawner (Cannon):** Fires cannonballs at regular intervals.

### Block Types
- **Brick Blocks:** Breakable when hit from below.
- **Platform Blocks:** Collidable only from above.
- **Deadly Blocks:** Cause instant death on collision.
- **Flagpole and Flag Blocks:** Cause level completion on touch.
- **Cosmetic Cloud and Castle Blocks**

### Modes of Play
1. **New Game:** Starts at 1-1 and continues through harder levels.
2. **Level Select:** Start the game later or play custom levels.
3. **Level Editor:** Make and save your own levels, playable from level select.

---

## Things to Add
- Mob animation
- Level end animation
- Boss fight
- More levels
- General animation:
	- Dust on landing
	- Bricks breaking
	- Coin collection (question mark blocks do nothing atm)
- Finish level editing by:
	- Allowing player spawn location to change
	- Allowing mobs to be placed
	- Fixing cannons
	- Allowing clouds to be placed as a single block
- Menu animation and improved gameplay interface

---